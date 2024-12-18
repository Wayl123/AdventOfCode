import os
import re
import math
from functools import reduce
import matplotlib.pyplot as plt

# spaceSize = (7, 11)
spaceSize = (103, 101)
secondsElapsed = 100
robotInit = []
quadrant = {1: [], 2: [], 3: [], 4: [], 5: []}

def get_robot_final_pos(posX, posY, vX, vY):
  global robotInit, quadrant

  robotInit.append([[posY, posX], [vY, vX]])

  finalPosX = (posX + (vX * secondsElapsed)) % spaceSize[1]
  finalPosY = (posY + (vY * secondsElapsed)) % spaceSize[0]

  leftRight = finalPosX < math.floor(spaceSize[1] / 2)
  upDown = finalPosY < math.floor(spaceSize[0] / 2)
  middle = finalPosX == math.floor(spaceSize[1] / 2) or finalPosY == math.floor(spaceSize[0] / 2)

  if middle:
    group = 5
  else:
    if leftRight:
      group = 1 if upDown else 3
    else:
      group = 2 if upDown else 4
    
  quadrant[group].append((finalPosY, finalPosX))

def iterate_next(pos, v, space):
  return (pos + v) % space

def find_easter_egg():
  global robotInit

  notFound = True

  seconds = 0
  totalRobot = len(robotInit)
  preDev = None

  while notFound:
    seconds += 1
    for robot in robotInit:
      robot[0] = list(map(iterate_next, robot[0], robot[1], spaceSize))

    yxSum = [sum(x) for x in zip(*next(zip(*robotInit)))]
    yxMean = [x / totalRobot for x in yxSum]
    yxVarSum = [sum(map(lambda a: (a - yxMean[i]) ** 2, x)) for i, x in enumerate(zip(*next(zip(*robotInit))))]
    yxDev = [math.sqrt(x / totalRobot) for x in yxVarSum]

    if (not preDev is None and (preDev[0] - yxDev[0] >= 5 and preDev[0] - yxDev[1] >= 5)) or seconds >= 10000:
      notFound = False

    preDev = yxDev

  for robot in robotInit:
    plt.plot(robot[0][1], spaceSize[0] - robot[0][0], 'o')
  plt.show()

  return seconds

def get_all_robot(input):
  robots = input.split("\n")

  for robot in robots:
    posVelo = re.findall(r"-?\d+", robot)
    get_robot_final_pos(*list(map(int, posVelo)))

  safetyFactor = 1
  for n in range(1, 5):
    safetyFactor *= len(quadrant[n])

  return safetyFactor, find_easter_egg()

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day14input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(get_all_robot(inputFile.read()))