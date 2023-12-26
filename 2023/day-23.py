"""
Advent of Code 2023 day 23.

Created on Sun Dec 24 2023 10:35:38 PM

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

inp_string = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


with open("inputs/day-23.txt", "r") as f:
    inp_string = f.read()

inps = inp_string.split('\n')

part1 = False

fmap = np.array([list(row) for row in inps])


def get_potential_next(i: int, j: int) -> Iterator[Tuple[int, int]]:
    """Get all potential next paths."""
    if part1:
        cur = fmap[i, j]
        if cur == '^':
            yield i - 1, j
            return
        if cur == 'v':
            yield i + 1, j
            return
        if cur == '<':
            yield i, j - 1
            return
        if cur == '>':
            yield i, j + 1
            return

    for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if ni < 0 or nj < 0 or ni >= fmap.shape[0] or nj >= fmap.shape[1]:
            continue
        if fmap[ni, nj] == '#':
            continue
        yield ni, nj


def print_fmap(visited: Set[Tuple[int, int]]):
    print('-' * 50)
    for i, row in enumerate(fmap):
        line = ''
        for j, ch in enumerate(row):
            if (i, j) in visited:
                line += 'O'
            else:
                line += ch
        print(line)


queue = [(0, 1, {(0, 1)})]
exit_i, exit_j = fmap.shape[0] - 1, fmap.shape[1] - 2
short_exit_i, short_exit_j = 137, 137

best_solution = 0
loops = 0
start = dt.datetime.now()
last_print = dt.datetime.now()

def loops_per_sec(at_time: dt.datetime, loops: int):
    secs = (at_time - start).seconds
    if secs == 0:
        return 0
    global last_print
    last_print = dt.datetime.now()
    return loops / secs


#def get_best_from_and_remaining(i: int, j: int, visited: Set[Tuple[int, int])
cur_is_good = False
while cur_is_good or len(queue) > 0:
    loops += 1
    if not cur_is_good:
        i, j, visited = queue.pop()
    cur_is_good = False
    #print_fmap(visited)
    if dt.datetime.now() - last_print > dt.timedelta(seconds=10):
        log.info('Longest: %d, Queue size: %d, Speed: %.1f loops/sec',
                 best_solution, len(queue), loops_per_sec(dt.datetime.now(), loops))

    all_next = []
    for ni, nj in get_potential_next(i, j):
        if (ni, nj) in visited:
            continue

        if ni == short_exit_i and nj == short_exit_j:
            cur_path = len(visited) + 5
            if cur_path > best_solution:
                best_solution = cur_path

            if dt.datetime.now() - last_print > dt.timedelta(seconds=1):
                log.info('New path: %d, Longest: %d, Queue size: %d, Speed: %.1f loops/sec',
                         cur_path, best_solution, len(queue), loops_per_sec(dt.datetime.now(), loops))
                # we got to path, done
            all_next.clear()
            break

        all_next.append((ni, nj))

    if len(all_next) == 0:
        continue

    # Insert all but first, copying visited
    for ni, nj in all_next[1:]:
        new_visited = visited.copy()
        new_visited.add((ni, nj))

        # using as stack, to see each path to its end
        queue.append((ni, nj, new_visited))
    
    # First will be cur
    visited.add(all_next[0])
    i, j = all_next[0]
    cur_is_good = True


log.info('Answer %d: %d', 1 if part1 else 2, best_solution)


log.info('Done?')
