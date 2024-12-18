import os
import math
from functools import cache

depthLimit = 75

@cache
def apply_rule(stone, depth):
  if depth == depthLimit:
    return 1
  
  stoneCount = 0

  if stone == 0:
    stoneCount += apply_rule(1, depth + 1)
  elif math.floor(math.log10(stone) + 1) % 2 == 0:
    digitCount = math.floor(math.log10(stone) + 1)
    stoneCount += apply_rule(math.floor(stone / (10 ** (digitCount / 2))), depth + 1)
    stoneCount += apply_rule(stone % (10 ** (digitCount / 2)), depth + 1)
  else:
    stoneCount += apply_rule(stone * 2024, depth + 1)

  return stoneCount

def get_stone_num(input):
  inputStones = list(map(int, input.split()))

  stoneCount = 0

  for stone in inputStones:
    stoneCount += apply_rule(stone, 0)

  return stoneCount

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day11input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(get_stone_num(inputFile.read()))