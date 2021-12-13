# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 13.

Created on Mon Dec 13 19:46:35 2021

@author: Eftychios
"""

import os

from typing import List

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

with open("inputs/day-13.txt", "r") as f:
    inp_string = f.read()

dots = set()
folds = []
for row in inp_string.split('\n'):
    p = row.split(',')
    if len(p) == 2:
        x = int(p[0])
        y = int(p[1])
        dots.add((x, y))

    if row.startswith('fold along'):
        row = row.replace('fold along ', '')
        p = row.split('=')
        folds.append((int(p[0] == 'y'), int(p[1])))


for f in folds:
    dim = f[0]
    line = f[1]

    for dot in list(dots):
        if dot[dim] <= line:
            continue
        new = list(dot)
        new[dim] = line - (dot[dim] - line)
        dots.remove(dot)
        dots.add(tuple(new))
    break

print('Answer 1:', len(dots))


for f in folds:
    dim = f[0]
    line = f[1]

    for dot in list(dots):
        if dot[dim] <= line:
            continue
        new = list(dot)
        new[dim] = line - (dot[dim] - line)
        dots.remove(dot)
        dots.add(tuple(new))


def print_dots():
    """Print out dots."""
    max_x = 0
    max_y = 0
    for dot in dots:
        if dot[0] > max_x:
            max_x = dot[0]
        if dot[1] > max_y:
            max_y = dot[1]

    lines = [' ' * (max_x + 1)] * (max_y + 1)
    for dot in dots:
        ln = list(lines[dot[1]])
        ln[dot[0]] = '#'
        lines[dot[1]] = ''.join(ln)

    for ln in lines:
        print(ln)


print('Answer 2:')
print_dots()
