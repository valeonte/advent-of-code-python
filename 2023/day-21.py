"""
Advent of Code 2023 day 21.

Created on Sat Dec 23 2023 8:50:11 PM

@author: Eftychios
"""

import os
import json
import re
import math

import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, Set, Iterator, Dict, List
from dataclasses import dataclass, replace
from enum import Enum

os.chdir("C:/Repos/advent-of-code-python/2023")

part1 = False

inp_string = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


# with open("inputs/day-21.txt", "r") as f:
#     inp_string = f.read()

inps = inp_string.split('\n')

def get_neighbours(i: int, j: int, max_i: int, max_j: int) -> Iterator[Tuple[int, int]]:
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < max_i:
        yield i + 1, j
    if j < max_j:
        yield i, j + 1


def get_reachable(farm: np.array, from_nodes: Set[Tuple[int, int]]) -> Iterator[Tuple[int, int]]:
    reachable = set()
    for i, j in from_nodes:
        for ni, nj in get_neighbours(i, j, farm.shape[0], farm.shape[1]):
            if (ni, nj) not in from_nodes and farm[ni, nj] == 0:
                reachable.add((ni, nj))

    return reachable

def print_farm(farm: np.array, cur_nodes: Set[Tuple[int, int]]):
    print('-' * 50)
    for i, row in enumerate(farm):
        line = ''
        for j, el in enumerate(row):
            if (i, j) in cur_nodes:
                line += 'O'
            elif el == -1:
                line += '#'
            else:
                line += '.'
        print(line)

farm = np.zeros((len(inps), len(inps[0])))
for i, row in enumerate(inps):
    for j, ch in enumerate(row):
        if ch == '#':
            farm[i, j] = -1
        elif ch == 'S':
            start_pos = (i, j)


if part1:
    steps = 64
    cur_nodes = {start_pos}
    while steps > 0:
        steps -= 1
        cur_nodes = get_reachable(farm, from_nodes=cur_nodes)
        # print_farm(farm, cur_nodes)


    print('Answer 1:', len(cur_nodes))


class InfiniteFarm(object):
    def __init__(self, farm: np.array) -> None:
        self.farm = farm
        self.orig_i, self.orig_j = farm.shape

    def __getitem__(self, key):
        """Get item at i, j."""
        i, j = key
        return self.farm[i % self.orig_i, j % self.orig_j]


def get_reachable_inf(farm: InfiniteFarm, from_nodes: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    reachable = set()
    for i, j in from_nodes:
        for ni, nj in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:
            if (ni, nj) not in from_nodes and farm[ni, nj] == 0:
                reachable.add((ni, nj))

    return reachable


ifarm = InfiniteFarm(farm)
steps = 100
cur_nodes = {start_pos}
all_lens = []
while steps > 0:
    steps -= 1
    cur_nodes = get_reachable_inf(ifarm, from_nodes=cur_nodes)
    all_lens.append(len(cur_nodes))


all_len = [all_lens[i+1] - all_lens[i] for i in range(len(all_lens)-1)]

ft = [all_len[i] - all_len[i - 11] for i in range(11, len(all_len))]
a = [ft[i + 11] == ft[i] for i in range(len(ft) - 11)]

plt.plot(ft)
plt.plot(ft)
plt.show()

period = 11
period_start = 36


idx = 47
ps = idx - period_start
one_period_sum = all_len[period_start:period_start + period]
all_lens_val = all_len[0] + sum(all_len[:period_start]) \
    + sum(all_len[period_start:period_start + (ps % period)]) \
        + all_len[period_start + (ps % period) - 1] * (ps // period)

assert(all_lens_val == all_lens[idx])


print('Answer 2:', len(cur_nodes))
