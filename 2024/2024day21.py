import os
import numpy as np
import re
from functools import cache, lru_cache

numericKeypad = np.array([["7", "8", "9"],
                          ["4", "5", "6"],
                          ["1", "2", "3"],
                          [None, "0", "A"]])

directionalKeypad = np.array([[None, "^", "A"],
                              ["<", "v", ">"]])

@cache
def find_char(char, isNumericKeypad):
  keypad = numericKeypad if isNumericKeypad else directionalKeypad

  return tuple(np.asarray(np.where(keypad == char)).T[0])

@cache
def move_to_pos(pos, goal, upDownIndex):
  upDown = pos[0] - goal[0]
  leftRight = pos[1] - goal[1]

  upDownOut = ("^" if upDown > 0 else "v") * abs(upDown)
  outSeq = ["<" * abs(leftRight) if leftRight > 0 else "", ">" * abs(leftRight) if leftRight < 0 else ""]
  
  outSeq.insert(upDownIndex, upDownOut)

  return "".join(outSeq)

@cache
def section_encode(subseq, isNumericKeypad = False):
  outSeq = ""

  pos = (3, 2) if isNumericKeypad else (0, 2)

  for char in subseq:
    goal = find_char(char, isNumericKeypad)

    if goal[1] == 0 and (isNumericKeypad and pos[0] == 3 or not isNumericKeypad and pos[0] == 0):
      outSeq += move_to_pos(pos, goal, 0)
    elif pos[1] == 0 and (isNumericKeypad and goal[0] == 3 or not isNumericKeypad and goal[0] == 0):
      outSeq += move_to_pos(pos, goal, 2)
    else:
      outSeq += move_to_pos(pos, goal, 1)

    outSeq += "A"
    pos = goal

  return outSeq

@cache
def reverse_sequence(seq, depth = 0, isNumericKeypad = False):
  if depth == 0:
    return len(seq)

  outSeq = 0

  seqSplit = re.split("([<v>^0-9]+A|A+)", seq)[1::2]

  for subseq in seqSplit:
    if subseq[0] == "A":
      outSeq += len(subseq)
    else:
      encodeSeq = section_encode(subseq, isNumericKeypad)
      outSeq += reverse_sequence(encodeSeq, depth - 1)

  return outSeq

def encode_sequences(inputSeqs):
  seqs = inputSeqs.split("\n")

  q1OutNum = 0
  q2OutNum = 0
  q1Depth = 2
  q2Depth = 25

  for seq in seqs:
    seqNum = int(seq[0:3])

    q1Out = reverse_sequence(seq, q1Depth + 1, True)
    q2Out = reverse_sequence(seq, q2Depth + 1, True)

    q1OutNum += seqNum * q1Out
    q2OutNum += seqNum * q2Out

  return q1OutNum, q2OutNum

inputFilePath = os.path.dirname(__file__) + "\\input\\2024day21input.txt"
with open(inputFilePath, "r") as inputFile: 
  print(encode_sequences(inputFile.read()))