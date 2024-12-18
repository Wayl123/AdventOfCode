import os
import re
import numpy as np

def get_min_cost(ax, ay, bx, by, x, y):
  # Cramer's rule
  b, bmod = divmod((ay * x) - (ax * y), (ay * bx) - (ax * by))
  a, amod = divmod(x - (b * bx), ax)

  x2 = x + 10000000000000
  y2 = y + 10000000000000

  b2, b2mod = divmod((ay * x2) - (ax * y2), (ay * bx) - (ax * by))
  a2, a2mod = divmod(x2 - (b2 * bx), ax)

  return 0 if bmod or amod else (3 * a) + b, 0 if b2mod or a2mod else (3 * a2) + b2

def get_all_prize_cost(input):
  games = input.split("\n\n")

  totalToken = [0, 0]

  for game in games:
    num = re.findall(r"\d+", game)
    totalToken = np.add(totalToken, get_min_cost(*list(map(int, num))))

  return totalToken

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day13input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(*get_all_prize_cost(inputFile.read()))