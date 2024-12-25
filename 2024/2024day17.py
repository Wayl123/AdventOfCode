import os
import copy
import re

def get_combo_operand(operand, registers):
  if operand < 0 or operand > 6:
    return "Invalid"
  elif operand > 3 and operand <= 6:
    return registers[operand - 4]
  return operand

def read_instruction(instructions, registers):
  pointer = 0
  out = []

  while pointer < len(instructions):
    opcode = instructions[pointer]
    operand = instructions[pointer + 1]

    match opcode:
      case 0: # adv
        registers[0] = registers[0] >> get_combo_operand(operand, registers)
      case 1: # bxl
        registers[1] = registers[1] ^ operand
      case 2: # bst
        registers[1] = get_combo_operand(operand, registers) % 8
      case 3: # jnz
        if registers[0] != 0:
          pointer = operand
          continue
      case 4: # bxc
        registers[1] = registers[1] ^ registers[2]
      case 5: # out
        out.append(get_combo_operand(operand, registers) % 8)
      case 6: # bdv
        registers[1] = registers[0] >> get_combo_operand(operand, registers)
      case 7: # cdv
        registers[2] = registers[0] >> get_combo_operand(operand, registers)

    pointer += 2

  return out

def find_copy(instructions, expectedOut, regs, prevA = 0, depth = 0):
  # Out of expected output value to test
  if not expectedOut:
    return prevA
  # Find lower 3 bit of A that gives the right most expected output pattern
  for a in range(8):
    # By property of the instruction, the output is preserved when it get lshifted 3 bit (main thing that need to be observed for this problem)
    #   - Out reads 0-3 or last 3 bit of reg A, B, or C
    #   - Reg B and C depends on rshift of reg A, and some xor of last 3 bit or truncating to last 3 bit
    #   - All output should depend on shifting of A
    testA = (prevA << 3) | a
    # If output is longer than depth, there is extra output in between
    testOut = read_instruction(instructions, [testA, regs[1], regs[2]])
    if testOut[0] == expectedOut[-1] and len(testOut) == depth + 1:
      # Found right most output, move to next one
      out = find_copy(instructions, expectedOut[:-1], regs, testA, depth + 1)
      if out is not None:
        return out

def read_program(input):
  regsInstruction = list(map(int, re.findall(r"\d+", input)))
  regs = regsInstruction[:3]
  instructions = regsInstruction[3:]

  return ",".join(map(str, read_instruction(instructions, copy.deepcopy(regs)))), find_copy(instructions, instructions, tuple(regs))

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day17input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_program(inputFile.read()))