"""
Advent of Code 2024 day 12.

Created on Sat Dec 14 2024 11:20:45 PM

@author: Eftychios
"""

import os
import math

import datetime as dt

from functools import lru_cache
from typing import Dict, Iterable, List, Set, Tuple
from dataclasses import dataclass


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

inp_string = """AAAA
BBCD
BBCC
EEEC"""

# with open("inputs/day-12.txt", "r") as f:
#     inp_string = f.read()


@dataclass
class Region:
    plant: str
    fence: int
    area: int


regions: List[Tuple[int, int]] = []

field = inp_string.split('\n')

max_x = len(field[0])
max_y = len(field)

plant_region_map: Dict[Tuple[int, int], Region] = dict()

other_region_stack: Tuple[int, int] = [(0, 0)]
all_regions: List[Region] = []

while len(other_region_stack) > 0:
    x, y = other_region_stack.pop()
    if (x, y) in plant_region_map:
        continue
    cur_region = Region(field[y][x], area=0, fence=0)
    all_regions.append(cur_region)
    cur_region_stack = [(x, y)]

    while len(cur_region_stack) > 0:
        x, y = cur_region_stack.pop()
        if x < 0 or y < 0 or x == max_x or y == max_y:
            # Out of bounds
            cur_region.fence += 1
            continue
        if (x, y) in plant_region_map:
            if plant_region_map[(x, y)].plant != cur_region.plant:
                cur_region.fence += 1
            continue

        plant = field[y][x]
        if plant == cur_region.plant:
            cur_region.area += 1
            plant_region_map[(x, y)] = cur_region
            cur_region_stack.append((x+1, y))
            cur_region_stack.append((x, y+1))
            cur_region_stack.append((x-1, y))
            cur_region_stack.append((x, y-1))
        else:
            cur_region.fence += 1
            other_region_stack.append((x, y))



print('Answer 1:', sum([r.area*r.fence for r in all_regions]))
