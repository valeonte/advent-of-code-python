# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 12.

Created on Mon Dec 12 22:03:16 2022

@author: Eftychios
"""

import os

import numpy as np

from typing import Iterator, Tuple


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

with open("inputs/day-12.txt", "r") as f:
    inp_string = f.read()


rows = []
for i, row in enumerate(inp_string.split('\n')):
    arr = []
    rows.append(arr)
    for j, ch in enumerate(row):
        if ch == 'S':
            start = (i, j)
            ch = 'a'
        elif ch == 'E':
            end = (i, j)
            ch = 'z'

        arr.append(ord(ch) - 97)

max_i = i
max_j = j

hm = np.array(rows)
costs = np.ones(hm.shape) * np.nan

costs[end] = 0


def get_neighbours(i: int, j: int) -> Iterator[Tuple[int, int]]:
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < max_i:
        yield i + 1, j
    if j < max_j:
        yield i, j + 1


changes_made = True
cnt = 0
while changes_made:
    changes_made = False
    cnt += 1
    if cnt % 100 == 0:
        print(cnt, 'iterations')
    for (i, j), h in np.ndenumerate(hm):
        min_cost = costs[i, j]
        if not np.isnan(min_cost):
            continue
        for ni, nj in get_neighbours(i, j):
            ncost = costs[ni, nj]
            if np.isnan(ncost):
                # Can't get cost from here
                continue

            if hm[ni, nj] <= h + 1:
                cost = ncost + 1
                if np.isnan(min_cost) or cost < min_cost:
                    min_cost = cost
        if not np.isnan(min_cost):
            costs[i, j] = min_cost
            changes_made = True

print('Answer 1:', costs[start])

print('Answer 2:', costs[(hm == 0) & ~np.isnan(costs)].min())
