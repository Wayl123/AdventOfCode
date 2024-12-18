import os
import numpy as np

def read_and_get_distance(input):
  elements = input.split("\n")

  list1 = []
  list2 = []
  freqDict = {}

  for element in elements:
    separateElement = list(map(int, element.split()))
    
    list1.append(separateElement[0])
    list2.append(separateElement[1])
    
    if not separateElement[1] in freqDict:
      freqDict[separateElement[1]] = 0
    freqDict[separateElement[1]] += 1

  list1.sort()
  list2.sort()

  return np.sum(np.abs(np.subtract(list1, list2))), np.sum([freqDict[x] * x for x in list1 if x in freqDict])

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day1input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_and_get_distance(inputFile.read()))