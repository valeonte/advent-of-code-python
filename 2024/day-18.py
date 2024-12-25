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
from common import Dir, get_neighbours
from itertools import product

os.chdir("C:/Repos/advent-of-code-python/2024")


inp_string = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

use_first = 12


with open("inputs/day-18.txt", "r") as f:
    inp_string = f.read()
use_first = 1024


max_x, max_y = 0, 0
drops = list()
for line in inp_string.split('\n'):
    x, y = map(int, line.split(','))
    drops.append((x, y))
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y


corrupted = set(drops[:use_first])
shortest_paths = dict()


def print_map():
    print('-'*20)
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x, y) in corrupted:
                ch = '#'
            elif (x, y) in shortest_paths:
                ch = 'O'
            else:
                ch = '.'
            print(ch, end='')
        print()


check_q = [(max_x, max_y, 0)]

while len(check_q) > 0:
    x, y, cost = check_q.pop(0)
    if x > max_x or y > max_y or x < 0 or y < 0 or (x, y) in corrupted:
        continue
    pre_cost = shortest_paths.get((x, y), math.inf)
    if cost >= pre_cost:
        continue
    shortest_paths[(x, y)] = cost
    #print_map()
    for nx, ny in get_neighbours(x, y):
        check_q.append((nx, ny, cost+1))


print('Answer 1:', shortest_paths[(0, 0)])


for use_first in trange(len(drops)):
    corrupted = set(drops[:use_first])
    shortest_paths = dict()

    check_q = [(max_x, max_y, 0)]

    while len(check_q) > 0:
        x, y, cost = check_q.pop(0)
        if x > max_x or y > max_y or x < 0 or y < 0 or (x, y) in corrupted:
            continue
        pre_cost = shortest_paths.get((x, y), math.inf)
        if cost >= pre_cost:
            continue
        shortest_paths[(x, y)] = cost
        #print_map()
        for nx, ny in get_neighbours(x, y):
            check_q.append((nx, ny, cost+1))

    if (0, 0) not in shortest_paths:
        break

print('Answer 2:', drops[use_first-1])
