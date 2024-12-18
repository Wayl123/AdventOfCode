import os

def get_floor(input):
  floor = 0
  firstBasement = None

  for index, char in enumerate(input):
    match char:
      case "(":
        floor += 1
      case ")":
        floor -= 1

    if floor == -1 and firstBasement is None:
      firstBasement = index + 1
  
  return floor, firstBasement

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day1input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_floor(inputFile.read()))