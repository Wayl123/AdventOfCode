import os
from functools import cache

towelPatterns = []

@cache
def check_towel_pattern(towelDesign):
  if not towelDesign:
    return 1

  return sum(check_towel_pattern(towelDesign[len(towelPattern):]) 
             for towelPattern in towelPatterns if towelDesign.startswith(towelPattern))

def read_towel_pattern(input):
  global towelPatterns

  towelPatternsDesigns = input.split("\n\n")
  towelPatterns = towelPatternsDesigns[0].split(", ")
  towelDesigns = towelPatternsDesigns[1].split("\n")

  result = [check_towel_pattern(towelDesign) for towelDesign in towelDesigns]

  return sum(map(bool, result)), sum(result)

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day19input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_towel_pattern(inputFile.read()))