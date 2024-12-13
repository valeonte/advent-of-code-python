"""
Advent of Code 2024 day 10.

Created on Fri Dec 13 2024 6:57:38 PM

@author: Eftychios
"""

import os
import math

from typing import Dict, Iterable, List, Set, Tuple


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


with open("inputs/day-10.txt", "r") as f:
    inp_string = f.read()


tmap = [[int(c) for c in row] for row in inp_string.split('\n')]

max_y = len(tmap) - 1
max_x = len(tmap[0]) - 1


def get_reachable_nines_from(x: int, y: int, height: int) -> Iterable[Tuple[int, int]]:
    if height == 9:
        yield x, y
        return

    if x > 0:
        nh = tmap[y][x-1]
        if nh == height + 1:
            for nn in get_reachable_nines_from(x - 1, y, nh):
                yield nn
    if x < max_x:
        nh = tmap[y][x+1]
        if nh == height + 1:
            for nn in get_reachable_nines_from(x + 1, y, nh):
                yield nn
    if y > 0:
        nh = tmap[y-1][x]
        if nh == height + 1:
            for nn in get_reachable_nines_from(x, y-1, nh):
                yield nn
    if y < max_y:
        nh = tmap[y+1][x]
        if nh == height + 1:
            for nn in get_reachable_nines_from(x, y+1, nh):
                yield nn


ret = 0
for y, row in enumerate(tmap):
    for x, height in enumerate(row):
        if height != 0:
            continue
        ret += len(set(get_reachable_nines_from(x, y, height)))


print('Answer 1:', ret)



ret = 0
for y, row in enumerate(tmap):
    for x, height in enumerate(row):
        if height != 0:
            continue
        ret += len(list(get_reachable_nines_from(x, y, height)))

print('Answer 2:', ret)
