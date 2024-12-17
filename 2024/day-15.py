"""
Advent of Code 2024 day 15.

Created on Mon Dec 16 2024 9:35:24 PM

@author: Eftychios
"""

import re
import os
import math

import datetime as dt
import numpy as np

from functools import lru_cache
from typing import Dict, Iterable, List, Set, Tuple
from dataclasses import dataclass
from decimal import Decimal
from tqdm import tqdm
from common import Dir


os.chdir("C:/Repos/advent-of-code-python/2024")


inp_string = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


inp_string = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""


inp_string = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

inp_string = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


with open("inputs/day-15.txt", "r") as f:
    inp_string = f.read()

map_rows = []
movements = []

robot = None

for y, inp in enumerate(inp_string.split('\n')):
    if inp.startswith('#'):
        # warehouse map
        row = np.zeros((1, len(inp)))
        for x, ch in enumerate(inp):
            if ch == '#':
                row[0, x] = -1
            elif ch == 'O':
                row[0, x] = 1
            elif ch == '@':
                robot = x, y
        
        map_rows.append(row)
    elif len(inp) == 0:
        continue
    else:
        # movements
        for ch in inp:
            if ch == '<':
                d = Dir.W
            elif ch == '>':
                d = Dir.E
            elif ch == '^':
                d = Dir.N
            elif ch == 'v':
                d = Dir.S
            else:
                raise Exception('NO!')
            movements.append(d)

assert robot is not None, 'NO ROBOT!'

full_map = np.concatenate(map_rows)


def print_map():
    for y, row in enumerate(full_map):
        for x, el in enumerate(row):
            ch = '.'
            if (x, y) == robot:
                ch = '@'
            elif el == -1:
                ch = '#'
            elif el == 1:
                ch = 'O'
            elif el == 2:
                ch = '['
            elif el == 3:
                ch = ']'
            print(ch, end='')
        print()


def move_if_you_can(start_pos: Tuple[int, int], dir: Dir) -> Tuple[int, int]:
    dx, dy = 0, 0
    if dir == Dir.E:
        dx = 1
    elif dir == Dir.W:
        dx = -1
    elif dir == Dir.N:
        dy = -1
    elif dir == Dir.S:
        dy = 1
    else:
        raise Exception('AA')

    dest = start_pos[0] + dy, start_pos[1] + dx
    if full_map[dest] == -1:
        return None

    if full_map[dest] == 0:
        full_map[dest] = full_map[start_pos]
        full_map[start_pos] = 0
        return dest

    # dest is a box
    dest_move = move_if_you_can(dest, dir)
    if dest_move is None:
        # dest could not move
        return None

    # dest moved, we move
    full_map[dest] = full_map[start_pos]
    full_map[start_pos] = 0
    return dest


#print_map()

for m in movements:
    dest = move_if_you_can(robot, m)
    if dest is not None:
        robot = dest

#print_map()


ret = 0

for y, row in enumerate(full_map):
    for x, el in enumerate(row):
        if el == 1:
            ret += 100*y+x


print('Answer 1:', ret)


#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#

map_rows = []
movements = []
robot = None

for y, inp in enumerate(inp_string.split('\n')):
    if inp.startswith('#'):
        # warehouse map
        row = np.zeros((1, len(inp)))
        for x, ch in enumerate(inp):
            if ch == '#':
                row[0, x] = -1
            elif ch == 'O':
                row[0, x] = 1
            elif ch == '@':
                robot = x, y
        
        map_rows.append(row)
    elif len(inp) == 0:
        continue
    else:
        # movements
        for ch in inp:
            if ch == '<':
                d = Dir.W
            elif ch == '>':
                d = Dir.E
            elif ch == '^':
                d = Dir.N
            elif ch == 'v':
                d = Dir.S
            else:
                raise Exception('NO!')
            movements.append(d)

assert robot is not None, 'NO ROBOT!'

full_map = np.concatenate(map_rows)
ext_full_map = np.zeros((full_map.shape[0], 2*full_map.shape[1]))

print_map()

print('Enhancing map')

for y, row in enumerate(full_map):
    for x, el in enumerate(row):
        ext_x = 2*x
        if el == -1:
            ext_full_map[y, ext_x:ext_x+2] = -1
        elif el == 1:
            ext_full_map[y, ext_x:ext_x+2] = [2, 3]

robot = (2*robot[0], robot[1])

full_map = ext_full_map

print_map()


def move_if_you_can2(start_pos: Tuple[int, int], dir: Dir) -> Tuple[int, int]:
    dx, dy = 0, 0
    if dir == Dir.E:
        dx = 1
    elif dir == Dir.W:
        dx = -1
    elif dir == Dir.N:
        dy = -1
    elif dir == Dir.S:
        dy = 1
    else:
        raise Exception('AA')

    can_move = True
    pending = [start_pos]
    checked = set()
    movables = []

    while can_move and len(pending) > 0:
        node = pending.pop(0)
        if node in checked:
            continue
        checked.add(node)

        src = full_map[node[1], node[0]]
        if src == -1:
            can_move = False
            break
        if src == 0 and node != robot:
            # Empty space, nothing to move, all good
            continue
        movables.append(node)

        # First examine other half of potential box
        if src == 2:
            pending.append((node[0] + 1, node[1]))
        elif src == 3:
            pending.append((node[0] - 1, node[1]))
        
        # then destination
        dest = (node[0] + dx, node[1] + dy)
        pending.append(dest)

    if not can_move:
        return None
    
    # Do the moves from last to first, and return first destination
    movables.reverse()
    for node in movables:
        dest = (node[0] + dx, node[1] + dy)
        full_map[dest[1], dest[0]] = full_map[node[1], node[0]]
        full_map[node[1], node[0]] = 0
    
    return dest


for m in movements:
    dest = move_if_you_can2(robot, m)
    if dest is not None:
        robot = dest

print_map()

ret = 0

for y, row in enumerate(full_map):
    for x, el in enumerate(row):
        if el == 2:
            ret += 100*y+x


print('Answer 2:', ret)