import os
import math

def get_xmas_count(input):
  word_rows = input.split("\n")

  word_search = []
  for row in word_rows:
    word_search.append(list(row))

  x_max = len(word_search[0])
  y_max = len(word_search)

  xmas_count = 0
  x_mas_count = 0
  
  for y in range(y_max):
    for x in range(x_max):
      if word_search[y][x] == "X":
        searchable = [x + 3 < x_max, y + 3 < y_max, x - 3 >= 0, y - 3 >= 0]
        
        for search in range(8):
          side_search = [round(math.sin(search * (math.pi / 4))), round(math.cos(search * (math.pi / 4)))]

          if searchable[math.floor(search / 2) % 4] and searchable[math.ceil(search / 2) % 4]:
            if (word_search[y + (side_search[0] * 1)][x + (side_search[1] * 1)] == "M" 
              and word_search[y + (side_search[0] * 2)][x + (side_search[1] * 2)] == "A" 
              and word_search[y + (side_search[0] * 3)][x + (side_search[1] * 3)] == "S"):
              xmas_count += 1
      
      if word_search[y][x] == "A":
        searchable = [x + 1 < x_max, y + 1 < y_max, x - 1 >= 0, y - 1 >= 0]

        for search in range(4):
          side_search = [round(math.sin(search * (math.pi / 2))), round(math.cos(search * (math.pi / 2)))]

          if all(searchable):
            if (word_search[y + (1 if side_search[0] == 0 else side_search[0])][x + (1 if side_search[1] == 0 else side_search[1])] == "M" 
              and word_search[y + (-1 if side_search[0] == 0 else side_search[0])][x + (-1 if side_search[1] == 0 else side_search[1])] == "M"
              and word_search[y + (1 if side_search[0] == 0 else -side_search[0])][x + (1 if side_search[1] == 0 else -side_search[1])] == "S" 
              and word_search[y + (-1 if side_search[0] == 0 else -side_search[0])][x + (-1 if side_search[1] == 0 else -side_search[1])] == "S"):
              x_mas_count += 1

  return xmas_count, x_mas_count

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day4input.txt"
with open(inputFilePath, "r") as inputFile:
  print(get_xmas_count(inputFile.read()))