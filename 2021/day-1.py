# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 1.

Created on Sat Dec  4 17:16:45 2021

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """199
200
208
210
200
207
240
269
260
263"""

with open("inputs/day-1.txt", "r") as f:
    inp_string = f.read()


inp = [int(s) for s in inp_string.split("\n")]

increases = 0
last = None
for num in inp:
    if last is not None and num > last:
        increases = increases + 1
    last = num

print('Answer 1:', increases)

increases = 0
last = None
for i in range(len(inp)):
    if i < 2:
        continue
    cur = inp[i - 2] + inp[i - 1] + inp[i]
    if last is not None and cur > last:
        increases = increases + 1

    last = cur

print('Answer 2:', increases)
