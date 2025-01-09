import os
from collections import deque

wires = {}
cmdQueue = deque([])

operators = {
  "AND": lambda x, y: x & y,
  "OR": lambda x, y: x | y,
  "XOR": lambda x, y: x ^ y,
  "EQUAL": lambda x: x
}

def check_if_input_initialized(input):
  return input.isnumeric() or (input in wires and "updated" in wires[input] and wires[input]["updated"])

def check_if_output_waiting(output):
  global cmdQueue

  if output in wires:
    if not ("updated" in wires[output] and wires[output]["updated"]) and "operation" in wires[output]:
      cmdQueue.extend(wires[output]["operation"])
  else:
    wires[output] = {}
    wires[output]["updated"] = False
    wires[output]["operation"] = set()

def get_value(input):
  return int(input) if input.isnumeric() else wires[input]["value"]

def append_instruction_to_input(input, cmd):
  global wires

  if not (input in wires and "operation" in wires[input]):
    wires[input] = {}
    wires[input]["updated"] = False
    wires[input]["operation"] = set()
  wires[input]["operation"].add(cmd)

def execute_command_queue():
  global cmdQueue

  while cmdQueue:
    execute_instruction(cmdQueue.popleft(), False)

def initialize_input(inputList):
  inputs = inputList.split("\n")

  for input in inputs:
    wireInput = input.split(": ")
    execute_instruction(wireInput[1] + " -> " + wireInput[0])

def execute_instruction(cmd, addToQueueFlag = True):
  global wires

  inOut = cmd.split(" -> ")
  inInstr = inOut[0].split()

  match len(inInstr):
    case 1:
      if check_if_input_initialized(inInstr[0]):
        check_if_output_waiting(inOut[1])
        if not wires[inOut[1]]["updated"]: wires[inOut[1]]["value"] = operators["EQUAL"](get_value(inInstr[0]))
        wires[inOut[1]]["updated"] = True
        if inInstr[0].isnumeric():
          wires[inOut[1]]["endpoint"] = True
      if not inInstr[0].isnumeric() and addToQueueFlag:
        append_instruction_to_input(inInstr[0], cmd)
    case 3:
      if check_if_input_initialized(inInstr[0]) and check_if_input_initialized(inInstr[2]):
        check_if_output_waiting(inOut[1])
        wires[inOut[1]]["value"] = operators[inInstr[1]](get_value(inInstr[0]), get_value(inInstr[2]))
        wires[inOut[1]]["updated"] = True
        if inInstr[0].isnumeric() and inInstr[2].isnumeric():
          wires[inOut[1]]["endpoint"] = True
      if addToQueueFlag:
        if not inInstr[0].isnumeric():
          append_instruction_to_input(inInstr[0], cmd)
        if not inInstr[2].isnumeric():
          append_instruction_to_input(inInstr[2], cmd)
  
  if addToQueueFlag:
    execute_command_queue()

def fix_incorrect_pair(pairs, wireInput):
  global wires

  for pair in pairs:
    for i in range(2):
      curWire = pair[i]
      otherWire = pair[(i + 1) % 2]

      operation = wireInput[curWire]
      inputs = operation.split()

      for input in inputs[0::2]:
        wires[input]["operation"].remove(operation + " -> " + curWire)
        wires[input]["operation"].add(operation + " -> " + otherWire)

