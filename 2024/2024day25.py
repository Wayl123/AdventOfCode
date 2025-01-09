import os
import numpy as np
from itertools import product

def convert_schematic_to_num(schematic):
  return np.count_nonzero(schematic == "#", axis = 0) - 1

def try_key_lock(pair):
  sum = np.add(*pair)

  return all(sum < 6)

def read_schematic(input):
  schematics = input.split("\n\n")

  locks = []
  keys = []

  for schematic in schematics:
    schematicRows = schematic.split("\n")
    schematicArray = np.array(list(map(list, schematicRows)))
    schematicNum = convert_schematic_to_num(schematicArray)

    if all(schematicArray[0] == "#"):
      locks.append(schematicNum)
    elif all(schematicArray[0] == "."):
      keys.append(schematicNum)

  fitCount = 0

  for pair in product(locks, keys):
    if try_key_lock(pair):
      fitCount += 1

  return fitCount

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day25input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_schematic(inputFile.read()))