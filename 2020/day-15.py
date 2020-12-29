# -*- coding: utf-8 -*-
"""
Day 15 Advent of Code 2020 file.

Created on Wed Dec 16 12:05:10 2020

@author: Eftychios
"""

inp = [0, 3, 6]
# inp = [3, 1, 2]
inp = [1, 17, 0, 10, 18, 11, 6]

ages = {num: i
        for i, num in enumerate(inp[:-1])}

last_num = inp[-1]
for cnt in range(len(inp) - 1, 2020 - 1):
    if last_num in ages:
        next_num = cnt - ages[last_num]
    else:
        next_num = 0

    ages[last_num] = cnt
    last_num = next_num

print('Answer 1:', next_num)


ages = {num: i
        for i, num in enumerate(inp[:-1])}

last_num = inp[-1]
for cnt in range(len(inp) - 1, 30_000_000 - 1):
    if last_num in ages:
        next_num = cnt - ages[last_num]
    else:
        next_num = 0

    ages[last_num] = cnt
    last_num = next_num


print('Answer 2:', next_num)
