import os
import re

def get_mul_result(mulOperation):
  mulNum = list(map(int, re.findall(r"\d+", mulOperation)))
  
  return mulNum[0] * mulNum[1]

def find_mul(input):
  mulOperations = re.findall(r"mul\(\d+,\d+\)|don't\(\)|do\(\)", input)

  enabled = True
  sum = 0
  
  for operation in mulOperations:
    if operation == "don't()" or operation == "do()":
      enabled = False if operation == "don't()" else True
      continue

    if enabled:
      sum += get_mul_result(operation)

  return sum

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day3input.txt"
with open(inputFilePath, "r") as inputFile:
  print(find_mul(inputFile.read()))