# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 9.

Created on Fri Dec  9 22:22:18 2022

@author: Eftychios
"""

import os

from typing import Tuple


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

inp_string = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

with open("inputs/day-9.txt", "r") as f:
    inp_string = f.read()

def move_tail(tail: Tuple[int, int],
              head: Tuple[int, int]) -> Tuple[int, int]:
    """Get new tail position for given head and tail positions."""
    x_dif = head[0] - tail[0]
    y_dif = head[1] - tail[1]

    if abs(x_dif) < 2 and abs(y_dif) < 2:
        x_dif = 0
        y_dif = 0
    else:
        if abs(x_dif) > 1:
            x_dif = x_dif // 2
        if abs(y_dif) > 1:
            y_dif = y_dif // 2

    new_tail = (tail[0] + x_dif, tail[1] + y_dif)
    #print('H:', head, 'T:', tail, 'NT:', new_tail)
    return new_tail


t = (0, 0)
h = (0, 0)

visited = set()

steps = dict(R=(0, 1), L=(0, -1),
             U=(1, 0), D=(-1, 0))

for row in inp_string.split('\n'):
    print('Moving', row)

    parts = row.split(' ')
    step = steps[parts[0]]
    dist = int(parts[1])

    for _ in range(dist):
        h = (h[0] + step[0], h[1] + step[1])
        t = move_tail(t, h)
        visited.add(t)

print('Answer 1:', len(visited))


knots = [(0, 0) for _ in range(10)]
visited = set()

for row in inp_string.split('\n'):
    print('Moving', row)

    parts = row.split(' ')
    step = steps[parts[0]]
    dist = int(parts[1])

    for _ in range(dist):
        for i in range(9):
            h = knots[i]
            if i == 0:
                h = (h[0] + step[0], h[1] + step[1])
                knots[i] = h

            tail = knots[i + 1]
            new_tail = move_tail(tail, h)
            if tail == new_tail:
                # knot didn't move, break
                print('-', i, knots)
                break
            knots[i + 1] = new_tail
            print(i, knots)

        visited.add(knots[9])

print('Answer 2:', len(visited))
