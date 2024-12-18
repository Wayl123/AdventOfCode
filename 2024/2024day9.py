import os
import copy

fileBlock = []
freeSpace = []
movedFileBlock = []
movedFreeSpace = []

def find_checksum():
  fileBlockLen = sum(fileBlock)

  fileBlockIndex = 0
  fileBlockReverseIndex = len(fileBlock) - 1
  freeSpaceIndex = 0
  fileFlag = True
  spaceCounter = fileBlock[fileBlockIndex]
  reverseCounter = fileBlock[fileBlockReverseIndex]

  freeSpaceLen = sum(freeSpace)

  q2MovedFileBlockIndex = 0
  q2MovedFileBlock = movedFileBlock[q2MovedFileBlockIndex]
  q2MovedFileBlockCounter = q2MovedFileBlock[1]

  checksum = 0
  q2Checksum = 0

  # Part 1
  for i in range(fileBlockLen):
    while spaceCounter == 0:
      if fileFlag:
        fileBlockIndex += 1
        if freeSpaceIndex >= len(freeSpace):
          break
        spaceCounter = freeSpace[freeSpaceIndex]
      else:
        freeSpaceIndex += 1
        if fileBlockIndex >= len(fileBlock):
          break
        spaceCounter = fileBlock[fileBlockIndex]

      fileFlag = not fileFlag
    
    if fileFlag:
      checksum += i * fileBlockIndex
    else:
      while reverseCounter == 0:
        fileBlockReverseIndex -= 1
        reverseCounter = fileBlock[fileBlockReverseIndex]
      checksum += i * fileBlockReverseIndex
      reverseCounter -= 1

    spaceCounter -= 1

  # Part 2
  for i in range(fileBlockLen + freeSpaceLen):
    while q2MovedFileBlockCounter == 0:
      q2MovedFileBlockIndex += 1
      q2MovedFileBlock = movedFileBlock[q2MovedFileBlockIndex]
      q2MovedFileBlockCounter = q2MovedFileBlock[1]
    q2Checksum += i * q2MovedFileBlock[0]
    q2MovedFileBlockCounter -= 1

  return checksum, q2Checksum

def move_whole_file():
  global movedFileBlock, movedFreeSpace

  movedFreeSpace = copy.deepcopy(freeSpace)
  movedFileBlock = [[] for _ in range(len(fileBlock) + len(movedFreeSpace))]

  for i in range(len(fileBlock) - 1, -1, -1):
    movedFlag = False

    for j in range(i):
      if movedFreeSpace[j] >= fileBlock[i]:
        movedFreeSpace[j] -= fileBlock[i]
        movedFileBlock[(j * 2) + 1].append((i, fileBlock[i]))
        movedFlag = True
        break

    if not movedFlag:
      movedFileBlock[i * 2].append((i, fileBlock[i]))
    else:
      movedFileBlock[i * 2].append((0, fileBlock[i]))

  for i in range(len(movedFreeSpace)):
    if movedFreeSpace[i] > 0:
      movedFileBlock[(i * 2) + 1].append((0, movedFreeSpace[i]))

  movedFileBlock = sum(movedFileBlock, [])

def separate_file(inputCharList):
  global fileBlock, freeSpace

  for i in range(len(inputCharList)):
    if i % 2 == 0:
      fileBlock.append(int(inputCharList[i]))
    else:
      freeSpace.append(int(inputCharList[i]))

def separate_and_find_checksum(input):
  separate_file(list(input))

  move_whole_file()

  return(find_checksum())

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day9input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(separate_and_find_checksum(inputFile.read()))