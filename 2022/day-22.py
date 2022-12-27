# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 22.

Created on Sun Dec 25 11:18:42 2022

@author: Eftychios
"""

import os
import math

import datetime as dt

from typing import Iterator
from dataclasses import dataclass, replace

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

with open("inputs/day-22.txt", "r") as f:
    inp_string = f.read()


walls = set()
free = set()

max_row = 0
max_col = 0

for row_idx, row in enumerate(inp_string.split('\n')):
    if len(row) == 0:
        max_row = row_idx - 1
        continue

    if row[0].isnumeric():
        instr = row
        break

    if len(row) - 1 > max_col:
        max_col = len(row) - 1

    for col_idx, ch in enumerate(row):
        if ch == '.':
            free.add((row_idx, col_idx))
        elif ch == '#':
            walls.add((row_idx, col_idx))


def do_move(pos: tuple[int, int], move: int, facing: str) -> tuple[int, int]:
    while move > 0:
        move -= 1

        if facing == 'E':
            new_pos = (pos[0], pos[1] + 1)
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out on the right
                first = (pos[0], 0)
                while first not in free and first not in walls:
                    first = (pos[0], first[1] + 1)
                if first in walls:
                    break
                pos = first
            else:
                pos = new_pos

        elif facing == 'W':
            new_pos = (pos[0], pos[1] - 1)
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out on the left
                last = (pos[0], max_col)
                while last not in free and last not in walls:
                    last = (pos[0], last[1] - 1)
                if last in walls:
                    break
                pos = last
            else:
                pos = new_pos

        elif facing == 'S':
            new_pos = (pos[0] + 1, pos[1])
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out at the bottom
                first = (0, pos[1])
                while first not in free and first not in walls:
                    first = (first[0] + 1, pos[1])
                if first in walls:
                    break
                pos = first
            else:
                pos = new_pos

        else:  # facing == 'N'
            new_pos = (pos[0] - 1, pos[1])
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out at the top
                first = (max_row, pos[1])
                while first not in free and first not in walls:
                    first = (first[0] - 1, pos[1])
                if first in walls:
                    break
                pos = first
            else:
                pos = new_pos

    return pos


face_dict = dict(ER='S', SR='W', WR='N', NR='E',
                 EL='N', NL='W', WL='S', SL='E')
facing_value = dict(E=0, S=1, W=2, N=3)

pos = (0, 0)
while pos not in free:
    pos = (0, pos[1] + 1)

facing = 'E'
move = 0
for i, ch in enumerate(instr):
    if i % 1000 == 0:
        print('Processed', i, 'command characters')

    if ch.isnumeric():
        move = move * 10 + int(ch)
        continue

    # We got the move number, move, then switch direction
    pos = do_move(pos, move, facing)
    facing = face_dict[facing + ch]
    move = 0

# final move
pos = do_move(pos, move, facing)


print('Answer 1:', 1000 * (pos[0] + 1) + 4 * (pos[1] + 1)
      + facing_value[facing])



def do_move2(pos: tuple[int, int], move: int,
             facing: str) -> tuple[tuple[int, int], str]:
    while move > 0:
        move -= 1

        if facing == 'E':
            new_pos = (pos[0], pos[1] + 1)
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out on the right
                if pos[0] < 50:
                    new_pos = (50 - pos[0] + 100 - 1, 99)
                    new_facing = 'W'
                elif pos[0] < 100:
                    new_pos = (49, pos[0] + 50)
                    new_facing = 'N'
                elif pos[0] < 150:
                    new_pos = (50 - (pos[0] - 100) - 1, 149)
                    new_facing = 'W'
                else:
                    new_pos = (149, pos[0] - 100)
                    new_facing = 'N'
                if new_pos in walls:
                    break
                facing = new_facing
            pos = new_pos

        elif facing == 'W':
            new_pos = (pos[0], pos[1] - 1)
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out on the left
                if pos[0] < 50:
                    new_pos = (50 - pos[0] + 100 - 1, 0)
                    new_facing = 'E'
                elif pos[0] < 100:
                    new_pos = (100, pos[0] - 50)
                    new_facing = 'S'
                elif pos[0] < 150:
                    new_pos = (50 - (pos[0] - 100) - 1, 50)
                    new_facing = 'E'
                else:
                    new_pos = (0, pos[0] - 100)
                    new_facing = 'S'
                if new_pos in walls:
                    break
                facing = new_facing
            pos = new_pos

        elif facing == 'S':
            new_pos = (pos[0] + 1, pos[1])
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out at the bottom
                if pos[0] < 50:
                    new_pos = (0, pos[1] + 100)
                    new_facing = 'S'
                elif pos[0] < 100:
                    new_pos = (pos[1] + 100, 49)
                    new_facing = 'W'
                else:
                    new_pos = (pos[1] - 50, 49)
                    new_facing = 'W'
                if new_pos in walls:
                    break
                facing = new_facing
            pos = new_pos

        else:  # facing == 'N'
            new_pos = (pos[0] - 1, pos[1])
            if new_pos in walls:
                break
            if new_pos not in free:  # fell out at the top
                if pos[0] < 50:
                    new_pos = (pos[1] + 50, 50)
                    new_facing = 'E'
                elif pos[0] < 100:
                    new_pos = (pos[1] + 100, 0)
                    new_facing = 'E'
                else:
                    new_pos = (pos[1] - 100, 199)
                    new_facing = 'N'
                if new_pos in walls:
                    break
                facing = new_facing
            pos = new_pos

    return pos, facing


face_dict = dict(ER='S', SR='W', WR='N', NR='E',
                 EL='N', NL='W', WL='S', SL='E')
facing_value = dict(E=0, S=1, W=2, N=3)

pos = (0, 0)
while pos not in free:
    pos = (0, pos[1] + 1)

facing = 'E'
move = 0
for i, ch in enumerate(instr):
    if i % 1000 == 0:
        print('Processed', i, 'command characters')

    if ch.isnumeric():
        move = move * 10 + int(ch)
        continue

    # We got the move number, move, then switch direction
    pos, facing = do_move2(pos, move, facing)
    facing = face_dict[facing + ch]
    move = 0

# final move
pos, facing = do_move2(pos, move, facing)


print('Answer 2:', 1000 * (pos[0] + 1) + 4 * (pos[1] + 1)
      + facing_value[facing])

