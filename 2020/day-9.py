# -*- coding: utf-8 -*-
"""
Day 9 Advent of Code 2020 file.

Created on Fri Dec 11 14:29:56 2020

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

with open("inputs/day-9.txt", "r") as f:
    inp_string = f.read()


preamble = 5
preamble = 25

q = list()

for cnt, row in enumerate(inp_string.split("\n")):
    num = int(row)
    if len(q) < preamble:
        q.append(num)
        continue

    found = False
    for i, n1 in enumerate(q):
        for j in range(i + 1, preamble):
            found = n1 + q[j] == num
            if found:
                break
        if found:
            break

    if not found:
        break

    q[cnt % preamble] = num

print('Answer 1:', num)

q = list()
target_sum = num

for cnt, row in enumerate(inp_string.split("\n")):
    num = int(row)
    q.append(num)

    while sum(q) > target_sum:
        q.pop(0)

    if sum(q) == target_sum:
        break

print('Answer 2:', min(q) + max(q))
