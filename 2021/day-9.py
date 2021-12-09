# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 9.

Created on Thu Dec  9 18:35:36 2021

@author: Eftychios
"""

import os

import numpy as np


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """2199943210
3987894921
9856789892
8767896789
9899965678"""

with open("inputs/day-9.txt", "r") as f:
    inp_string = f.read()


inp = np.array([[int(s) for s in list(ss)]
                for ss in inp_string.split("\n")])

height, width = inp.shape

low_points = []
for row in range(height):
    for col in range(width):
        v = inp[row, col]
        is_low_point = ((col == 0 or inp[row, col - 1] > v)
                        and (row == 0 or inp[row - 1, col] > v)
                        and (row == height - 1 or inp[row + 1, col] > v)
                        and (col == width - 1 or inp[row, col + 1] > v))

        if is_low_point:
            low_points.append((row, col))

low_vs = [inp[row, col] for row, col in low_points]
print('Answer 1:', sum(low_vs) + len(low_points))

inp[inp < 9] = 1
inp[inp == 9] = 0


def get_basin_size(row: int, col: int):
    """Get the sum of the point and the surrounding not already counted."""
    if (row < 0 or col < 0 or row >= height or col >= width
            or inp[row, col] == 0):
        return 0

    inp[row, col] = 0
    return (1 + get_basin_size(row, col - 1) + get_basin_size(row - 1, col)
            + get_basin_size(row, col + 1) + get_basin_size(row + 1, col))


basin_sizes = [get_basin_size(row, col)
               for row, col in low_points]

print('Answer 2:', np.prod(sorted(basin_sizes)[-3:]))
