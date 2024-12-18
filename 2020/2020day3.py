import os

def get_tree_count(mapList, x, y):
  count = 0

  for yIndex, line in enumerate(mapList[::y]):
    xIndex = (yIndex * x) % len(line)
    if line[xIndex] == "#":
      count += 1

  return count

def get_product_of_multiple_slope(inputMap):
  mapList = inputMap.split("\n")

  count = 1

  count *= get_tree_count(mapList, 1, 1)
  count *= get_tree_count(mapList, 3, 1)
  count *= get_tree_count(mapList, 5, 1)
  count *= get_tree_count(mapList, 7, 1)
  count *= get_tree_count(mapList, 1, 2)

  return count

inputFilePath = os.path.dirname(__file__) + "\\input\\2020day3input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_product_of_multiple_slope(inputFile.read()))