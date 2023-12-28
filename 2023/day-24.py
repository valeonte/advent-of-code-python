"""
Advent of Code 2023 day 24.

Created on Wed Dec 27 2023 9:56:50 AM

@author: Eftychios
"""

import os
import json
import re
import math
import logging

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, Set, Iterator, Dict, List
from dataclasses import dataclass, replace, field
from enum import Enum
from functools import cache

logging.basicConfig(format='%(asctime)s: %(name)s|%(levelname)s|%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """19, 13, 30 @ -2, 1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @ 1, -5, -3"""

min_d, max_d = 7, 27


# with open("inputs/day-24.txt", "r") as f:
#     inp_string = f.read()
# min_d, max_d = 200000000000000, 400000000000000

part1 = False

inps = inp_string.split('\n')


@dataclass
class Hailstone:
    px: int
    py: int
    pz: int

    vx: int
    vy: int
    vz: int

    @staticmethod
    def t_range_within_bounds(min_d: int, max_d: int, pd: int, vd: int):
        """Detarming at what times dimension d will be within bounds."""
        if vd > 0:
            min_t = (min_d - pd) / vd
            max_t = (max_d - pd) / vd
        else:
            min_t = (max_d - pd) / vd
            max_t = (min_d - pd) / vd

        if max_t < 0:
            return None
        if min_t < 0:
            min_t = 0
        
        return min_t, max_t

    def t_range_x_within_bounds(self, min_x: int, max_x: int) -> Tuple[int, int]:
        """Determine at between what times x will be within bounds."""
        return self.t_range_within_bounds(min_x, max_x, self.px, self.vx)

    def t_range_y_within_bounds(self, min_y: int, max_y: int) -> Tuple[int, int]:
        """Determine at between what times x will be within bounds."""
        return self.t_range_within_bounds(min_y, max_y, self.py, self.vy)
    
    def get_equation_a_b(self) -> Tuple[int, int]:
        """Assuming equation of X/Y line is y = ax + b, this calculates a and b."""
        a = self.vy / self.vx
        b = self.py - a * self.px
        return a, b
    
    def crosses_at(self, other: 'Hailstone') -> Tuple[int, int]:
        """Get the point where the paths cross."""
        a1, b1 = self.get_equation_a_b()
        a2, b2 = other.get_equation_a_b()

        if a1 == a2:
            # Lines do not cross
            return None

        x = (b2 - b1)/(a1 - a2)
        y = a1 * x + b1

        return x, y
    
    def time_at_x_y(self, x: int, y: int) -> int:
        """At what time t, will the hailstone be at x, y."""
        if self.vx != 0:
            return (x - self.px) / self.vx
        return (y - self.py) / self.vy


pat = re.compile(r'^(?P<px>[\-\d]+), (?P<py>[\-\d]+), (?P<pz>[\-\d]+) @ (?P<vx>[\-\d]+), (?P<vy>[\-\d]+), (?P<vz>[\-\d]+)$')

hailstones = []
for inp in inps:
    m = pat.match(inp)
    h = Hailstone(int(m.group('px')), int(m.group('py')), int(m.group('pz')),
                  int(m.group('vx')), int(m.group('vy')), int(m.group('vz')))
    hailstones.append(h)


if part1:

    crossing_within = 0

    for i, h1 in enumerate(hailstones):
        for h2 in hailstones[i + 1:]:
            t_x1 = h1.t_range_x_within_bounds(min_d, max_d)
            if t_x1 is None:
                log.info('%s x not within bounds on time', h1)
                continue
            t_x2 = h2.t_range_x_within_bounds(min_d, max_d)
            if t_x2 is None:
                log.info('%s x not within bounds on time', h2)
                continue
            t_y1 = h1.t_range_y_within_bounds(min_d, max_d)
            if t_y1 is None:
                log.info('%s y not within bounds on time', h1)
                continue
            t_y2 = h2.t_range_y_within_bounds(min_d, max_d)
            if t_y2 is None:
                log.info('%s y not within bounds on time', h2)
                continue

            min_x1, max_x1 = t_x1
            min_x2, max_x2 = t_x2
            min_y1, max_y1 = t_y1
            min_y2, max_y2 = t_y2

            c = h1.crosses_at(h2)
            if c is None:
                log.info('%s never crosses %s', h1, h2)
                continue
            x, y = c
            t1 = h1.time_at_x_y(x, y)
            t2 = h2.time_at_x_y(x, y)
            log.info('%s crosses %s at %.1f/%.1f in %.1fns and %.1f', h1, h2, x, y, t1, t2)
            if min_d <= x and x <= max_d and min_d <= y and y <= max_d and t1 >= 0 and t2 >= 0:
                crossing_within += 1

    log.info('Answer 1: %d', crossing_within)




log.info('Done?')
