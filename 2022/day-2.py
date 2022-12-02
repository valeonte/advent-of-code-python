# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 2.

Created on Fri Dec  2 21:55:05 2022

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """A Y
B X
C Z"""

with open("inputs/day-2.txt", "r") as f:
    inp_string = f.read()

scores = {'A X': 1 + 3,
          'A Y': 2 + 6,
          'A Z': 3 + 0,
          'B X': 1 + 0,
          'B Y': 2 + 3,
          'B Z': 3 + 6,
          'C X': 1 + 6,
          'C Y': 2 + 0,
          'C Z': 3 + 3}

score = 0
for row in inp_string.split("\n"):
    score += scores[row]

print('Answer 1:', score)


scores2 = {'A X': 3 + 0,
           'A Y': 1 + 3,
           'A Z': 2 + 6,
           'B X': 1 + 0,
           'B Y': 2 + 3,
           'B Z': 3 + 6,
           'C X': 2 + 0,
           'C Y': 3 + 3,
           'C Z': 1 + 6}

score = 0
for row in inp_string.split("\n"):
    score += scores2[row]

print('Answer 2:', score)
