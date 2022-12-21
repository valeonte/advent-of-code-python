# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 17.

Created on Tue Dec 20 18:35:37 2022

@author: Eftychios
"""

import os
import re
from time import time

import numpy as np
import pandas as pd

from typing import List, Set, Iterator, Tuple
from random import shuffle


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

with open("inputs/day-17.txt", "r") as f:
    inp_string = f.read()


nrocks = [[0b11110],
          [0b01000,
           0b11100,
           0b01000],
          [0b11100,
           0b00100,
           0b00100],
          [0b10000,
           0b10000,
           0b10000,
           0b10000],
          [0b11000,
           0b11000]]


def infinite_jets() -> Iterator[int]:
    while True:
        for ch in inp_string:
            yield ch


def infinite_rocks() -> Iterator[List[int]]:
    while True:
        yield nrocks[0]
        yield nrocks[1]
        yield nrocks[2]
        yield nrocks[3]
        yield nrocks[4]
        # for rock in nrocks:
        #     yield rock.copy()


def print_rocks(rocks: List[int],
                rock: List[int] = [0],
                rock_idx: int = -1):
#    if len(rocks) > 20:
    return
    ret = ''
    if rock_idx == -1:
        rock_idx = len(rocks)

    y_max = -1
    rock_lines = dict()
    for i, r in enumerate(rock):
        rock_lines[i + rock_idx] = r
        if i + rock_idx > y_max:
            y_max = i + rock_idx

    rocks_lines = dict()
    for i in range(len(rocks) - 1, -1, -1):
        rocks_lines[i] = rocks[i]
        if i > y_max:
            y_max = i

    for y in range(y_max, -1, -1):
        row = ['|'] + ['.'] * 7 + ['|\n']

        if y in rocks_lines:
            for i, ch in enumerate(str(bin(rocks_lines[y]))[2:].zfill(7)):
                if ch == '1':
                    row[i + 1] = '#'
        if y in rock_lines:
            for i, ch in enumerate(str(bin(rock_lines[y]))[2:].zfill(7)):
                if ch == '1':
                    row[i + 1] = '@'

        ret += ''.join(row)

    ret += '+-------+'
    print(ret)
    print()


def find_pattern(data: list[int]) -> tuple[list[int], list[int]]:
    for p in range(len(data)):
        sd = data[p:]
        for r in range(2, len(sd) // 2):
            if sd[0:r] == sd[r:2 * r]:
                if all([(sd[0:r] == sd[y:y + r])
                        for y in range(r, len(sd) - r, r)]):
                    return data[:p], data[p:p + r]
    return [], []


rocks = []

fallen_rocks = 0

rock_gen = iter(infinite_rocks())
jet_gen = iter(infinite_jets())

rock_is_moving = False

last_time = time()
start_time = last_time

max_rocks = 10000
extra_height = 0
max_rocks_length = 1000000000
height_diffs = []

while fallen_rocks <= max_rocks:
    if not rock_is_moving:
        fallen_rocks += 1

        if max_rocks > 100 and fallen_rocks % (max_rocks // 20) == 0:
            t = time()
            print(f'{fallen_rocks} fallen rocks in {t - last_time:.2f}')
            last_time = t

        rock_is_moving = True
        rock_idx = len(rocks) + 4
        rock = next(rock_gen)
        # We do first 4 shifts here as there are no objects by design
        for _ in range(4):
            jet = next(jet_gen)
            rock_idx -= 1
            new_rock = []
            if jet == '<':
                for r in rock:
                    if r > 63:
                        new_rock = rock
                        break
                    new_rock.append(r << 1)
            else:
                for r in rock:
                    if r % 2 == 1:
                        new_rock = rock
                        break
                    new_rock.append(r >> 1)
            rock = new_rock
            print_rocks(rocks, rock, rock_idx)

    # Then try dropping one
    if rock_idx > 0:
        # crash check
        new_rock_idx = rock_idx - 1
        for i in range(len(rock)):
            rock_is_moving &= (new_rock_idx + i >= len(rocks)
                               or rock[i] & rocks[new_rock_idx + i] == 0)
            if not rock_is_moving:
                break
    else:
        rock_is_moving = False

    if not rock_is_moving:
        # Rock stopped, we merge it with rocks at the current position
        pre_height = len(rocks)
        for i in range(len(rock)):
            if rock_idx + i >= len(rocks):
                rocks.append(rock[i])
            else:
                rocks[rock_idx + i] |= rock[i]

        height_diffs.append(len(rocks) - pre_height)
        print_rocks(rocks)
        continue

    # We lower the rock_idx, as the piece moves down
    rock_idx -= 1

    # Else move from jet
    jet = next(jet_gen)
    new_rock = []
    crashed = False
    if jet == '<':
        for i, r in enumerate(rock):
            crashed = r > 63 or (rock_idx + i < len(rocks)
                                 and (r << 1) & rocks[rock_idx + i] > 0)
            if crashed:
                break
            new_rock.append(r << 1)
    else:
        for i, r in enumerate(rock):
            crashed = r % 2 == 1 or (rock_idx + i < len(rocks)
                                     and (r >> 1) & rocks[rock_idx + i] > 0)
            if crashed:
                break
            new_rock.append(r >> 1)

    if not crashed:
        rock = new_rock

    print_rocks(rocks, rock, rock_idx)

    if len(rocks) > max_rocks_length:
        trm = max_rocks_length // 2
        rock_idx -= trm
        extra_height += trm
        rocks = rocks[trm:]


#print_rocks(rocks)

offset, pattern = find_pattern(height_diffs)

def calc_rock_height(num_rocks: int):

    rem_rocks = num_rocks - len(offset)
    return (sum(offset) + (rem_rocks // len(pattern)) * sum(pattern)
            + sum(pattern[:rem_rocks % len(pattern)]))


print('Answer 1:', calc_rock_height(2022))
print('Answer 2:', calc_rock_height(1000000000000))
