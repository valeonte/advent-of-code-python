# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 7.

Created on Tue Dec  7 15:45:20 2021

@author: Eftychios
"""

import os

import numpy as np


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = "16,1,2,0,4,2,7,1,2,14"

with open("inputs/day-7.txt", "r") as f:
    inp_string = f.read()

inp = np.array([int(i) for i in inp_string.split(',')])

med = np.median(inp)
print('Best position:', med, ', Answer 1:', abs(inp - med).sum())


# Start from median and move towards either direction, to find the least


def calc_fuel(pos1: int, pos2: int) -> int:
    """Calculate the fuel to go from position pos1 to pos2."""
    n = abs(pos1 - pos2)

    return n * (n + 1) / 2


best = med
best_sum = sum([calc_fuel(best, x)
                for x in inp])

while True:
    chk = best + 1
    chk_sum = sum([calc_fuel(chk, x)
                   for x in inp])
    if chk_sum > best_sum:
        break
    if chk_sum < best_sum:
        best = chk
        best_sum = chk_sum

print('Best position:', best, ', Answer 1:', best_sum)
