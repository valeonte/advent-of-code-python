# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 11.

Created on Sat Dec 11 09:49:12 2021

@author: Eftychios
"""

import os

import numpy as np

from typing import Iterator, Tuple

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

with open("inputs/day-11.txt", "r") as f:
    inp_string = f.read()


inp = np.array([[int(s) for s in list(ss)]
                for ss in inp_string.split("\n")])


def adj(arr: np.array, x: int, y: int) -> Iterator[Tuple[int, int]]:
    """Return all adjacent nodes of node."""
    max_x, max_y = arr.shape
    if x > 0:
        yield x - 1, y
        if y > 0:
            yield x - 1, y - 1
        if y < max_y - 1:
            yield x - 1, y + 1
    if x < max_x - 1:
        yield x + 1, y
        if y > 0:
            yield x + 1, y - 1
        if y < max_y - 1:
            yield x + 1, y + 1
    if y > 0:
        yield x, y - 1
    if y < max_y - 1:
        yield x, y + 1


def print_arr(arr: np.array):
    """Print array."""
    print("\n".join([''.join([str(r) for r in row])
                     for row in arr]))


flashes = 0
w = inp
for step in range(100):
    # print_arr(w)
    # input(f'Press for step {step + 1}')

    w = w + 1
    while True:
        new_flashes = 0
        xs, ys = np.nonzero(w > 9)
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            w[x, y] = 0
            new_flashes = new_flashes + 1

            for ax, ay in adj(w, x, y):
                if w[ax, ay] > 0:  # only if it hasn't flased this turn
                    w[ax, ay] = w[ax, ay] + 1

        if new_flashes == 0:
            break
        else:
            flashes = flashes + new_flashes

print('Answer 1:', flashes)


w = inp
step = 0
while True:
    step = step + 1

    w = w + 1
    while True:
        new_flashes = 0
        xs, ys = np.nonzero(w > 9)
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            w[x, y] = 0
            new_flashes = new_flashes + 1

            for ax, ay in adj(w, x, y):
                if w[ax, ay] > 0:  # only if it hasn't flased this turn
                    w[ax, ay] = w[ax, ay] + 1

        if new_flashes == 0:
            break

    if (np.zeros(10) == w).all():
        break

print('Answer 2:', step)
