import os

visitedHouse = {}

def add_house_to_dict(x, y):
  coord = str(x) + "," + str(y)

  if coord not in visitedHouse:
    visitedHouse[coord] = 1
  else:
    visitedHouse[coord] += 1

def read_delivery_path(path):
  x = [0, 0]
  y = [0, 0]

  altFlag = True

  add_house_to_dict(x[0], y[0])
  add_house_to_dict(x[1], y[1])

  for direction in path:
    altIndex = 0 if altFlag else 1

    match direction:
      case ">":
        x[altIndex] += 1
      case "<":
        x[altIndex] -= 1
      case "^":
        y[altIndex] += 1
      case "v":
        y[altIndex] -= 1
    
    add_house_to_dict(x[altIndex], y[altIndex])

    altFlag = not altFlag

  return len(visitedHouse)

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day3input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_delivery_path(inputFile.read()))