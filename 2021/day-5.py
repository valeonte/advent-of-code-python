# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 5.

Created on Sun Dec  5 16:50:12 2021

@author: Eftychios
"""

import os

import numpy as np

from dataclasses import dataclass


@dataclass
class Line:
    """Line representation."""

    x1: int
    y1: int

    x2: int
    y2: int

    @classmethod
    def from_pair(cls, p1: str, p2: str):
        """Create a line from a pair of points."""
        p1 = p1.split(',')
        p2 = p2.split(',')

        return cls(x1=int(p1[0]), y1=int(p1[1]),
                   x2=int(p2[0]), y2=int(p2[1]))


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

with open("inputs/day-5.txt", "r") as f:
    inp_string = f.read()

inp = []

for line in inp_string.split("\n"):
    p = line.split(' ')

    inp.append(Line.from_pair(p[0], p[-1]))


cross_points = dict()
for line in inp:
    if line.x1 == line.x2:
        for y in range(min(line.y1, line.y2), max(line.y1, line.y2) + 1):
            point = (line.x1, y)
            if point in cross_points:
                cross_points[point] = cross_points[point] + 1
            else:
                cross_points[point] = 1
    elif line.y1 == line.y2:
        for x in range(min(line.x1, line.x2), max(line.x1, line.x2) + 1):
            point = (x, line.y1)
            if point in cross_points:
                cross_points[point] = cross_points[point] + 1
            else:
                cross_points[point] = 1

print('Answer 1:', sum([x > 1 for x in cross_points.values()]))


cross_points = dict()
for line in inp:
    if line.x1 == line.x2:
        for y in range(min(line.y1, line.y2), max(line.y1, line.y2) + 1):
            point = (line.x1, y)
            if point in cross_points:
                cross_points[point] = cross_points[point] + 1
            else:
                cross_points[point] = 1
    elif line.y1 == line.y2:
        for x in range(min(line.x1, line.x2), max(line.x1, line.x2) + 1):
            point = (x, line.y1)
            if point in cross_points:
                cross_points[point] = cross_points[point] + 1
            else:
                cross_points[point] = 1
    else:
        dist = abs(line.x2 - line.x1)
        step_x = -1 if line.x1 > line.x2 else 1
        step_y = -1 if line.y1 > line.y2 else 1

        for i in range(dist + 1):
            point = (line.x1 + i * step_x, line.y1 + i * step_y)
            if point in cross_points:
                cross_points[point] = cross_points[point] + 1
            else:
                cross_points[point] = 1

print('Answer 2:', sum([x > 1 for x in cross_points.values()]))
