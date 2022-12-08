# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 8.

Created on Thu Dec  8 18:44:13 2022

@author: Eftychios
"""

import os

import numpy as np


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """30373
25512
65332
33549
35390"""

with open("inputs/day-8.txt", "r") as f:
    inp_string = f.read()


for i, row in enumerate(inp_string.split('\n')):
    if i == 0:
        n = len(row)
        inp = np.ones((n, n)) * np.nan

    inp[i, :] = np.array([int(c) for c in row])


visible = 0
for (i, j), v in np.ndenumerate(inp):
    if i == 0 or j == 0 or i == n-1 or j == n-1:
        visible += 1
        continue

    # left side
    if (inp[i, :j] < v).all():
        visible += 1
        continue

    # right side
    if (inp[i, j+1:] < v).all():
        visible += 1
        continue

    # top side
    if (inp[:i, j] < v).all():
        visible += 1
        continue

    # bottom side
    if (inp[i+1:, j] < v).all():
        visible += 1

print('Answer 1:', visible)


scores = np.ones(inp.shape) * np.nan
for (i, j), v in np.ndenumerate(inp):
    if i == 0 or j == 0 or i == n-1 or j == n-1:
        scores[i, j] = 0
        continue

    score = 1
    # left
    cnt = 0
    for k in range(j - 1, -1, -1):
        cnt += 1
        if inp[i, k] >= v:
            break
    score *= cnt

    # right
    cnt = 0
    for k in range(j + 1, n):
        cnt += 1
        if inp[i, k] >= v:
            break
    score *= cnt

    # top
    cnt = 0
    for k in range(i - 1, -1, -1):
        cnt += 1
        if inp[k, j] >= v:
            break
    score *= cnt

    # top
    cnt = 0
    for k in range(i + 1, n):
        cnt += 1
        if inp[k, j] >= v:
            break
    score *= cnt

    scores[i, j] = score

print('Answer 2:', scores.max())
