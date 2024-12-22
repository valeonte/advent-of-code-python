"""
Advent of Code 2024 day 18.

Created on Sat Dec 21 2024 11:17:25 PM

@author: Eftychios
"""

import re
import os
import math
import sys

import datetime as dt
import numpy as np

from functools import lru_cache
from typing import Dict, Iterable, List, Set, Tuple
from dataclasses import dataclass
from decimal import Decimal
from tqdm import tqdm, trange
from common import Dir
from itertools import product

os.chdir("C:/Repos/advent-of-code-python/2024")


inp_string = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


with open("inputs/day-19.txt", "r") as f:
    inp_string = f.read()


available_towels: Set[str] = None
designs: List[str] = list()
for i, line in enumerate(inp_string.split("\n")):
    if i == 0:
        available_towels = set(line.split(", "))
        continue
    if i == 1:
        continue
    designs.append(line)

max_len = max(map(len, available_towels))


def get_relevant_towels(design: str) -> Iterable[str]:
    for i in range(min(max_len, len(design)), -1, -1):
        key = design[:i]
        if key in available_towels:
            yield key


@lru_cache(maxsize=5000)
def is_design_doable(design: str) -> bool:
    if len(design) == 0:
        return True
    for towel in get_relevant_towels(design):
        if design.startswith(towel) and is_design_doable(design[len(towel):]):
            return True

    return False


doable_designs = 0
for design in tqdm(designs):
    if is_design_doable(design):
        doable_designs += 1


print('Answer 1:', doable_designs)


@lru_cache(maxsize=5000)
def doable_ways_count(design: str) -> int:
    if len(design) == 0:
        return 1
    ret = 0
    for towel in get_relevant_towels(design):
        ret += doable_ways_count(design[len(towel):])

    return ret


doable_count_sum = 0
for design in tqdm(designs):
    doable_count_sum += doable_ways_count(design)


print('Answer 2:', doable_count_sum)
