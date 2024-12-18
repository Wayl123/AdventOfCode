import os
import copy
from functools import reduce

def concat(num1, num2):
  return int(f"{num1}{num2}")

def try_operators(num_list, target_num):
  if len(num_list) == 2:
    q1Result = num_list[0] + num_list[1] == target_num or num_list[0] * num_list[1] == target_num
    q2Result = q1Result or concat(num_list[0], num_list[1]) == target_num
    return q1Result, q2Result
  else:
    q1Result1, q1Result2, q2Result1, q2Result2, q2Result3 = (False,) * 5

    if num_list[0] + num_list[1] <= target_num:
      reduce_list = copy.deepcopy(num_list)
      reduce_list[0 : 2] = [reduce(lambda i, j: i + j, reduce_list[0 : 2])]
      q1Result1, q2Result1 = try_operators(reduce_list, target_num)
    if num_list[0] * num_list[1] <= target_num:
      reduce_list = copy.deepcopy(num_list)
      reduce_list[0 : 2] = [reduce(lambda i, j: i * j, reduce_list[0 : 2])]
      q1Result2, q2Result2 = try_operators(reduce_list, target_num)
    if concat(num_list[0], num_list[1]) <= target_num:
      reduce_list = copy.deepcopy(num_list)
      reduce_list[0 : 2] = [reduce(lambda i, j: concat(i, j), reduce_list[0 : 2])]
      _, q2Result3 = try_operators(reduce_list, target_num)

    return q1Result1 or q1Result2, q2Result1 or q2Result2 or q2Result3
  
def sum_correct_equation(input):
  equations = input.split("\n")

  q1Sum, q2Sum = 0, 0

  for equation in equations:
    targetAndNum = equation.split(": ")

    target_num = int(targetAndNum[0])
    num_list = list(map(int, targetAndNum[1].split()))

    results = try_operators(num_list, target_num)
    if results[0]:
      q1Sum += target_num
    if results[1]:
      q2Sum += target_num

  return q1Sum, q2Sum

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day7input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(sum_correct_equation(inputFile.read()))