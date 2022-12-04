# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 4.

Created on Sun Dec  4 09:30:13 2022

@author: Eftychios
"""

import os
import re


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

with open("inputs/day-4.txt", "r") as f:
    inp_string = f.read()


def set_a_contains_b(a_from: int, a_to : int, b_from: int, b_to: int) -> bool:
    """Check whether set a fully contains set b."""
    return a_from <= b_from and a_to >= b_to


def set_a_overlaps_b(a_from: int, a_to : int, b_from: int, b_to: int) -> bool:
    """Check whether set a overlaps set b."""
    return a_from <= b_to and a_to >= b_from


pat = re.compile(r'^(\d+)-(\d+),(\d+)-(\d+)$')

cnt = 0
for row in inp_string.split('\n'):
    m = pat.match(row)
    a_from = int(m.group(1))
    a_to = int(m.group(2))
    b_from = int(m.group(3))
    b_to = int(m.group(4))

    if (set_a_contains_b(a_from, a_to, b_from, b_to)
            or set_a_contains_b(b_from, b_to, a_from, a_to)):
        cnt += 1
        print('Contained found:', row)

print('Answer 1:', cnt)


cnt = 0
for row in inp_string.split('\n'):
    m = pat.match(row)
    a_from = int(m.group(1))
    a_to = int(m.group(2))
    b_from = int(m.group(3))
    b_to = int(m.group(4))

    if set_a_overlaps_b(a_from, a_to, b_from, b_to):
        cnt += 1
        print('Overlapping found:', row)

print('Answer 2:', cnt)