def find_incorrect_pair(incorrectWires):
  global wires

  wirePairs = []
  incorrectWiresList = sorted(incorrectWires.keys())

  # To find the pair we find the next output in the sequence closest to the incorrect wire
  for incorrectWire in incorrectWiresList[: len(incorrectWiresList) // 2]:
    checkNextQueue = deque([])
    checkNextQueue.extend(wires[incorrectWire]["operation"])

    while checkNextQueue:
      operation = checkNextQueue.popleft()

      inOut = operation.split(" -> ")
      if inOut[1][0] == "z":
        # The output wire here is the next in the sequence, we want the one parallel to the wire we checking so we minus 1
        wireNum = int(inOut[1][1:]) - 1
        wirePairs.append((incorrectWire, "z" + f"{wireNum :02d}"))
        break
      else:
        checkNextQueue.extend(wires[inOut[1]]["operation"])

  # Swap operation
  fix_incorrect_pair(wirePairs, incorrectWires)

def fix_adder(instrList):
  # Structure is a ripple carry adder
  # For one bit full adder 
  # Output z is x XOR y XOR c (c as carry bit)
  # Next carry bit is (x AND y) OR ((x XOR y) AND c)
  # From this we observe that
  # Output z is preceeded by XOR (except for the output bit since that just take the carry bit)
  # Output that are not z and input not x or y operation must be AND or OR but not XOR
  incorrectWires = {}

  for instr in instrList:
    inOut = instr.split(" -> ")
    inInstr = inOut[0].split()

    if inOut[1][0] == "z" and len(inInstr) == 3 and inInstr[1] != "XOR" and inOut[1] != "z45":
      incorrectWires[inOut[1]] = inOut[0]
    if inOut[1][0] != "z" and len(inInstr) == 3 and inInstr[1] == "XOR" and not inInstr[0][0] in ["x", "y"] and not inInstr[2][0] in ["x", "y"]:
      incorrectWires[inOut[1]] = inOut[0]

  find_incorrect_pair(incorrectWires)

  # Find incorrect carry bit
  # Set both input to all 1
  # The bit that shows 0 (except 0th bit) have messes up the carry bit
  # The output of the two operations of that adders input is likely the one swapped, the x AND y and x XOR y
  for w in wires:
    wires[w]["updated"] = False

  for w in wires:
    if ("endpoint" in wires[w] and wires[w]["endpoint"]) and ("updated" in wires[w] and not wires[w]["updated"]):
      execute_instruction(str(1) + " -> " + w)

  zKeys = sorted([key for key in wires.keys() if key[0] == "z"], reverse = True)
  incorrectCarry = [key for key in zKeys if wires[key]["value"] == 0 and key != "z00"]

  incorrectPairs = []

  for incorrect in incorrectCarry:
    incorrectNum = incorrect[1:]
    incorrectOperation = wires["x" + incorrectNum]["operation"]
    incorrectPair = []

    for operation in incorrectOperation:
      inOut = operation.split(" -> ")
      incorrectPair.append(inOut[1])
      incorrectWires[inOut[1]] = inOut[0]

    incorrectPairs.append(tuple(incorrectPair))

  fix_incorrect_pair(incorrectPairs, incorrectWires)

  return ",".join(sorted(incorrectWires.keys()))

def read_instruction(input):
  global wires

  inputInstr = input.split("\n\n")
  instrList = inputInstr[1].split("\n")

  initialize_input(inputInstr[0])

  for instr in instrList:
    execute_instruction(instr)

  zKeys = sorted([key for key in wires.keys() if key[0] == "z"], reverse = True)
  result = int("".join(map(str, [wires[key]["value"] for key in zKeys])), 2)

  # Fix adder and rerun adder
  incorrectWires = fix_adder(instrList)

  for w in wires:
    wires[w]["updated"] = False

  initialize_input(inputInstr[0])

  zKeys = sorted([key for key in wires.keys() if key[0] == "z"], reverse = True)
  q2Result = int("".join(map(str, [wires[key]["value"] for key in zKeys])), 2)

  # Actual result
  xKeys = sorted([key for key in wires.keys() if key[0] == "x"], reverse = True)
  yKeys = sorted([key for key in wires.keys() if key[0] == "y"], reverse = True)
  xValue = int("".join(map(str, [wires[key]["value"] for key in xKeys])), 2)
  yValue = int("".join(map(str, [wires[key]["value"] for key in yKeys])), 2)
  expected = xValue + yValue

  print(expected == q2Result)

  return result, q2Result, incorrectWires

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day24input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_instruction(inputFile.read()))