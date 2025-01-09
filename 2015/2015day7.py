import os
import numpy as np
from collections import deque

wires = {}
cmdQueue = deque([])

operators = {
  "AND": lambda x, y: x & y,
  "OR": lambda x, y: x | y,
  "NOT": lambda x: ~x,
  "LSHIFT": lambda x, y: x << y,
  "RSHIFT": lambda x, y: x >> y,
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
  return np.uint16(input) if input.isnumeric() else wires[input]["value"]

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
    execute_instruction(cmdQueue.popleft(), True)

def execute_instruction(cmd, repeatFlag = False):
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
      if not inInstr[0].isnumeric() and not repeatFlag:
        append_instruction_to_input(inInstr[0], cmd)
    case 2:
      if check_if_input_initialized(inInstr[1]):
        check_if_output_waiting(inOut[1])
        wires[inOut[1]]["value"] = operators[inInstr[0]](get_value(inInstr[1]))
        wires[inOut[1]]["updated"] = True
        if inInstr[1].isnumeric():
          wires[inOut[1]]["endpoint"] = True
      if not inInstr[1].isnumeric() and not repeatFlag:
        append_instruction_to_input(inInstr[1], cmd)
    case 3:
      if check_if_input_initialized(inInstr[0]) and check_if_input_initialized(inInstr[2]):
        check_if_output_waiting(inOut[1])
        wires[inOut[1]]["value"] = operators[inInstr[1]](get_value(inInstr[0]), get_value(inInstr[2]))
        wires[inOut[1]]["updated"] = True
        if inInstr[0].isnumeric() and inInstr[2].isnumeric():
          wires[inOut[1]]["endpoint"] = True
      if not repeatFlag:
        if not inInstr[0].isnumeric():
          append_instruction_to_input(inInstr[0], cmd)
        if not inInstr[2].isnumeric():
          append_instruction_to_input(inInstr[2], cmd)
  
  if not repeatFlag:
    execute_command_queue()

def read_instruction(input):
  global wires

  instrList = input.split("\n")

  for instr in instrList:
    execute_instruction(instr)

  result = wires["a"]["value"]

  for w in wires:
    wires[w]["updated"] = False

  execute_instruction(str(result) + " -> b")

  for w in wires:
    if ("endpoint" in wires[w] and wires[w]["endpoint"]) and ("updated" in wires[w] and not wires[w]["updated"]):
      execute_instruction(str(wires[w]["value"]) + " -> " + w)

  return result, wires["a"]["value"]

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day7input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_instruction(inputFile.read()))