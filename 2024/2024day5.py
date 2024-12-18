import os

ruleDict = {}

def organize_rule(rules):
  ruleList = rules.split("\n")

  for rule in ruleList:
    order = list(map(int, rule.split("|")))

    if not order[0] in ruleDict:
      ruleDict[order[0]] = set()
    ruleDict[order[0]].add(order[1])

def validate_update(updates):
  updateList = updates.split("\n")

  validUpdateList = []
  invalidUpdateList = []

  for update in updateList:
    updateNumbers = list(map(int, update.split(",")))

    valid = True
    preceedingNumber = set()

    for number in updateNumbers:
      numberRule = set() if not number in ruleDict else ruleDict[number]
      if any(num in preceedingNumber for num in numberRule):
        valid = False
        break

      preceedingNumber.add(number)

    if valid:
      validUpdateList.append(updateNumbers)
    else:
      invalidUpdateList.append(updateNumbers)

  return validUpdateList, invalidUpdateList

# min heap
def heapify(arr, n, i):
  smallest = i

  l = 2 * i + 1
  r = 2 * i + 2

  if l < n and arr[smallest] in ruleDict and arr[l] in ruleDict[arr[smallest]]:
    smallest = l

  if r < n and arr[smallest] in ruleDict and arr[r] in ruleDict[arr[smallest]]:
    smallest = r

  if smallest != i:
    arr[i], arr[smallest] = arr[smallest], arr[i]

    heapify(arr, n, smallest)

def heapSort(arr):
  n = len(arr)

  for i in range(n // 2 - 1, -1, -1):
    heapify(arr, n, i)

  for i in range(n - 1, 0, -1):
    arr[0], arr[i] = arr[i], arr[0]

    heapify(arr, i, 0)

def reorder_invalid(invalidList):
  for numList in invalidList:
    heapSort(numList)

def get_middle_number_sum(numLists):
  sum = 0

  for numList in numLists:
    listSize = len(numList)
    midIndex = listSize // 2

    sum += numList[midIndex]

  return sum

def separate_rule_update(input):
  ruleUpdate = input.split("\n\n")

  organize_rule(ruleUpdate[0])
  validList, invalidList = validate_update(ruleUpdate[1])
  reorder_invalid(invalidList)

  return get_middle_number_sum(validList), get_middle_number_sum(invalidList)

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day5input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(separate_rule_update(inputFile.read()))