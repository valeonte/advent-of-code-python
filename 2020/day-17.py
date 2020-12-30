# -*- coding: utf-8 -*-
"""
Day 17 Advent of Code 2020 file.

Created on Wed Dec 30 17:25:11 2020

@author: Eftychios
"""

import os

from typing import Tuple, Iterator


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """.#.
..#
###"""


inp_string = """.##.##..
..###.##
.##....#
###..##.
#.###.##
.#.#..#.
.......#
.#..#..#"""


active = set()

z = 0
for x, row in enumerate(inp_string.split("\n")):
    for y, ch in enumerate(row):
        if ch == '#':
            active.add((x, y, z))


def get_neighbours(cube: Tuple[int, int, int]
                   ) -> Iterator[Tuple[int, int, int]]:
    """Return all neighbours of cube."""
    for x in range(cube[0] - 1, cube[0] + 2):
        for y in range(cube[1] - 1, cube[1] + 2):
            for z in range(cube[2] - 1, cube[2] + 2):
                n = (x, y, z)
                if n == cube:
                    continue

                yield n


for cycle in range(0, 6):

    print('Cycle', cycle + 1)

    next_active = set()
    non_active_to_check = set()

    for a in active:
        active_count = 0
        for n in get_neighbours(a):
            if n in active:
                active_count += 1
            else:
                non_active_to_check.add(n)

        if active_count == 2 or active_count == 3:
            next_active.add(a)

    for n in non_active_to_check:
        active_count = 0
        for nn in get_neighbours(n):
            if nn in active:
                active_count += 1
                if active_count > 3:
                    break

        if active_count == 3:
            next_active.add(n)

    active = next_active

print('Answer 1:', len(active))


active = set()

z = 0
w = 0
for x, row in enumerate(inp_string.split("\n")):
    for y, ch in enumerate(row):
        if ch == '#':
            active.add((x, y, z, w))


def get_neighbours2(cube: Tuple[int, int, int, int]
                    ) -> Iterator[Tuple[int, int, int, int]]:
    """Return all neighbours of cube."""
    for x in range(cube[0] - 1, cube[0] + 2):
        for y in range(cube[1] - 1, cube[1] + 2):
            for z in range(cube[2] - 1, cube[2] + 2):
                for w in range(cube[3] - 1, cube[3] + 2):
                    n = (x, y, z, w)
                    if n == cube:
                        continue

                    yield n


for cycle in range(0, 6):

    print('Cycle', cycle + 1)

    next_active = set()
    non_active_to_check = set()

    for a in active:
        active_count = 0
        for n in get_neighbours2(a):
            if n in active:
                active_count += 1
            else:
                non_active_to_check.add(n)

        if active_count == 2 or active_count == 3:
            next_active.add(a)

    for n in non_active_to_check:
        active_count = 0
        for nn in get_neighbours2(n):
            if nn in active:
                active_count += 1
                if active_count > 3:
                    break

        if active_count == 3:
            next_active.add(n)

    active = next_active

print('Answer 2:', len(active))
