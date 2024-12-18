import os
import math

def two_sum(arr, target):
  l = 0
  r = len(arr) - 1

  while l < r:
    sum = arr[l] + arr[r]
    
    if sum == target:
      return arr[l], arr[r]
    elif sum < target:
      l += 1
    else:
      r -= 1

  return False

def three_sum(arr, target):
  for i in range(len(arr)):
    subTarget = target-arr[i]

    result = two_sum(arr, subTarget)
    if result:
      return result + (arr[i],)
    
  return False

def input_to_array(input):
  target = 2020

  arr = list(map(int, input.split("\n")))
  arr.sort()
  return math.prod(two_sum(arr, target)), math.prod(three_sum(arr, target))

inputFilePath = os.path.dirname(__file__) + "\\input\\2020day1input.txt"
with open(inputFilePath, "r") as inputFile:
  print(input_to_array(inputFile.read()))