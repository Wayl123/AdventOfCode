import os
import math
import numpy as np

def get_surface_area_with_slack(dimension):
  d = list(map(int, dimension.split("x")))

  #wrapping
  s1 = d[0]*d[1]
  s2 = d[1]*d[2]
  s3 = d[0]*d[2]

  slack = min(s1, s2, s3)

  #ribbon
  bow = math.prod(d)

  d.remove(max(d))

  return 2*sum([s1, s2, s3]) + slack, 2*sum(d) + bow

def get_sum_of_multiple_box(dimensions):
  result = [0, 0]

  boxes = dimensions.split("\n")

  for dimension in boxes:
    result = np.add(result, get_surface_area_with_slack(dimension))

  return result

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day2input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_sum_of_multiple_box(inputFile.read()))