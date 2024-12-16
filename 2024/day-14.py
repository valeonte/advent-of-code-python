"""
Advent of Code 2024 day 14.

Created on Sun Dec 15 2024 10:29:15 AM

@author: Eftychios
"""

import re
import os
import math

import datetime as dt

from functools import lru_cache
from typing import Dict, Iterable, List, Set, Tuple
from dataclasses import dataclass
from decimal import Decimal
from tqdm import tqdm


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

# inp_string = """p=5,0 v=3,-3
# p=4,1 v=-1,-3
# p=6,1 v=-1,2
# p=3,2 v=2,-1
# p=7,2 v=1,3
# p=2,3 v=-2,-2
# p=8,3 v=-1,-3
# p=1,4 v=-1,-2
# p=9,4 v=2,3
# p=0,5 v=-1,2
# p=10,5 v=2,-3
# p=5,6 v=-3,-3"""

space_width = 11
space_height = 7

with open("inputs/day-14.txt", "r") as f:
    inp_string = f.read()
space_width = 101
space_height = 103


@dataclass
class Robot:
    px: int
    py: int

    vx: int
    vy: int

    @classmethod
    def from_line(cls, line: str) -> 'Robot':
        pv = line.split(' ')
        px, py = tuple([int(p) for p in pv[0][2:].split(',')])
        vx, vy = tuple([int(v) for v in pv[1][2:].split(',')])

        return cls(px, py, vx, vy)
    
    def move(self, seconds: int, space_width: int, space_height: int):
        """Move the robot for certain seconds."""
        self.px = (self.px + seconds * self.vx) % space_width
        self.py = (self.py + seconds * self.vy) % space_height

    def cur_quadrant(self, space_width: int, space_height: int) -> int:
        """Get current quadrant, 0 to 3 for top left, top right, bottom left, bottom right."""
        mid_x = space_width // 2
        mid_y = space_height // 2
        if self.px < mid_x:
            if self.py < mid_y:
                return 0
            if self.py > mid_y:
                return 2
        elif self.px > mid_x:
            if self.py < mid_y:
                return 1
            if self.py > mid_y:
                return 3

        return -1
    
    def all_possible_locations(self, space_width: int, space_height: int) -> Iterable[Tuple[int, int]]:
        """Return all possible locations of robot."""
        orig_px, orig_py = self.px, self.py
        yield orig_px, orig_py
        returned = {(orig_px, orig_py)}
        while True:
            self.move(1, space_width, space_height)
            if (self.px, self.py) in returned:
                self.px = orig_px
                self.py = orig_py
                return
            returned.add((self.px, self.py))
            yield self.px, self.py



def print_robots(robots: List[Robot], space_width: int, space_height: int):
    tuples = [(r.px, r.py) for r in robots]
    print_tuples(tuples, space_width, space_height)


def print_tuples(tuples: List[Tuple[int, int]], space_width: int, space_height: int):
    sorted_tuples = sorted(tuples, key=lambda x: x[1] * 10000 + x[0])
    cur_idx = 0
    cur_tup = sorted_tuples[cur_idx]
    for y in range(space_height):
        for x in range(space_width):
            robs = 0
            while cur_tup is not None and cur_tup[0] == x and cur_tup[1] == y:
                robs += 1
                cur_idx += 1
                if cur_idx >= len(sorted_tuples):
                    cur_tup = None
                else:
                    cur_tup = sorted_tuples[cur_idx]
            ch = '.' if robs == 0 else str(robs % 10)
            print(ch, end='')
        print()

    assert cur_tup is None, 'Tuples missing from map!'



robots: List[Robot] = []
for line in inp_string.split('\n'):
    robots.append(Robot.from_line(line))

# Move 100 seconds
quadrants = [0] * 4
for r in robots:
    r.move(100, space_width, space_height)
    quad = r.cur_quadrant(space_width, space_height)
    if quad > -1:
        quadrants[quad] += 1


ret = math.prod(quadrants)

print('Answer 1:', ret)


@dataclass
class QuadCounter:
    top_left: int = 0
    top_right: int = 0
    bottom_left: int = 0
    bottom_right: int = 0

    def add_robot(self, quad: int):
        if quad == -1:
            return
        if quad == 0:
            self.top_left += 1
        elif quad == 1:
            self.top_right += 1
        elif quad == 2:
            self.bottom_left += 1
        elif quad == 3:
            self.bottom_right += 1
        else:
            raise Exception('EEE')

    def get_safety_factor(self):
        return self.top_left * self.top_right * self.bottom_left * self.bottom_right
    
    def clear(self):
        self.top_left = 0
        self.top_right = 0
        self.bottom_left = 0
        self.bottom_right = 0
    
    def is_symmetric(self):
        return self.top_left == self.top_right and self.bottom_left == self.bottom_right



robots: List[Robot] = []
for line in inp_string.split('\n'):
    robots.append(Robot.from_line(line))


quad = QuadCounter()
for r in robots:
    r.move(100, space_width, space_height)
    quad.add_robot(r.cur_quadrant(space_width, space_height))

print('Re-do Answer 1:', quad.get_safety_factor())


def is_christmas(robots: List[Robot], space_width: int, space_height: int) -> Tuple[bool, int]:
    mid_x = space_width // 2
    star = (mid_x, 0)
    trunk = (mid_x, space_height-1)
    found = 0
    for r in robots:
        if (r.px, r.py) == star or (r.px, r.py) == trunk:
            found += 1
    if found != 2:
        return False, 0

    robots.sort(key=lambda x: x.py * 10000 + x.px)
    cur_idx = 0
    cur_robot = robots[cur_idx]
    symmetric_lines = 0

    for y in range(space_height):
        if cur_robot.py != y:
            continue

        robs_left: int = []
        robs_right: int = []
        for x in range(space_width):
            while cur_robot.px == x and cur_robot.py == y:
                if x < mid_x:
                    robs_left.append(x)
                elif x > mid_x:
                    robs_right.append(x)

                cur_idx += 1
                if cur_idx >= len(robots):
                    cur_robot = None
                    break
                cur_robot = robots[cur_idx]

            if cur_robot is None or cur_robot.py != y:
                # No more robots to check in row
                break

        # Assess line symmetry
        if len(robs_left) != len(robs_right):
            return False, symmetric_lines
        for left_robot in robs_left:
            right_robot = 2*mid_x - left_robot
            if right_robot not in robs_right:
                return False, symmetric_lines
        symmetric_lines += 1
        if cur_robot is None:
            break
    
    assert cur_robot is None, 'Robot missing!'
    return True, symmetric_lines


robots: List[Robot] = []
for line in inp_string.split('\n'):
    robots.append(Robot.from_line(line))


def fake_generator() -> Iterable[int]:
    seconds = 0
    max_symm_lines = 0
    while True:
        seconds += 1
        if seconds % 10000 == 0:
            yield seconds
            # print('-'* 40, seconds)
            # print_robots(robots, space_width, space_height)

        for r in robots:
            r.move(1, space_width, space_height)

        is_symm, symm_lines = is_christmas(robots, space_width, space_height)
        if is_symm:
            print_robots(robots, space_width, space_height)
            print('Is that it?')
            break
        if symm_lines > max_symm_lines:
            max_symm_lines = symm_lines
            print('-'* 10, 'Max symmetric lines', max_symm_lines, 'after', seconds, 'seconds')
            print_robots(robots, space_width, space_height)

    yield seconds

for seconds in tqdm(fake_generator()):
    pass

print('Answer 2:', seconds)
