# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 24.

Created on Mon Dec 26 17:38:53 2022

@author: Eftychios
"""

import os
import sys
import math

import datetime as dt

from typing import Iterator, Set
from dataclasses import dataclass, replace

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

inp_string = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""


with open("inputs/day-24.txt", "r") as f:
    inp_string = f.read()


blizzards = dict()
for row_idx, row in enumerate(inp_string.split('\n')):
    for col_idx, ch in enumerate(row):
        if ch in ['<', '>', '^', 'v']:
            blizzards[(row_idx, col_idx)] = [ch]

min_row = 0
max_row = row_idx
min_col = 0
max_col = len(row) - 1


def print_map(blizzards: dict[tuple[int, int], str],
              elves: Set[tuple[int, int]]):
    for row in range(0, max_row + 1):
        line = ''
        for col in range(0, max_col + 1):
            if (row, col) in elves:
                line += 'E'
            elif (row, col) in blizzards:
                b = blizzards[(row, col)]
                if len(b) == 1:
                    line += b[0]
                else:
                    line += str(len(b))
            elif (col == max_col or col == 0
                      or row == 0 and col != 1
                      or row == max_row and col != max_col - 1):
                line += '#'
            else:
                line += '.'
        print(line)


def move_blizzards(blizzards: dict[tuple[int, int], str]
                   ) -> dict[tuple[int, int], str]:
    new_blizzards = dict()
    for blizz, dirs in blizzards.items():
        for dr in dirs:
            if dr == '>':
                if blizz[1] == max_col - 1:
                    new_blizz = (blizz[0], 1)
                else:
                    new_blizz = (blizz[0], blizz[1] + 1)
            elif dr == '<':
                if blizz[1] == 1:
                    new_blizz = (blizz[0], max_col - 1)
                else:
                    new_blizz = (blizz[0], blizz[1] - 1)
            elif dr == 'v':
                if blizz[0] == max_row - 1:
                    new_blizz = (1, blizz[1])
                else:
                    new_blizz = (blizz[0] + 1, blizz[1])
            elif dr == '^':
                if blizz[0] == 1:
                    new_blizz = (max_row - 1, blizz[1])
                else:
                    new_blizz = (blizz[0] - 1, blizz[1])

            if new_blizz in new_blizzards:
                new_blizzards[new_blizz].append(dr)
            else:
                new_blizzards[new_blizz] = [dr]

    return new_blizzards


def get_potential_next(elf: tuple[int, int]) -> Iterator[tuple[int, int]]:
    yield elf
    yield elf[0] + 1, elf[1]
    yield elf[0] - 1, elf[1]
    yield elf[0], elf[1] + 1
    yield elf[0], elf[1] - 1


entry_point = (0, 1)
exit_point = (max_row, max_col - 1)
elves = {(0, 1)}
minutes = 0

stage = 0

while True:
    minutes += 1
    new_blizzards = move_blizzards(blizzards)

    new_elves = set()
    for elf in elves:
        for nelf in get_potential_next(elf):
            if nelf == entry_point or nelf == exit_point:
                new_elves.add(nelf)
                continue
            if (nelf in new_blizzards
                    or nelf[0] <= 0 or nelf[0] >= max_row
                    or nelf[1] <= 0 or nelf[1] >= max_col):
                continue
            new_elves.add(nelf)

    elves = new_elves
    blizzards = new_blizzards

    # print('After', minutes, 'minutes ----------------------')
    # print_map(blizzards, elves)

    if exit_point in elves and stage == 0:
        print('Got to exit the first time in', minutes, 'minutes, going back')
        answer_1 = minutes
        exit_point = (0, 1)
        entry_point = (max_row, max_col - 1)
        elves = {entry_point}
        stage += 1
    elif exit_point in elves and stage == 1:
        print('Got to entry again in', minutes, 'minutes, going again')
        entry_point = (0, 1)
        exit_point = (max_row, max_col - 1)
        elves = {entry_point}
        stage += 1
    elif exit_point in elves and stage == 2:
        print('Finally got to exit again in', minutes)
        break


print('Answer 1:', answer_1)
print('Answer 2:', minutes)
