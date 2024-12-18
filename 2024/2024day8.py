import os
import numpy as np

signalCoord = {}
q1AntennaCoord = set()
q2AntennaCoord = set()

def find_antenna(bound):
  global antennaCoord

  for signal in signalCoord:
    signalAmount = len(signalCoord[signal])
    if signalAmount >= 2:
      for i in range(signalAmount - 1):
        signal1 = signalCoord[signal][i]
        for j in range(i + 1, signalAmount):
          signal2 = signalCoord[signal][j]

          dist = (signal2[0] - signal1[0], signal2[1] - signal1[1])

          if 0 <= signal1[0] - dist[0] < bound[0] and 0 <= signal1[1] - dist[1] < bound[1]:
            q1AntennaCoord.add((signal1[0] - dist[0], signal1[1] - dist[1]))

          if 0 <= signal2[0] + dist[0] < bound[0] and 0 <= signal2[1] + dist[1] < bound[1]:
            q1AntennaCoord.add((signal2[0] + dist[0], signal2[1] + dist[1]))

          n = 0
          while 0 <= signal1[0] + dist[0] * n < bound[0] and 0 <= signal1[1] + dist[1] * n < bound[1]:
            q2AntennaCoord.add((signal1[0] + dist[0] * n, signal1[1] + dist[1] * n))
            n += 1

          n = -1
          while 0 <= signal1[0] + dist[0] * n < bound[0] and 0 <= signal1[1] + dist[1] * n < bound[1]:
            q2AntennaCoord.add((signal1[0] + dist[0] * n, signal1[1] + dist[1] * n))
            n -= 1

def read_map(map):
  global signalCoord

  rows = map.split("\n")

  for y, row in enumerate(rows):
    rows[y] = list(row)
    for x, col in enumerate(row):
      if col != ".":
        if not col in signalCoord:
          signalCoord[col] = []
        signalCoord[col].append((y, x))

  mapAsArray = np.array(rows)

  find_antenna(mapAsArray.shape)

  return len(q1AntennaCoord), len(q2AntennaCoord)

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day8input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_map(inputFile.read()))