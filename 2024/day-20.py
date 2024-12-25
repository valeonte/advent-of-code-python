"""
Advent of Code 2024 day 20.

Created on Sun Dec 22 2024 9:46:17 PM

@author: Eftychios
"""

import re
import os
import math
import sys

import datetime as dt
import numpy as np

from functools import lru_cache
from typing import Dict, Iterable, List, Set, Tuple
from dataclasses import dataclass
from decimal import Decimal
from tqdm import tqdm, trange
from common import Dir, get_neighbours
from itertools import product

os.chdir("C:/Repos/advent-of-code-python/2024")



inp_string = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

minimum_reduction = 1


with open("inputs/day-20.txt", "r") as f:
    inp_string = f.read()
minimum_reduction = 100


inps = inp_string.split("\n")
max_x = len(inps[0]) - 1
max_y = len(inps) - 1

racetrack = np.zeros((max_y+1, max_x+1), dtype=np.int8)
start = None
end = None
internal_walls: Set[Tuple[int, int]] = list()

for y, line in enumerate(inps):
    for x, ch in enumerate(line):
        if ch == '#':
            racetrack[y, x] = -1
            if x > 0 and y > 0 and x < max_x and y < max_y:
                internal_walls.append((x, y))
        elif ch == 'S':
            start = (x, y)
        elif ch == 'E':
            end = (x, y)


def print_racetrack(racetrack: np.ndarray):
    print('-'*20)
    for y in range(max_y+1):
        for x in range(max_x+1):
            num = racetrack[y, x]
            if num == -1:
                ch = '#'
            else:
                ch = '.'
            print(ch, end='')
        print()


def get_fastest_time(racetrack: np.ndarray, ignore_wall_at: Tuple[int, int] = (-1, -1)) -> int:
    shortest_paths = dict()
    check_q = [(end[0], end[1], 0)]

    while len(check_q) > 0:
        x, y, cost = check_q.pop(0)
        if x > max_x or y > max_y or x < 0 or y < 0 or (x, y) != ignore_wall_at and racetrack[y, x] == -1:
            continue
        pre_cost = shortest_paths.get((x, y), math.inf)
        if cost >= pre_cost:
            continue
        shortest_paths[(x, y)] = cost
        #print_map()
        for nx, ny in get_neighbours(x, y):
            check_q.append((nx, ny, cost+1))

    return shortest_paths[start]


orig_time = get_fastest_time(racetrack)
max_reduction = 0
reduction_counts: Dict[int, int] = dict()
reductions_total = 0

print('Original fastest time:', orig_time)
for w in tqdm(internal_walls):
    if not (racetrack[w[1]-1, w[0]] == 0 and racetrack[w[1]+1, w[0]] == 0
            or racetrack[w[1], w[0]-1] == 0 and racetrack[w[1], w[0]+1] == 0):
        continue
    new_time = get_fastest_time(racetrack, ignore_wall_at=w)
    reduction = orig_time - new_time
    if reduction >= minimum_reduction:
        reductions_total += 1
        reduction_counts[reduction] = reduction_counts.get(reduction, 0) + 1
        if reduction > max_reduction:
            print('New max reduction:', reduction)
            max_reduction = reduction


print('Answer 1:', reductions_total)
