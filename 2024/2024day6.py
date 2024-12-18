import os
import numpy as np
import collections
import copy

cratesCoord = set()
loopCratesCoord = {"^": {}, ">": {}, "v": {}, "<": {}} # {MoveDir: {col/row coord: crates coord}}

def get_distinct_position_count(inputMap, guardCoord, guardDir, checkLoop = False):
  global cratesCoord, loopCratesCoord

  guardLeft = False

  dirList = ["^", ">", "v", "<"]
  dirIndex = dirList.index(guardDir)

  inputMap[guardCoord[0], guardCoord[1]] = "X"
  distPos = 1
  loopCount = 0

  while not guardLeft:
    loopCrateDir = dirList[(dirIndex + 3) % len(dirList)]

    loopCrateList = []

    match(guardDir):
      case "^":
        crateList = [coord[0] for coord in cratesCoord if coord[1] == guardCoord[1] and coord[0] < guardCoord[0]]
        if not crateList:
          guardLeft = True
          closest = -1
        else:
          closest = max(crateList)

        up = closest
        down = guardCoord[0]
        left = guardCoord[1] - 1
        right = guardCoord[1] + 1

        low = up
        high = down
        current = guardCoord[1]

        # Bruteforce check
        if checkLoop:
          for n in range(low + 1, high):
            if inputMap[n, current] != "X":
              cratesCoordCopy = copy.deepcopy(cratesCoord)
              loopCratesCoordCopy = copy.deepcopy(loopCratesCoord)
              mapCopy = copy.deepcopy(inputMap)

              mapCopy[n, current] = "#"
              cratesCoord.add((n, current))
              looping, _ = get_distinct_position_count(mapCopy, copy.deepcopy(guardCoord), copy.deepcopy(guardDir))

              if looping < 0:
                loopCount += 1

              cratesCoord = cratesCoordCopy
              loopCratesCoord = loopCratesCoordCopy

        # All crate beside the path will cause loop if approached <
        if guardCoord[1] > 0:
          loopCratePos = guardCoord[1] - 1
          loopCrateList = [coord[0] for coord in cratesCoord if coord[1] == loopCratePos and closest < coord[0] <= guardCoord[0]]

        guardCoord[0] = closest + 1

      case ">":
        crateList = [coord[1] for coord in cratesCoord if coord[0] == guardCoord[0] and coord[1] > guardCoord[1]]
        if not crateList:
          guardLeft = True
          closest = inputMap.shape[1]
        else:
          closest = min(crateList)

        up = guardCoord[0] - 1
        down = guardCoord[0] + 1
        left = guardCoord[1]
        right = closest

        low = left
        high = right
        current = guardCoord[0]

        # Bruteforce check
        if checkLoop:
          for n in range(low + 1, high):
            if inputMap[current, n] != "X":
              cratesCoordCopy = copy.deepcopy(cratesCoord)
              loopCratesCoordCopy = copy.deepcopy(loopCratesCoord)
              mapCopy = copy.deepcopy(inputMap)

              mapCopy[current, n] = "#"
              cratesCoord.add((current, n))
              looping, _ = get_distinct_position_count(mapCopy, copy.deepcopy(guardCoord), copy.deepcopy(guardDir))

              if looping < 0:
                loopCount += 1

              cratesCoord = cratesCoordCopy
              loopCratesCoord = loopCratesCoordCopy

        # All crate beside the path will cause loop if approached ^
        if guardCoord[0] > 0:
          loopCratePos = guardCoord[0] - 1
          loopCrateList = [coord[1] for coord in cratesCoord if coord[0] == loopCratePos and closest > coord[1] >= guardCoord[1]]

        guardCoord[1] = closest - 1

      case "v":
        crateList = [coord[0] for coord in cratesCoord if coord[1] == guardCoord[1] and coord[0] > guardCoord[0]]
        if not crateList:
          guardLeft = True
          closest = inputMap.shape[0]
        else:
          closest = min(crateList)

        up = guardCoord[0]
        down = closest
        left = guardCoord[1] - 1
        right = guardCoord[1] + 1

        low = up
        high = down
        current = guardCoord[1]

        # Bruteforce check
        if checkLoop:
          for n in range(low + 1, high):
            if inputMap[n, current] != "X":
              cratesCoordCopy = copy.deepcopy(cratesCoord)
              loopCratesCoordCopy = copy.deepcopy(loopCratesCoord)
              mapCopy = copy.deepcopy(inputMap)

              mapCopy[n, current] = "#"
              cratesCoord.add((n, current))
              looping, _ = get_distinct_position_count(mapCopy, copy.deepcopy(guardCoord), copy.deepcopy(guardDir))

              if looping < 0:
                loopCount += 1

              cratesCoord = cratesCoordCopy
              loopCratesCoord = loopCratesCoordCopy

        # All crate beside the path will cause loop if approached >
        if guardCoord[1] < inputMap.shape[1] - 1:
          loopCratePos = guardCoord[1] + 1
          loopCrateList = [coord[0] for coord in cratesCoord if coord[1] == loopCratePos and closest > coord[0] >= guardCoord[0]]

        guardCoord[0] = closest - 1

      case "<":
        crateList = [coord[1] for coord in cratesCoord if coord[0] == guardCoord[0] and coord[1] < guardCoord[1]]
        if not crateList:
          guardLeft = True
          closest = -1
        else:
          closest = max(crateList)

        up = guardCoord[0] - 1
        down = guardCoord[0] + 1
        left = closest
        right = guardCoord[1]

        low = left
        high = right
        current = guardCoord[0]

        # Bruteforce check
        if checkLoop:
          for n in range(low + 1, high):
            if inputMap[current, n] != "X":
              cratesCoordCopy = copy.deepcopy(cratesCoord)
              loopCratesCoordCopy = copy.deepcopy(loopCratesCoord)
              mapCopy = copy.deepcopy(inputMap)

              mapCopy[current, n] = "#"
              cratesCoord.add((current, n))
              looping, _ = get_distinct_position_count(mapCopy, copy.deepcopy(guardCoord), copy.deepcopy(guardDir))

              if looping < 0:
                loopCount += 1

              cratesCoord = cratesCoordCopy
              loopCratesCoord = loopCratesCoordCopy

        # All crate beside the path will cause loop if approached v
        if guardCoord[0] < inputMap.shape[0] - 1:
          loopCratePos = guardCoord[0] + 1
          loopCrateList = [coord[1] for coord in cratesCoord if coord[0] == loopCratePos and closest < coord[1] <= guardCoord[1]]

        guardCoord[1] = closest + 1

    # If looping
    if current in loopCratesCoord[guardDir] and closest in loopCratesCoord[guardDir][current]:
      return -1, 1

    # Add loop crate list to dictionary
    for loopCrate in loopCrateList:
      if not loopCrate in loopCratesCoord[loopCrateDir]:
        loopCratesCoord[loopCrateDir][loopCrate] = set()
      loopCratesCoord[loopCrateDir][loopCrate].add(loopCratePos)

    # Draw X on traversed path
    repeatCount = collections.Counter(inputMap[up + 1 : down, left + 1 : right].flatten())["X"]
    inputMap[up + 1 : down, left + 1 : right] = "X"
    distPos += abs(down - up) + abs(right - left) - 3 - repeatCount # -1 to not count starting pos, -2 for the other coordinate as we are not moving in that direction
   
    dirIndex = (dirIndex + 1) % len(dirList)
    guardDir = dirList[dirIndex]

  return distPos, loopCount

def read_map(inputMap):
  global cratesCoord

  rows = inputMap.split("\n")

  guardCoord = None
  guardDir = None

  for y, row in enumerate(rows):
    rows[y] = list(row)
    for x, col in enumerate(row):
      if col == "#":
        cratesCoord.add((y, x))
      if guardCoord is None:
        if col in ["^", ">", "v", "<"]:
          guardCoord = [y, x]
          guardDir = col

  mapAsArray = np.array(rows)

  return get_distinct_position_count(mapAsArray, guardCoord, guardDir, True)

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day6input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(read_map(inputFile.read()))