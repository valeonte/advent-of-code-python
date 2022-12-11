# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 10.

Created on Sat Dec 10 11:23:08 2022

@author: Eftychios
"""

import os

from typing import Iterator, Tuple


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

with open("inputs/day-10.txt", "r") as f:
    inp_string = f.read()


def get_cycles(program: str) -> Iterator[Tuple[int, int]]:
    """Return cycle and value of X, and the end of the cycle returned."""
    cycle = 0
    X = 1
    yield (cycle, X)
    for cmd in program.split('\n'):
        if cmd == 'noop':
            cycle += 1
            yield (cycle, X)
            continue

        parts = cmd.split(' ')
        cycle += 1
        yield (cycle, X)
        cycle += 1
        X = X + int(parts[1])
        yield (cycle, X)


strength_sum = 0
for cycle, X in get_cycles(inp_string):
    during = cycle + 1
    if (during - 20) % 40 == 0:
        strength = during * X
        print('During cycle', during, 'X is', X, 'with strength', strength)
        strength_sum += strength

print('Answer 1:', strength_sum)


print('\nAnswer 2:')
output = ''
for cycle, X in get_cycles(inp_string):
    pos = cycle % 40
    if pos >= X - 1 and pos <= X + 1:
        c = '#'
    else:
        c = '.'

    if len(output) > 0 and len(output) % 40 == 0:
        print(output)
        output = ''

    output += c
