import os
import numpy as np
import copy

def push_boxes(mapArray, direction, coord, boxesPushed):
  nextCoord = copy.deepcopy(coord)
  nextCoord2 = None
  pushable = []

  match direction:
    case "^":
      nextCoord[0] -= 1
      if mapArray[tuple(nextCoord)] == "[":
        nextCoord2 = [nextCoord[0], nextCoord[1] + 1]
      elif mapArray[tuple(nextCoord)] == "]":
        nextCoord2 = [nextCoord[0], nextCoord[1] - 1]
    case ">":
      nextCoord[1] += 1
    case "v":
      nextCoord[0] += 1
      if mapArray[tuple(nextCoord)] == "[":
        nextCoord2 = [nextCoord[0], nextCoord[1] + 1]
      elif mapArray[tuple(nextCoord)] == "]":
        nextCoord2 = [nextCoord[0], nextCoord[1] - 1]
    case "<":
      nextCoord[1] -= 1

  boxesPushed[tuple(nextCoord)] = (mapArray[tuple(coord)], tuple(coord))

  if mapArray[tuple(nextCoord)] in [".", "O", "[", "]"]:
    if mapArray[tuple(nextCoord)] != ".":
      pushable.append(push_boxes(mapArray, direction, nextCoord, boxesPushed))
    else:
      pushable.append(True)
  else:
    pushable.append(False)
  if not nextCoord2 is None:
    if mapArray[tuple(nextCoord2)] in [".", "O", "[", "]"]:
      if mapArray[tuple(nextCoord2)] != ".":
        pushable.append(push_boxes(mapArray, direction, nextCoord2, boxesPushed))
      else:
        pushable.append(True)
    else:
      pushable.append(False)

  return all(pushable)

def read_instruction(mapArray, moves, coord):
  for move in moves:
    boxesPushed = {}
    
    if push_boxes(mapArray, move, coord, boxesPushed):
      edited = set()
      for boxPushed in boxesPushed:
        pushItem = boxesPushed[boxPushed][0]
        mapArray[boxPushed] = pushItem
        if pushItem == "@":
          coord = list(boxPushed)
        preCoord = boxesPushed[boxPushed][1]
        edited.add(boxPushed)
        if not preCoord in edited:
          mapArray[preCoord] = "."

def read_map(inputMap):
  mapMove = inputMap.split("\n\n")
  rows = mapMove[0].split("\n")
  rows2 = []

  robotCoord = None
  robot2Coord = None

  for y, row in enumerate(rows):
    rows[y] = list(row)
    rows2.append([])
    for x, col in enumerate(row):
      if col == "#":
        rows2[y].extend(list("##"))
      elif col == "O":
        rows2[y].extend(list("[]"))
      elif col == ".":
        rows2[y].extend(list(".."))
      elif col == "@":
        rows2[y].extend(list("@."))
        robotCoord = [y, x]
        robot2Coord = [y, x * 2]

  mapAsArray = np.array(rows)
  map2AsArray = np.array(rows2)

  read_instruction(mapAsArray, mapMove[1], copy.deepcopy(robotCoord))
  read_instruction(map2AsArray, mapMove[1], copy.deepcopy(robot2Coord))

  boxCoordSum = 0
  box2CoordSum = 0

  for idx, ele in np.ndenumerate(mapAsArray):
    if ele == "O":
      boxCoordSum += (idx[0] * 100) + idx[1]

  for idx, ele in np.ndenumerate(map2AsArray):
    if ele == "[":
      box2CoordSum += (idx[0] * 100) + idx[1]

  print(map2AsArray)

  return boxCoordSum, box2CoordSum

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day15input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_map(inputFile.read()))