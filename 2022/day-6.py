# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 5.

Created on Tue Dec  6 21:43:51 2022

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2022")

inp = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"

with open("inputs/day-6.txt", "r") as f:
    inp = f.read()


for i in range(4, len(inp)):
    marker = set(inp[i - 4:i])
    if len(marker) == 4:
        break


print('Answer 1:', i)


for i in range(14, len(inp)):
    marker = set(inp[i - 14:i])
    if len(marker) == 14:
        break

print('Answer 2:', i)
