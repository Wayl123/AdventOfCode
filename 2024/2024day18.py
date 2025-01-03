import os
import numpy as np
import heapq
import matplotlib.pyplot as plt

closedGrid = []
gridShape = (71, 71)
startCoord = (0, 0)
endCoord = (gridShape[0] - 1, gridShape[1] - 1)
simulateAmount = 1024

def is_in_grid(coord):
  return (coord[0] >= 0) and (coord[0] < gridShape[0]) and (coord[1] >= 0) and (coord[1] < gridShape[1])

def calculate_h_value(coord, goal):
  return ((coord[0] - goal[0]) ** 2 + (coord[1] - goal[1]) ** 2) ** 0.5

def find_path_min_score(start, goal, closed):
  visitedGrid = {}
  visitedGrid[start] = (0, 0, 0, start)
  
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

      if is_in_grid(nextCoord) and not tuple(nextCoord) in closed:
        score = visitedGrid[tuple(coord)][1] + 1
        heuristic = calculate_h_value(tuple(nextCoord), goal)
        totalScore = score + heuristic

        if not tuple(nextCoord) in visitedGrid or visitedGrid[tuple(nextCoord)][0] > totalScore:
          visitedGrid[tuple(nextCoord)] = (totalScore, score, heuristic, coord)
          heapq.heappush(openList, (totalScore, tuple(nextCoord)))

        if tuple(nextCoord) == goal:
          return visitedGrid
        
def trace_path(start, goal, closed, grid):
  pathList = {goal}

  curCoord = goal

  while curCoord != start:
    curCoord = grid[curCoord][3]
    pathList.add(curCoord)

  for coord in closed:
    plt.plot(coord[1], gridShape[0] - coord[0], 'x')
  for coord in pathList:
    plt.plot(coord[1], gridShape[0] - coord[0], 'o')
  plt.show()

  return len(pathList) - 1

def find_first_failure():
  low = 0
  high = len(closedGrid) - 1
  mid = 0

  while low < high:
    mid = (high + low) // 2
    
    if find_path_min_score(startCoord, endCoord, closedGrid[:mid]):
      low = mid + 1
    else:
      high = mid

  mid = (high + low) // 2

  return closedGrid[mid-1][::-1], mid
          
def read_map(input):
  global closedGrid

  blockedCoords = input.split("\n")

  for blockedCoord in blockedCoords:
    coord = list(map(int, blockedCoord.split(",")))
    closedGrid.append((coord[1], coord[0]))

  visitedGrid = find_path_min_score(startCoord, endCoord, closedGrid[:simulateAmount])

  return trace_path(startCoord, endCoord, closedGrid[:simulateAmount], visitedGrid) if visitedGrid else "Solution not found", find_first_failure()

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day18input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_map(inputFile.read()))