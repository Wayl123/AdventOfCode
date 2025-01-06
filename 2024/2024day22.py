import os
from functools import cache, reduce
from collections import deque, Counter
import operator

def mix_number(num1, num2):
  return num1 ^ num2

def prune_number(num):
  return num & ((2 ** 24) - 1)

@cache
def calculate_next_secret(num):
  num = prune_number(mix_number(num, num << 6))
  num = prune_number(mix_number(num, num >> 5))
  num = prune_number(mix_number(num, num << 11))

  return num, num % 10

def calculate_secret_and_seq(num, times = 1):
  seq = deque(maxlen = 4)
  seqDict = {}
  prePrice = num % 10

  for _ in range(times):
    num, price = calculate_next_secret(num)

    diff = price - prePrice
    seq.append(diff)

    if len(seq) == 4 and not tuple(seq) in seqDict:
      seqDict[tuple(seq)] = price

    prePrice = price

  return num, seqDict

def sum_secret_num(input):
  secretNums = list(map(int, input.split("\n")))

  times = 2000
  secretSum = 0
  seqDicts = []

  for secretNum in secretNums:
    num, seqDict = calculate_secret_and_seq(secretNum, times)
    seqDicts.append(seqDict)
    secretSum += num

  seqDictSum = dict(reduce(operator.add, map(Counter, seqDicts)))
  maxSeq = max(zip(seqDictSum.values(), seqDictSum.keys()))

  return secretSum, maxSeq

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day22input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(sum_secret_num(inputFile.read()))