import os
from functools import cache

connections = {}
tConnections = set()
largestGroup = frozenset()

def add_connection(connection):
  global connections

  computers = connection.split("-")

  for com in range(2):
    if not computers[com] in connections:
      connections[computers[com]] = set()
    connections[computers[com]].add(computers[(com + 1) % 2])

@cache
def find_largest_intersect(intersectGroup):
  global largestGroup

  intersection = set.intersection(*[connections[key] for key in intersectGroup])

  for intersect in intersection:
    intersectGroupNext = set(intersectGroup)
    intersectGroupNext.add(intersect)

    find_largest_intersect(frozenset(intersectGroupNext))

  if len(intersectGroup) > len(largestGroup):
    largestGroup = intersectGroup

def check_connections():
  global tConnections

  checked = set()

  for computer in connections:
    connection = connections[computer]

    for connected in connection:
      if not connected in checked:
        find_largest_intersect(frozenset({computer, connected}))
        intersection = connection & connections[connected]

        for intersect in intersection:
          connectionGroup = frozenset({computer, connected, intersect})
          if computer[0] == "t" or connected[0] == "t" or intersect[0] == "t":
            tConnections.add(connectionGroup)

    checked.add(computer)

def check_connection_group(input):
  connections = input.split("\n")

  for connection in connections:
    add_connection(connection)

  check_connections()

  largestGroupList = sorted(list(largestGroup))

  return len(tConnections), ",".join(largestGroupList)

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day23input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(check_connection_group(inputFile.read()))