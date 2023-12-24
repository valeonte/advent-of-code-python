"""
Advent of Code 2023 day 21.

Created on Sat Dec 23 2023 8:50:11 PM

@author: Eftychios
"""

import os
import json
import re
import math

import datetime as dt
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


with open("inputs/day-21.txt", "r") as f:
    inp_string = f.read()

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
steps = 300
print('Populating first', steps, 'steps', dt.datetime.now())
cur_nodes = {start_pos}
all_lens = []
while steps > 0:
    steps -= 1
    cur_nodes = get_reachable_inf(ifarm, from_nodes=cur_nodes)
    all_lens.append(len(cur_nodes))

print('Done, doing derivs and finding period', dt.datetime.now())

deriv1 = [all_lens[i] - all_lens[i-1] for i in range(1, len(all_lens))]
deriv2 = [deriv1[i] - deriv1[i-1] for i in range(1, len(deriv1))]


def find_period(deriv2: List[int]) -> Tuple[int, int]:
    """Attempt to auto-find period and offset."""
    # numbers in an entire period should have the exact same sum
    period = 5
    while period < len(deriv2) // 2:
        sums = [sum(deriv2[i-period:i])
               for i in range(period, len(deriv2), period)]
        period_sum = sums[-1]
        cont_eq = 0
        while cont_eq < len(sums) and sums[-1 - cont_eq] == period_sum:
            cont_eq += 1
        if cont_eq > 1:
            period_start = (len(sums) - cont_eq) * period
            first_period = deriv2[period_start:period_start + period]
            return period_start, period, period_sum, first_period

        period += 1
    
    raise Exception('Failed to find any period!')


period_start, period, period_sum, first_period = find_period(deriv2)
period_incs = [deriv2[i+period] - deriv2[i] for i in range(period_start, period_start + period)]


def find_deriv1_value(x: int) -> int:
    ret = deriv1[0]
    if x <= period_start:
        return ret + sum(deriv2[:x])
    ret += sum(deriv2[:period_start])

    periods = (x - period_start) // period
    ret += periods * period_sum
    for rem in range((x - period_start) % period):
        ret += first_period[rem] + period_incs[rem] * periods

    return ret


# Confirming it works correctly
for x in range(len(deriv1)):
    assert(deriv1[x] == find_deriv1_value(x))


def find_all_lens_value(x: int) -> int:
    return all_lens[0] + sum([find_deriv1_value(i) for i in range(x)])


for x in range(len(all_lens)):
    if x == 0:
        last_no = all_lens[0]
        continue
    last_no += find_deriv1_value(x - 1)
    assert(all_lens[x] == last_no)

print('All good, knocking it on the head now!')

start = dt.datetime.now()
steps = 26501365
for x in range(steps):
    if x == 0:
        last_no = all_lens[0]
        continue
    last_no += find_deriv1_value(x - 1)
    if x % 1_000_000 == 0:
        spent = dt.datetime.now() - start
        est = steps * spent/x - spent
        print('x =', x, 'no =', last_no, 'spent =', spent, 'est finish =', est)

print('Answer 2:', last_no)
print('Done?')
