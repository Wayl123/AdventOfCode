import os
import hashlib

def get_password(key):
  num = 1

  while True:
    hash = hashlib.md5((key + str(num)).encode())
    
    if hash.hexdigest()[:6] == "000000":
      break
    
    num += 1

  return num

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day4input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_password(inputFile.read()))

