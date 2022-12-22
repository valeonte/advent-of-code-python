# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 18.

Created on Wed Dec 21 21:54:24 2022

@author: Eftychios
"""

import os

from typing import Iterator
from functools import lru_cache


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

with open("inputs/day-18.txt", "r") as f:
    inp_string = f.read()


inp = set()
for row in inp_string.split('\n'):
    inp.add(tuple([int(r) for r in row.split(',')]))


def get_adjacent(t: tuple[int, int, int]) -> Iterator[tuple[int, int, int]]:
    """Return all adjacent cubes."""
    ads = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for a in ads:
        yield (t[0] + a[0], t[1] + a[1], t[2] + a[2])
        yield (t[0] - a[0], t[1] - a[1], t[2] - a[2])


exposed = 0
for cube in inp:
    for adj in get_adjacent(cube):
        if adj not in inp:
            exposed += 1

print('Answer 1:', exposed)


x_lim = {min([t[0] for t in inp]), max([t[0] for t in inp])}

y_lim = {min([t[1] for t in inp]), max([t[1] for t in inp])}

z_lim = {min([t[2] for t in inp]), max([t[2] for t in inp])}


@lru_cache(maxsize=65536)
def has_way_out(t: tuple[int, int, int]) -> bool:
    """Check whether the point has a way out."""
    if t in inp:
        return False

    if t[0] in x_lim or t[1] in y_lim or t[2] in z_lim:
        return True

    print('Checking adjacent of', t)
    for adj in get_adjacent(t):
        if has_way_out(adj):
            return True

    return False


have_way_out = dict()
trapped = set()
cnt = 0
while True:
    cnt += 1
    iters = 0
    pre_size = len(have_way_out)
    for x in range(min(x_lim), max(x_lim) + 1):
        for y in range(min(y_lim), max(y_lim) + 1):
            for z in range(min(z_lim), max(z_lim) + 1):
                iters+=1
                t = (x, y, z)
                if t in have_way_out:
                    continue
                if t in inp:
                    have_way_out[t] = None
                    continue

                if t[0] in x_lim or t[1] in y_lim or t[2] in z_lim:
                    have_way_out[t] = True
                    continue

                way_out = False
                checked_all = True
                for adj in get_adjacent(t):
                    if adj in inp:
                        continue

                    if adj in have_way_out:
                        if have_way_out[adj]:
                            way_out = True
                            break
                    else:
                        checked_all = False

                if way_out:
                    have_way_out[t] = True
                else:
                    if checked_all:
                        trapped.add(t)
                        have_way_out[t] = False

    if len(have_way_out) == pre_size:
        print('No assigned in iteration, job done!')
        break

    print('Assigned', len(have_way_out) - pre_size, 'cubes in iteration',
          cnt, 'with current size', len(have_way_out))

print('Found', len(trapped), 'trapped air cubes')

# All cubes that do not exist in the dict, are also trapped
for x in range(min(x_lim), max(x_lim) + 1):
    for y in range(min(y_lim), max(y_lim) + 1):
        for z in range(min(z_lim), max(z_lim) + 1):
            t = (x, y, z)
            if t in have_way_out:
                continue
            have_way_out[t] = False
            trapped.add(t)

exposed = 0
for cube in inp:
    for adj in get_adjacent(cube):
        if adj not in inp and adj not in trapped:
            exposed += 1

print('Answer 2:', exposed)
len(have_way_out)
