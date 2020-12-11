# -*- coding: utf-8 -*-
"""
Day 10 Advent of Code 2020 file.

Created on Fri Dec 11 16:10:06 2020

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

with open("inputs/day-10.txt", "r") as f:
    inp_string = f.read()


adapters = [int(s) for s in inp_string.split("\n")]
adapters.sort()

adapters.append(adapters[-1] + 3)

last = 0
diffs = {1: 0, 2: 0, 3: 0}

for a in adapters:
    diff = a - last
    diffs[diff] += 1

    last = a

print('Answer 1:', diffs[1] * diffs[3])


adapters.insert(0, 0)
size = len(adapters)

combos_up_to_index = [1] * size
for i in range(1, size):
    combos_up_to_index[i] = combos_up_to_index[i - 1]
    if i > 1 and adapters[i] - adapters[i - 2] <= 3:
        combos_up_to_index[i] += combos_up_to_index[i - 2]
    if i > 2 and adapters[i] - adapters[i - 3] <= 3:
        combos_up_to_index[i] += combos_up_to_index[i - 3]

print('Answer 2:', combos_up_to_index[-1])
