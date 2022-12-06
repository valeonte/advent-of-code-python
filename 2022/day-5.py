# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 5.

Created on Mon Dec  5 08:04:20 2022

@author: Eftychios
"""

import os
import re


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

with open("inputs/day-5.txt", "r") as f:
    inp_string = f.read()

stacks = dict()

# parse stacks
for row in inp_string.split('\n'):
    if '[' in row:
        idx = 0
        for i in range(1, len(row), 4):
            if row[i] != ' ':
                if idx + 1 in stacks:
                    stack = stacks[idx + 1]
                else:
                    stack = []
                stack.insert(0, row[i])

                stacks[idx + 1] = stack

            idx += 1
    else:
        break

pat = re.compile(r'^move (\d+) from (\d+) to (\d+)$')

# now move
for row in inp_string.split('\n'):
    if not row.startswith('move'):
        continue

    m = pat.match(row)

    rep = int(m.group(1))
    ffrom = int(m.group(2))
    tto = int(m.group(3))
    for _ in range(rep):
        stacks[tto].append(stacks[ffrom].pop())

ret = ''
for i in range(len(stacks)):
    ret += stacks[i + 1][-1]

print('Answer 1:', ret)


stacks = dict()

# parse stacks
for row in inp_string.split('\n'):
    if '[' in row:
        idx = 0
        for i in range(1, len(row), 4):
            if row[i] != ' ':
                if idx + 1 in stacks:
                    stack = stacks[idx + 1]
                else:
                    stack = []
                stack.insert(0, row[i])

                stacks[idx + 1] = stack

            idx += 1
    else:
        break
print(stacks)

# now move  # 2
for row in inp_string.split('\n'):
    if not row.startswith('move'):
        continue

    m = pat.match(row)

    rep = int(m.group(1))
    ffrom = int(m.group(2))
    tto = int(m.group(3))

    stacks[tto] = stacks[tto] + stacks[ffrom][-rep:]
    stacks[ffrom] = stacks[ffrom][:-rep]


ret = ''
for i in range(len(stacks)):
    ret += stacks[i + 1][-1]

print('Answer 2:', ret)
