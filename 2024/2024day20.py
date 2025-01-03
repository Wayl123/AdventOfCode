import os
import numpy as np
import heapq
import matplotlib.pyplot as plt

gridShape = (0, 0)

def is_in_grid(coord):
  return (coord[0] >= 0) and (coord[0] < gridShape[0]) and (coord[1] >= 0) and (coord[1] < gridShape[1])

def find_path_min_score(mapArray, start, goal):
  visitedGrid = {}
  visitedGrid[start] = (0, start)
  
  openList = []
  heapq.heappush(openList, (0, start))

  while len(openList) > 0:
    checkGrid = heapq.heappop(openList)

    coord = checkGrid[1]

    nextCoord = [0, 0]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for dir in directions:
      nextCoord[0] = coord[0] + dir[0]
      nextCoord[1] = coord[1] + dir[1]

      if is_in_grid(nextCoord) and mapArray[tuple(nextCoord)] != "#":
        score = visitedGrid[tuple(coord)][0] + 1

        if not tuple(nextCoord) in visitedGrid or visitedGrid[tuple(nextCoord)][0] > score:
          visitedGrid[tuple(nextCoord)] = (score, coord)
          heapq.heappush(openList, (score, tuple(nextCoord)))

        if tuple(nextCoord) == goal:
          return visitedGrid
        
def trace_path(start, goal, grid):
  pathList = {goal}

  curCoord = goal

  while curCoord != start:
    curCoord = grid[curCoord][1]
    pathList.add(curCoord)

  for coord in pathList:
    plt.plot(coord[1], gridShape[0] - coord[0], 'o')
    # plt.annotate(grid[coord][0], (coord[1], gridShape[0] - coord[0] + 0.2))
  plt.show()

  return len(pathList) - 1

def find_shortcut(grid):
  q1Shortcuts = {}
  q2Shortcuts = {}

  direction = [(-2, 0), (0, 2), (2, 0), (0, -2)]
  emptyMap = np.empty(gridShape)

  checkedCoord = set()

  for coord in grid:
    nextCoord = [0, 0]
    for dir in direction:
      nextCoord[0] = coord[0] + dir[0]
      nextCoord[1] = coord[1] + dir[1]

      if tuple(nextCoord) in grid:
        cutTime = grid[tuple(nextCoord)][0] - (grid[coord][0] + 2)
        if cutTime > 0:
          if not cutTime in q1Shortcuts:
            q1Shortcuts[cutTime] = 0
          q1Shortcuts[cutTime] += 1

    checkedCoord.add(coord)
    subGrid = {c : grid[c] for c in grid if not c in checkedCoord}

    for otherCoord in subGrid:
      coordDist = abs(otherCoord[0] - coord[0]) + abs(otherCoord[1] - coord[1])
      if coordDist <= 20:
        cutTime = grid[otherCoord][0] - (grid[coord][0] + coordDist)
        if cutTime >= 50:
          if not cutTime in q2Shortcuts:
            q2Shortcuts[cutTime] = 0
          q2Shortcuts[cutTime] += 1

  return q1Shortcuts, q2Shortcuts

def read_map(inputMap):
  global gridShape

  rows = inputMap.split("\n")

  startCoord = None
  endCoord = None

  for y, row in enumerate(rows):
    rows[y] = list(row)
    for x, col in enumerate(row):
      if col == "S":
        startCoord = (y, x)
      elif col == "E":
        endCoord = (y, x)

  mapAsArray = np.array(rows)
  gridShape = mapAsArray.shape

  visitedGrid = find_path_min_score(mapAsArray, startCoord, endCoord)
  trace_path(startCoord, endCoord, visitedGrid)
  q1Shortcuts, q2Shortcuts = find_shortcut(visitedGrid)

  return sum(q1Shortcuts[shortcut] for shortcut in q1Shortcuts if shortcut >= 100), sum(q2Shortcuts[shortcut] for shortcut in q2Shortcuts if shortcut >= 100)

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day20input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_map(inputFile.read()))