import os
import numpy as np
from functools import cache

trailheadCoord = set()
inputMapAsArray = []

@cache
def find_next_height(coord, height):
  trailend = set()
  rating = 0

  if height == 9:
    trailend.add(coord)
    rating = 1
  else:
    if coord[0] - 1 >= 0 and inputMapAsArray[coord[0] - 1, coord[1]] == height + 1:
      result = find_next_height((coord[0] - 1, coord[1]), height + 1)
      trailend.update(result[0])
      rating += result[1]
    if coord[1] + 1 < inputMapAsArray.shape[1] and inputMapAsArray[coord[0], coord[1] + 1] == height + 1:
      result = find_next_height((coord[0], coord[1] + 1), height + 1)
      trailend.update(result[0])
      rating += result[1]
    if coord[0] + 1 < inputMapAsArray.shape[0] and inputMapAsArray[coord[0] + 1, coord[1]] == height + 1:
      result = find_next_height((coord[0] + 1, coord[1]), height + 1)
      trailend.update(result[0])
      rating += result[1]
    if coord[1] - 1 >= 0 and inputMapAsArray[coord[0], coord[1] - 1] == height + 1:
      result = find_next_height((coord[0], coord[1] - 1), height + 1)
      trailend.update(result[0])
      rating += result[1]

  return trailend, rating

def read_map(inputMap):
  global trailheadCoord, inputMapAsArray

  rows = inputMap.split("\n")

  for y, row in enumerate(rows):
    rows[y] = list(map(int, list(row)))
    for x, col in enumerate(row):
      if col == "0":
        trailheadCoord.add((y, x))

  inputMapAsArray = np.array(rows)

  trailScore = 0
  trailRating = 0
  
  for trailhead in trailheadCoord:
    result = find_next_height(trailhead, 0)
    trailScore += len(result[0])
    trailRating += result[1]

  return trailScore, trailRating

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day10input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_map(inputFile.read()))