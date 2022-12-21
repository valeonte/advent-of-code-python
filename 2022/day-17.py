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

# with open("inputs/day-17.txt", "r") as f:
#     inp_string = f.read()


rocks = [[(2, 0), (3, 0), (4, 0), (5, 0)],  # dash
         [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)],  # plus
         [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)],  # reverse L
         [(2, 0), (2, 1), (2, 2), (2, 3)], # I
         [(2, 0), (3, 0), (2, 1), (3, 1)]]  # square


def infinite_jets() -> Iterator[int]:
    while True:
        for ch in inp_string:
            yield -1 if ch == '<' else 1


def infinite_rocks() -> Iterator[List[Tuple[int, int]]]:
    while True:
        for rock in rocks:
            yield rock


def print_rocks(stopped: Set[Tuple[int, int]],
                rock: List[Tuple[int, int]]):
    ret = ''
    max_y = min(5000, max([r[1] for r in rock]))
    for y in range(max_y, -1, -1):
        for x in range(9):
            if x == 0:
                ret += '|'
            elif x == 8:
                ret += '|\n'
            elif (x - 1, y) in stopped:
                ret += '#'
            elif (x - 1, y) in rock:
                ret += '@'
            else:
                ret += '.'

    ret += '+-------+'
    print(ret)
    print()


stopped = set()
stopped_list = []

fallen_rocks = 0
rock_idx = 0

rock_gen = iter(infinite_rocks())
jet_gen = iter(infinite_jets())

rock_is_moving = False
highest_rock = -1
last_time = time()
start_time = last_time

max_rocks = 1000000

heights = []

while fallen_rocks <= max_rocks:
    if not rock_is_moving:
        fallen_rocks += 1
        if fallen_rocks == max_rocks:
            print('stop')

        heights.append(highest_rock)
        if max_rocks > 100 and fallen_rocks % (max_rocks // 20) == 0:
            t = time()
            print(f'{fallen_rocks} fallen rocks in {t - last_time:.2f}')
            last_time = t

        rock_is_moving = True
        next_rock = next(rock_gen)
        rock = []
        for r in next_rock:
            rock.append((r[0], r[1] + highest_rock + 4))

    # First move from jet
    jet = next(jet_gen)
    moved_rock = []
    crashed = False
    for r in rock:
        new_x = r[0] + jet
        new_bit = (new_x, r[1])
        if new_x < 0 or new_x > 6 or new_bit in stopped:
            crashed = True
            break
        moved_rock.append(new_bit)

    if not crashed:
        rock = moved_rock

    # Then try dropping one
    moved_rock = []
    crashed = False
    for r in rock:
        new_bit = (r[0], r[1] - 1)
        crashed = new_bit in stopped or new_bit[1] < 0
        if crashed:
            rock_is_moving = False
            break
        moved_rock.append(new_bit)

    if rock_is_moving:
        rock = moved_rock
    else:
        for r in rock:
            if r[1] >= highest_rock:
                highest_rock = r[1]
            stopped.add(r)
            stopped_list.append(r)
        if len(stopped) > 1000000:
            stopped_list = stopped_list[500000:]
            stopped = set(stopped_list)


print('Answer 1:', highest_rock + 1)

print_rocks(stopped, rock)
