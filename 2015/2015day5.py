import os
import numpy as np

def is_vowel(char):
  return char in ("a", "e", "i", "o", "u")

def is_bad_string(stringPair):
  return stringPair in ("ab", "cd", "pq", "xy")

def is_nice_string(string):
  vowelCount = 0
  doubleLetterFlag = False
  badStringFlag = False
  
  pairDict = set()
  pairRepeatFlag = False
  tempPairRepeatFlag = False
  stringPair = ""
  previousPair = ""
  gapDoubleLetterFlag = False

  for index in range(len(string)):
    if is_vowel(string[index]):
      vowelCount += 1

    if index >= 1:
      stringPair = string[index - 1] + string[index]

      if not doubleLetterFlag and string[index - 1] == string[index]:
        doubleLetterFlag = True

      if is_bad_string(stringPair):
        badStringFlag = True

      if stringPair in pairDict:
        tempPairRepeatFlag = True
      else:
        pairDict.add(stringPair)
      
    if index >= 2:
      if not gapDoubleLetterFlag and string[index - 2] == string[index]:
        gapDoubleLetterFlag = True

      if tempPairRepeatFlag and previousPair == stringPair:
        tempPairRepeatFlag = False
        previousPair = 0

    if tempPairRepeatFlag:
      pairRepeatFlag = True
      tempPairRepeatFlag = False
    
    if isinstance(previousPair, str):
      previousPair = stringPair
    else:
      previousPair = ""
    
  return vowelCount >= 3 and doubleLetterFlag and not badStringFlag, pairRepeatFlag and gapDoubleLetterFlag

def get_nice_string_count(input):
  stringList = input.split("\n")

  count = [0, 0]

  for string in stringList:
    count = np.add(count, list(map(int, is_nice_string(string))))

  return count

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day5input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_nice_string_count(inputFile.read()))