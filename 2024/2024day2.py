import os
import copy

def check_safety(report, problemDamper = False):
  ascFlag = None
  removeIndex = None

  prevEle = report[0]

  for prevIndex, element in enumerate(report[1:]):
    diff = prevEle - element

    if abs(diff) > 3 or abs(diff) < 1 or (not ascFlag is None and ascFlag * diff < 0):
      if problemDamper:
        problemDamper = False
        removeIndex = prevIndex
        continue
      else:
        if removeIndex is None:
          return False
        else:
          report2 = copy.deepcopy(report)
          report2.pop(removeIndex)
          return check_safety(report2) or (removeIndex == 1 and check_safety(report[1:]))
      
    if ascFlag is None:
      ascFlag = diff
    
    prevEle = element

  return True

def read_report(input):
  reports = input.split("\n")

  safeCount = 0
  safeCountDamp = 0

  for report in reports:
    if check_safety(list(map(int, report.split()))):
      safeCount += 1
    if check_safety(list(map(int, report.split())), True):
      safeCountDamp += 1

  return safeCount, safeCountDamp

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day2input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_report(inputFile.read()))