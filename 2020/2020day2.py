import os
import numpy as np

def is_valid_password(password):
  reqAndPass = password.split(": ")
  charCheck = reqAndPass[0].split()
  charLimit = list(map(int, charCheck[0].split("-")))

  oldCheck = True

  charCount = 0

  for c in reqAndPass[1]:
    if c == charCheck[1]:
      charCount += 1
    if charCount > charLimit[1]:
      oldCheck = False
      break
    
  return charCount >= charLimit[0] if oldCheck else False, (reqAndPass[1][charLimit[0]-1] == charCheck[1]) ^ (reqAndPass[1][charLimit[1]-1] == charCheck[1])

def get_num_of_valid_password(input):
  passwords = input.split("\n")

  validCount = [0, 0]

  for password in passwords:
    validCount = np.add(validCount, list(map(int, is_valid_password(password))))

  return validCount

inputFilePath = os.path.dirname(__file__) + "\\input\\2020day2input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_num_of_valid_password(inputFile.read()))