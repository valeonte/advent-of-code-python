"""
Advent of Code 2023 day 22.

Created on Sun Dec 24 2023 4:19:19 PM

@author: Eftychios
"""

import os
import json
import re
import math

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, Set, Iterator, Dict, List
from dataclasses import dataclass, replace, field
from enum import Enum
from functools import cache

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


with open("inputs/day-22.txt", "r") as f:
    inp_string = f.read()

inps = inp_string.split('\n')


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Block:
    name: str
    c1: Cube
    c2: Cube

    @property
    def min_x(self) -> int:
        return self.c1.x if self.c1.x <= self.c2.x else self.c2.x
    @property
    def max_x(self) -> int:
        return self.c1.x if self.c1.x > self.c2.x else self.c2.x
    @property
    def min_y(self) -> int:
        return self.c1.y if self.c1.y <= self.c2.y else self.c2.y
    @property
    def max_y(self) -> int:
        return self.c1.y if self.c1.y > self.c2.y else self.c2.y
    @property
    def min_z(self) -> int:
        return self.c1.z if self.c1.z <= self.c2.z else self.c2.z
    @property
    def max_z(self) -> int:
        return self.c1.z if self.c1.z > self.c2.z else self.c2.z

    def overlaps(self, other: 'Block') -> bool:
        """Check whether the block is overlapping looking from above."""
        return self.min_x <= other.max_x and self.max_x >= other.min_x \
            and self.min_y <= other.max_y and self.max_y >= other.min_y

    def supports(self, other: 'Block') -> bool:
        """Check whether self supports other."""
        if not self.overlaps(other):
            return False
        return self.max_z == other.min_z - 1


def name_generator() -> Iterator[str]:
    for rep in range(1, 100):
        for ch in range(ord('A'), ord('Z') + 1):
            yield chr(ch) * rep


blocks = []
pat = re.compile(r'^(?P<x1>\d+),(?P<y1>\d+),(?P<z1>\d+)~(?P<x2>\d+),(?P<y2>\d+),(?P<z2>\d+)$')
name_iter = iter(name_generator())
for row in inps:
    m = pat.match(row)

    c1 = Cube(int(m.group('x1')), int(m.group('y1')), int(m.group('z1') ))
    c2 = Cube(int(m.group('x2')), int(m.group('y2')), int(m.group('z2') ))

    blocks.append(Block(next(name_iter), c1, c2))

print('Landing all blocks', dt.datetime.now())
landed_blocks = []
# Iterate sorted by the one closest to the ground
for i, b in enumerate(sorted(blocks, key=lambda x: x.min_z)):
    lowest_z = 1
    for lb in landed_blocks:
        if lb.max_z < lowest_z:
            continue
        if lb.overlaps(b):
            if lowest_z < lb.max_z + 1:
                lowest_z = lb.max_z + 1
    drop_by = b.min_z - lowest_z
    if drop_by > 0:
        # print('Dropping', b, 'by', drop_by)
        c1 = replace(b.c1, z=b.c1.z-drop_by)
        c2 = replace(b.c2, z=b.c2.z-drop_by)
        landed_blocks.append(replace(b, c1=c1, c2=c2))
    else:
        # print('Leaving', b, 'as is')
        landed_blocks.append(b)

print('Working out supporters', dt.datetime.now())
supports = {b:[] for b in landed_blocks}
supported_by = {b:[] for b in landed_blocks}
for i, b1 in enumerate(landed_blocks):
    for b2 in landed_blocks[i:]:
        if not b1.overlaps(b2):
            continue
        if b1.supports(b2):
            supports[b1].append(b2)
            supported_by[b2].append(b1)
        elif b2.supports(b1):
            supports[b2].append(b1)
            supported_by[b1].append(b2)

print('Working out goners', dt.datetime.now())
can_disintegrate = 0
for b in landed_blocks:
    can_go = True
    for sup in supports[b]:
        if len(supported_by[sup]) == 1:
            can_go = False
            break
    if can_go:
        can_disintegrate += 1

print('Done?', dt.datetime.now())

print('Answer 1:', can_disintegrate)


def find_fallers(b: Block) -> int:
    """Find the number of bricks that will fall if we disintegrate b."""
    fallers = {b}
    fallers_increased = True
    while fallers_increased:
        fallers_increased = False
        for bb in landed_blocks:
            if bb in fallers or bb.min_z == 1:
                continue
            all_supporters_fallen = True
            for sup_by in supported_by[bb]:
                if sup_by not in fallers:
                    all_supporters_fallen = False
                    break
            if all_supporters_fallen:
                fallers.add(bb)
                fallers_increased = True

    return len(fallers) - 1


print('Answer 2:', sum([find_fallers(b) for b in landed_blocks]))
