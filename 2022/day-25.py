# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 25.

Created on Wed Dec 28 18:38:15 2022

@author: Eftychios
"""

import os
import sys
import math

import datetime as dt

from typing import Iterator, Set
from dataclasses import dataclass, replace

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


with open("inputs/day-25.txt", "r") as f:
    inp_string = f.read()


def eval_snafu(snum: str) -> int:
    """Evaluates a SNAFU number."""
    n = list(snum)
    n.reverse()

    ret = 0
    for i, d in enumerate(n):
        mult = 5 ** i
        if d.isnumeric():
            ret += int(d) * mult
        elif d == '-':
            ret -= mult
        elif d == '=':
            ret -= 2 * mult
        else:
            raise Exception('Unrecognised digit!')

    return ret


def num_to_snafu(n: int) -> str:
    """Convert a number to its SNAFU representation."""
    # Add number 222 with as many digits as base 5 n first
    if n == 0:
        return '0'

    # We add an extra digit here, in case it is needed. We trim 0's at the end
    n_digits = math.floor(math.log(n, 5)) + 2
    add = 0
    for i in range(n_digits):
        add += 2 * (5 ** i)

    n += add

    # Then convert to base 5
    base5 = ''
    while n > 0:
        d = n % 5
        base5 = str(d) + base5
        n = n // 5

    # Then replace every digit with the respective SNAFU (2 less)
    snafu = ''
    for d in base5:
        nd = int(d)
        if nd > 1:
            snafu += str(nd - 2)
        elif nd == 1:
            snafu += '-'
        elif nd == 0:
            snafu += '='

    # Trim leading 0's
    while snafu[0] == '0':
        snafu = snafu[1:]

    return base5, snafu


ss = 0
for row in inp_string.split('\n'):
    v = eval_snafu(row)
    print(row, '=', v)
    ss += v

print('Answer 1:', num_to_snafu(ss))
