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

inp_string = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

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

with open("inputs/day-12.txt", "r") as f:
    inp_string = f.read()


@dataclass
class Region:
    plant: str
    fence: int
    area: int
    sides: int = -1


regions: List[Tuple[int, int]] = []

field = inp_string.split('\n')

max_x = len(field[0])
max_y = len(field)

plant_region_map: Dict[Tuple[int, int], Region] = dict()

other_region_stack: List[Tuple[int, int]] = [(0, 0)]
all_regions: List[Region] = []


def calc_region_sides(region_nodes: List[Tuple[int, int]]) -> int:
    north_fences = []
    south_fences = []
    east_fences = []
    west_fences = []
    for x, y in region_nodes:
        if (x-1, y) not in region_nodes:
            west_fences.append((x, y))
        if (x+1, y) not in region_nodes:
            east_fences.append((x, y))
        if (x, y-1) not in region_nodes:
            north_fences.append((x, y))
        if (x, y+1) not in region_nodes:
            south_fences.append((x, y))

    sides = 0
    for ew_fences in [east_fences, west_fences]:
        last_x, last_y = -1, -1
        for x, y in sorted(ew_fences):
            # Sorting is first by x then by y
            if last_x != x:
                sides += 1
            else:
                # same x, check for y continuity
                if y > last_y + 1:
                    # there is a gap in the side, so increase count
                    sides += 1

            last_x, last_y = x, y

    for ns_fences in [north_fences, south_fences]:
        last_x, last_y = -1, -1
        for x, y in sorted(ns_fences, key=lambda n:n[1]*1000000+n[0]):
            # Sorting is fist by y then by x
            if last_y != y:
                sides += 1
            else:
                # same y, check for x continuity
                if x > last_x + 1:
                    # there is a gap in the side, so increase count
                    sides += 1

            last_x, last_y = x, y

    return sides


while len(other_region_stack) > 0:
    x, y = other_region_stack.pop()
    if (x, y) in plant_region_map:
        continue
    cur_region = Region(field[y][x], area=0, fence=0)
    all_regions.append(cur_region)
    cur_region_stack = [(x, y)]
    cur_region_nodes = set()

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
            cur_region_nodes.add((x, y))
            plant_region_map[(x, y)] = cur_region
            cur_region_stack.append((x+1, y))
            cur_region_stack.append((x, y+1))
            cur_region_stack.append((x-1, y))
            cur_region_stack.append((x, y-1))
        else:
            cur_region.fence += 1
            other_region_stack.append((x, y))

    cur_region.sides = calc_region_sides(cur_region_nodes)


print('Answer 1:', sum([r.area*r.fence for r in all_regions]))

print('Answer 2:', sum([r.area*r.sides for r in all_regions]))
