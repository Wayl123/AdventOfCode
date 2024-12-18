import os

lights1 = [[False for i in range(1000)] for j in range(1000)]
lights2 = [[0 for i in range(1000)] for j in range(1000)]

def execute_instruction(cmd, startCoord, endCoord):
  start = list(map(int, startCoord.split(",")))
  end = list(map(int, endCoord.split(",")))

  for x in range(start[0], end[0]+1):
    for y in range(start[1], end[1]+1):
      match cmd:
        case "turn on":
          lights1[x][y] = True
          lights2[x][y] += 1
        case "toggle":
          lights1[x][y] = not lights1[x][y]
          lights2[x][y] += 2
        case "turn off":
          lights1[x][y] = False
          if lights2[x][y] > 0: lights2[x][y] -= 1

def read_instruction(input):
  instrList = input.split("\n")

  for instr in instrList:
    splitInstr = instr.split()

    if splitInstr[0] == "turn":
      splitInstr[0:2] = [" ".join(splitInstr[0:2])]

    execute_instruction(splitInstr[0], splitInstr[1], splitInstr[3])

  return sum(map(sum, lights1)), sum(map(sum, lights2))

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day6input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_instruction(inputFile.read()))