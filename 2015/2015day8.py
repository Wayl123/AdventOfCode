import os
import numpy as np
import ast

def get_string_len_value(string):
  return len(string), len(ast.literal_eval(string)), len(repr(string).replace("\"", "\\\""))

def get_string_len_diff(input):
  strList = list(map(str.strip, input.split("\n")))

  sum = [0, 0, 0]

  for string in strList:
    sum = np.add(sum, get_string_len_value(string))

  return sum[0] - sum[1], sum[2] - sum[0]

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day8input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_string_len_diff(inputFile.read()))