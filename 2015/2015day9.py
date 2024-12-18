import os
from collections import deque
from copy import deepcopy
from functools import cache

cities = {}
# cachedSet = {}

@cache
def shortest_longest_distance(citySet):
  global cachedSet

  cityName = list(citySet)
  
  if len(citySet) == 2:
    return cities[cityName[0]][cityName[1]], deque([cityName[0], cityName[1]]), cities[cityName[0]][cityName[1]], deque([cityName[0], cityName[1]])
  # elif citySet in cachedSet:
  #   return cachedSet[citySet]
  else:
    resultMin = 10**9
    resultMax = 0
    pathMin = deque()
    pathMax = deque()

    for city in cityName:
      subCitySet = set(citySet)
      subCitySet.remove(city)

      subDist = deepcopy(shortest_longest_distance(frozenset(subCitySet)))
      tempResultMin = subDist[0]
      tempResultMax = subDist[2]
      joinToStartMinFlag = True
      joinToStartMaxFlag = True

      if cities[city][subDist[1][0]] <= cities[city][subDist[1][-1]]:
        tempResultMin += cities[city][subDist[1][0]]
      else: 
        tempResultMin += cities[city][subDist[1][-1]]
        joinToStartMinFlag = False

      if tempResultMin < resultMin:
        resultMin = tempResultMin
        pathMin = subDist[1]
        if joinToStartMinFlag:
          pathMin.appendleft(city)
        else:
          pathMin.append(city)

      if cities[city][subDist[3][0]] >= cities[city][subDist[3][-1]]:
        tempResultMax += cities[city][subDist[3][0]]
      else: 
        tempResultMax += cities[city][subDist[3][-1]]
        joinToStartMaxFlag = False

      if tempResultMax > resultMax:
        resultMax = tempResultMax
        pathMax = subDist[3]
        if joinToStartMaxFlag:
          pathMax.appendleft(city)
        else:
          pathMax.append(city)

    # cachedSet[citySet] = resultMin, pathMin, resultMax, pathMax

    return resultMin, pathMin, resultMax, pathMax

def add_city_to_dict(dist):
  global cities

  cityDist = dist.split(" = ")
  cityToCity = cityDist[0].split(" to ")

  if not cityToCity[0] in cities:
    cities[cityToCity[0]] = {}

  if not cityToCity[1] in cities:
    cities[cityToCity[1]] = {}

  cities[cityToCity[0]][cityToCity[1]] = int(cityDist[1])
  cities[cityToCity[1]][cityToCity[0]] = int(cityDist[1])

def read_dist_list(input):
  distList = input.split("\n")

  for dist in distList:
    add_city_to_dict(dist)

  return shortest_longest_distance(frozenset(cities.keys()))

inputFilePath = os.path.dirname(__file__) + "\\input\\2015day9input.txt"
with open(inputFilePath, "r") as inputFile:
  print(read_dist_list(inputFile.read()))