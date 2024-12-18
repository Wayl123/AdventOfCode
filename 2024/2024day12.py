import os
import numpy as np
import math
from itertools import groupby

gardenTypeCoord = {}
inputMapAsArray = []

def find_cluster(coord, visited, areaPerimeter, sideDict):
  if coord[0] - 1 >= 0 and (coord[0] - 1, coord[1]) in visited:
    checkCoord = (coord[0] - 1, coord[1])
    if not visited[checkCoord]:
      visited[checkCoord] = True
      areaPerimeter[0] += 1
      find_cluster(checkCoord, visited, areaPerimeter, sideDict)
  else:
    areaPerimeter[1] += 1
    if not coord[0] in sideDict["^"]:
      sideDict["^"][coord[0]] = []
    sideDict["^"][coord[0]].append(coord[1])

  if coord[1] + 1 < inputMapAsArray.shape[1] and (coord[0], coord[1] + 1) in visited:
    checkCoord = (coord[0], coord[1] + 1)
    if not visited[checkCoord]:
      visited[checkCoord] = True
      areaPerimeter[0] += 1
      find_cluster(checkCoord, visited, areaPerimeter, sideDict)
  else:
    areaPerimeter[1] += 1
    if not coord[1] in sideDict[">"]:
      sideDict[">"][coord[1]] = []
    sideDict[">"][coord[1]].append(coord[0])

  if coord[0] + 1 < inputMapAsArray.shape[0] and (coord[0] + 1, coord[1]) in visited:
    checkCoord = (coord[0] + 1, coord[1])
    if not visited[checkCoord]:
      visited[checkCoord] = True
      areaPerimeter[0] += 1
      find_cluster(checkCoord, visited, areaPerimeter, sideDict)
  else:
    areaPerimeter[1] += 1
    if not coord[0] in sideDict["v"]:
      sideDict["v"][coord[0]] = []
    sideDict["v"][coord[0]].append(coord[1])

  if coord[1] - 1 >= 0 and (coord[0], coord[1] - 1) in visited:
    checkCoord = (coord[0], coord[1] - 1)
    if not visited[checkCoord]:
      visited[checkCoord] = True
      areaPerimeter[0] += 1
      find_cluster(checkCoord, visited, areaPerimeter, sideDict)
  else:
    areaPerimeter[1] += 1
    if not coord[1] in sideDict["<"]:
      sideDict["<"][coord[1]] = []
    sideDict["<"][coord[1]].append(coord[0])

def find_side_group(sideArray):
  sideAmount = 0

  for _, _ in groupby(enumerate(sideArray), lambda x : x[0] - x[1]):
    sideAmount += 1

  return sideAmount

def find_cluster_price(gardenType):
  visited = dict.fromkeys(gardenType, False)

  q1Price, q2Price = 0, 0

  while not all(checked for checked in visited.values()):
    # When side is ^ or v, the key will be the y level with x as value
    # When side is > or <, the key will be the x level with y as value
    sideDict = {"^": {}, ">": {}, "v": {}, "<": {}}
    areaPerimeter = [0, 0]
    checkCoord = next((checked[0] for checked in visited.items() if not checked[1]))
    visited[checkCoord] = True
    areaPerimeter[0] += 1
    find_cluster(checkCoord, visited, areaPerimeter, sideDict)

    sideAmount = 0

    for sides in sideDict.values():
      for sideArray in sides.values():
        sideArray.sort()
        sideAmount += find_side_group(sideArray)

    q1Price += math.prod(areaPerimeter)
    q2Price += areaPerimeter[0] * sideAmount

  return q1Price, q2Price

def get_garden_price(inputMap):
  global gardenTypeCoord, inputMapAsArray

  rows = inputMap.split("\n")

  for y, row in enumerate(rows):
    rows[y] = list(row)
    for x, col in enumerate(row):
      if not col in gardenTypeCoord:
        gardenTypeCoord[col] = set()
      gardenTypeCoord[col].add((y, x))

  inputMapAsArray = np.array(rows)

  prices = [0, 0]

  for gardenType in gardenTypeCoord.values():
    prices = np.add(prices, find_cluster_price(gardenType))

  return prices

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day12input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(*get_garden_price(inputFile.read()))