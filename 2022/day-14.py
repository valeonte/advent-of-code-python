# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 14.

Created on Wed Dec 14 10:48:05 2022

@author: Eftychios
"""

import os

import numpy as np


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

with open("inputs/day-14.txt", "r") as f:
    inp_string = f.read()

rocks = set()
sand = set()

for row in inp_string.split('\n'):
    start = None
    for edge_string in row.split(' -> '):
        edge = eval(edge_string)
        if start is None:
            start = edge
            rocks.add(start)
            continue
        for x in range(start[0] + 1, edge[0] + 1):
            rocks.add((x, start[1]))
        for x in range(start[0] - 1, edge[0] - 1, -1):
            rocks.add((x, start[1]))
        for y in range(start[1] + 1, edge[1] + 1):
            rocks.add((start[0], y))
        for y in range(start[1] - 1, edge[1] - 1, -1):
            rocks.add((start[0], y))
        start = edge


def draw_map():
    ys = [s[1] for s in rocks] + [s[1] for s in sand] + [0]
    xs = [s[0] for s in rocks] + [s[0] for s in sand] + [500]
    min_y = 0
    max_y = max(ys)
    min_x = min(xs)
    max_x = max(xs)

    offset_x = min_x - 1
    offset_y = min_y
    ret = np.zeros((max_y - min_y + 2, max_x - min_x + 3))

    for x, y in rocks:
        ret[y - offset_y, x - offset_x] = 1
    for x, y in sand:
        ret[y - offset_y, x - offset_x] = 2

    ret[- offset_y, 500 - offset_x] = -1

    lines = [''] * ret.shape[0]
    for (y, x), v in np.ndenumerate(ret):
        if v == 0:
            ch = '.'
        elif v == 1:
            ch = '#'
        elif v == 2:
            ch = 'o'
        elif v == -1:
            ch = '+'
        else:
            raise Exception('eee')

        lines[y] += ch

    for line in lines:
        print(line)

    return ret


sand_spilled = False
max_rock_y = max([r[1] for r in rocks])
while not sand_spilled:
    cur_sand = (500, 0)
    sand_rested = False
    while not sand_spilled and not sand_rested:
        if cur_sand[1] > max_rock_y:
            sand_spilled = True
            sand.add(cur_sand)
            break

        test_sand = (cur_sand[0], cur_sand[1] + 1)
        if test_sand not in rocks and test_sand not in sand:
            cur_sand = test_sand
            continue
        test_sand = (cur_sand[0] - 1, cur_sand[1] + 1)
        if test_sand not in rocks and test_sand not in sand:
            cur_sand = test_sand
            continue
        test_sand = (cur_sand[0] + 1, cur_sand[1] + 1)
        if test_sand not in rocks and test_sand not in sand:
            cur_sand = test_sand
            continue

        sand_rested = True

    sand.add(cur_sand)

draw_map()

print('Answer 1:', len(sand) - 1)


rocks = set()
sand = set()

for row in inp_string.split('\n'):
    start = None
    for edge_string in row.split(' -> '):
        edge = eval(edge_string)
        if start is None:
            start = edge
            rocks.add(start)
            continue
        for x in range(start[0] + 1, edge[0] + 1):
            rocks.add((x, start[1]))
        for x in range(start[0] - 1, edge[0] - 1, -1):
            rocks.add((x, start[1]))
        for y in range(start[1] + 1, edge[1] + 1):
            rocks.add((start[0], y))
        for y in range(start[1] - 1, edge[1] - 1, -1):
            rocks.add((start[0], y))
        start = edge


# floor_min_x = min([r[0] for r in rocks]) - 5
# floor_max_x = max([r[0] for r in rocks]) + 5

# for x in range(floor_min_x, floor_max_x + 1):
#     rocks.add((x, max_rock_y + 2))

# draw_map()


full_map = False
while not full_map:
    cur_sand = (500, 0)
    sand_rested = False
    while not full_map and not sand_rested:
        if cur_sand[1] > max_rock_y:
            sand_rested = True
            sand.add(cur_sand)
            break

        test_sand = (cur_sand[0], cur_sand[1] + 1)
        if test_sand not in rocks and test_sand not in sand:
            cur_sand = test_sand
            continue
        test_sand = (cur_sand[0] - 1, cur_sand[1] + 1)
        if test_sand not in rocks and test_sand not in sand:
            cur_sand = test_sand
            continue
        test_sand = (cur_sand[0] + 1, cur_sand[1] + 1)
        if test_sand not in rocks and test_sand not in sand:
            cur_sand = test_sand
            continue

        sand_rested = True
        if cur_sand == (500, 0):
            full_map = True

    sand.add(cur_sand)
#    draw_map()

ret = draw_map()

print('Answer 2:', len(sand))
