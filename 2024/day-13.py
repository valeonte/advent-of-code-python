"""
Advent of Code 2024 day 12.

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


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

with open("inputs/day-13.txt", "r") as f:
    inp_string = f.read()


epsilon = 0.00001

@dataclass
class Machine:
    ax: int
    ay: int
    bx: int
    by: int

    prizex: int
    prizey: int

    def solve(self) -> Tuple[int, int]:
        # It is a matter of solving the equations system.
        # If we press button A A times, and button B B times:
        # ax * A + bx * B = prizex
        # ay * A + by * B = prizey  ==>  by * B - (bx * ay / ax) * B = prizey - prizex * ay / ax
        #       ==> B = (prizey - prizex * ay / ax) / (by - bx * ay / ax)
        #
        # From the first: A = (prizex - bx * B) / ax
        
        B = (Decimal(self.prizey) - (Decimal(self.prizex) / Decimal(self.ax)) * Decimal(self.ay)) / (Decimal(self.by) - Decimal(self.bx) * Decimal(self.ay) / Decimal(self.ax))
        A = (Decimal(self.prizex) - Decimal(self.bx) * B) / Decimal(self.ax)

        assert abs(A * self.ax + B * self.bx - self.prizex) < epsilon, 'Invalid solution!'
        assert abs(A * self.ay + B * self.by - self.prizey) < epsilon, 'Invalid solution!'

        return A, B

    @classmethod
    def from_lines(cls, lines: List[str]) -> 'Machine':
        match = re.match(r'^Button \w: X\+(\d+), Y\+(\d+)$', lines[0])
        ax = int(match.group(1))
        ay = int(match.group(2))

        match = re.match(r'^Button \w: X\+(\d+), Y\+(\d+)$', lines[1])
        bx = int(match.group(1))
        by = int(match.group(2))

        match = re.match(r'^Prize: X=(\d+), Y=(\d+)$', lines[2])
        prizex = int(match.group(1))
        prizey = int(match.group(2))

        return cls(ax, ay, bx, by, prizex, prizey)



lines = inp_string.split('\n')
i = 0
machines: List[Machine] = []
while i < len(lines):
    if lines[i].startswith('Button A'):
        machines.append(Machine.from_lines(lines[i:i+3]))
        i += 3
    i += 1


ret = 0
for machine in machines:
    A, B = machine.solve()
    if A > -epsilon and B > -epsilon and abs(round(A) - A) < epsilon and abs(round(B) - B) < epsilon:
        ret += 3 * int(round(A)) + int(round(B))

print('Answer 1:', ret)


inc = 10000000000000
ret = 0

for machine in machines:
    machine.prizex += inc
    machine.prizey += inc

    A, B = machine.solve()
    if A > -epsilon and B > -epsilon and abs(round(A) - A) < epsilon and abs(round(B) - B) < epsilon:
        ret += 3 * int(round(A)) + int(round(B))

print('Answer 2:', ret)
