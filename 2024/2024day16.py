import os
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

visitedMinGridCost = {}

def find_path_min_score(mapArray, startcoord, startDir, goal):
  global visitedMinGridCost
  
  openList = deque([])
  openList.append((startcoord, startDir, 0))

  while len(openList) > 0:
    checkGrid = openList.popleft()

    coord = checkGrid[0]
    curDir = checkGrid[1]

    nextCoord = [0, 0]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for dir in directions:
      nextCoord[0] = coord[0] + dir[0]
      nextCoord[1] = coord[1] + dir[1]
      tempScore = checkGrid[2]

      if mapArray[tuple(nextCoord)] in [".", "S", "E"]:
        if curDir != dir:
          tempScore += 1001
        else:
          tempScore += 1
        
        if not tuple(nextCoord) in visitedMinGridCost:
          visitedMinGridCost[tuple(nextCoord)] = [(tempScore, dir, coord, curDir)]
        else:
          minScore = min(next(zip(*visitedMinGridCost[tuple(nextCoord)])))
          path = [minPath for minPath in visitedMinGridCost[tuple(nextCoord)] if minPath[0] == minScore][0]

          if dir == path[1]:
            if tempScore < path[0]:
              visitedMinGridCost[tuple(nextCoord)] = [(tempScore, dir, coord, curDir)]
            elif tempScore == path[0]:
              visitedMinGridCost[tuple(nextCoord)].append((tempScore, dir, coord, curDir))
              continue
            else:
              continue
          elif dir != path[1] and tempScore <= path[0] + 1000:
            if tempScore < path[0] - 1000:
              visitedMinGridCost[tuple(nextCoord)] = [(tempScore, dir, coord, curDir)]
            else:
              visitedMinGridCost[tuple(nextCoord)].append((tempScore, dir, coord, curDir))
          else:
            continue

        if tuple(nextCoord) != goal:
          openList.append((tuple(nextCoord), dir, tempScore))

def trace_path(mapArrayShape, goal):
  minScore = min(next(zip(*visitedMinGridCost[goal])))
  minList = deque([path for path in visitedMinGridCost[goal] if path[0] == minScore])

  minPathCoords = {goal}

  while len(minList) > 0:
    checkPath = minList.popleft()
    if checkPath[2]:
      minPathCoords.add(checkPath[2])
      minPathNext = [path for path in visitedMinGridCost[checkPath[2]] if path[1] == checkPath[3]]
      minPathNextMinScore = min(next(zip(*minPathNext)))
      minList.extend([path for path in minPathNext if path[0] == minPathNextMinScore])

  for coord in minPathCoords:
    plt.plot(coord[1], mapArrayShape[0] - coord[0], 'o')
  plt.show()

  return minScore, len(minPathCoords)
          
def read_map(inputMap):
  rows = inputMap.split("\n")

  startCoord = None
  endCoord = None
  startDir = (0, 1)

  for y, row in enumerate(rows):
    rows[y] = list(row)
    for x, col in enumerate(row):
      if col == "S":
        startCoord = (y, x)
      elif col == "E":
        endCoord = (y, x)

  mapAsArray = np.array(rows)

  visitedMinGridCost[startCoord] = [(0, startDir, None, None)]

  find_path_min_score(mapAsArray, startCoord, startDir, endCoord)

  if endCoord in visitedMinGridCost:
    return trace_path(mapAsArray.shape, endCoord)
  else:
    return "Solution not found"

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day16input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_map(inputFile.read()))