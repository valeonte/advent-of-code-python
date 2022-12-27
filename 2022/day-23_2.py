# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 23.

Created on Mon Dec 26 17:18:42 2022

@author: Eftychios
"""

import os
import math

import datetime as dt

from typing import Iterator
from dataclasses import dataclass, replace

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """##
#.
..
##"""

inp_string = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

with open("inputs/day-23.txt", "r") as f:
    inp_string = f.read()

elves = set()
for row_idx, row in enumerate(inp_string.split('\n')):
    for col_idx, ch in enumerate(row):
        if ch == '.':
            continue
        elves.add((row_idx, col_idx))


def get_elf_limits() -> tuple[int, int, int, int]:
    min_row, max_row = 100000, -100000
    min_col, max_col = 100000, -100000
    for e in elves:
        if e[0] < min_row:
            min_row = e[0]
        if e[0] > max_row:
            max_row = e[0]
        if e[1] < min_col:
            min_col = e[1]
        if e[1] > max_col:
            max_col = e[1]

    return min_row, max_row, min_col, max_col


def print_elves():
    min_row, max_row, min_col, max_col = get_elf_limits()
    for row in range(min_row - 1, max_row + 2):
        line = '.'
        for col in range(min_col, max_col + 1):
            if (row, col) in elves:
                line += '#'
            else:
                line += '.'
        print(line + '.')


def can_move(elf: tuple[int, int]) -> list[tuple[int, int]]:
    free = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            target = (elf[0] + i, elf[1] + j)
            if target in elves:
                continue
            free.add(target)

    avail = set()
    if len(free) == 8:
        return avail

    if ((elf[0] - 1, elf[1] - 1) in free
            and (elf[0] - 1, elf[1]) in free
            and (elf[0] - 1, elf[1] + 1)) in free:
        avail.add((elf[0] - 1, elf[1]))

    if ((elf[0] + 1, elf[1] - 1) in free
            and (elf[0] + 1, elf[1]) in free
            and (elf[0] + 1, elf[1] + 1)) in free:
        avail.add((elf[0] + 1, elf[1]))

    if ((elf[0] - 1, elf[1] - 1) in free
            and (elf[0], elf[1] - 1) in free
            and (elf[0] + 1, elf[1] - 1)) in free:
        avail.add((elf[0], elf[1] - 1))

    if ((elf[0] - 1, elf[1] + 1) in free
            and (elf[0], elf[1] + 1) in free
            and (elf[0] + 1, elf[1] + 1)) in free:
        avail.add((elf[0], elf[1] + 1))

    return avail


rnd = 0

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

while True:
    rnd += 1
    if rnd % 100 == 0:
        print('Round', rnd, 'and counting')

    elf_targets = dict()
    target_elves = dict()
    duplicates = set()
    for elf in elves:
        elf_moves = can_move(elf)
        if len(elf_moves) == 0:
            continue
        for d in dirs:
            target = (elf[0] + d[0], elf[1] + d[1])
            if target in elf_moves:
                break
        if target in duplicates:
            continue

        if target in target_elves:
            duplicates.add(target)
            dup_elf = target_elves.pop(target)
            elf_targets.pop(dup_elf)
            continue

        target_elves[target] = elf
        elf_targets[elf] = target

    if len(elf_targets) == 0:
        break

    new_elves = set()
    for elf in elves:
        if elf in elf_targets:
            new_elves.add(elf_targets[elf])
        else:
            new_elves.add(elf)

    elves = new_elves
    dirs.append(dirs.pop(0))


print('Answer 2:', rnd)
