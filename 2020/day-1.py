# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:18:10 2020

@author: valeo
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """1721
979
366
299
675
1456"""

with open("inputs/day-1.txt", "r") as f:
    inp_string = f.read()


inp = [int(s) for s in inp_string.split("\n")]

for i in range(0, len(inp)):
    for j in range(i + 1, len(inp)):
        for k in range(j + 1, len(inp)):
            x = inp[i]
            y = inp[j]
            z = inp[k]

            if x + y + z == 2020:
                break
        if x + y + z == 2020:
            break

    if x + y + z == 2020:
        print('Got solution')
        break

answer = x * y * z
print(answer)
