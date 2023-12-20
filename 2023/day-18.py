"""
Advent of Code 2023 day 18.

Created on Tue Dec 19 2023 9:32:42 PM

@author: Eftychios
"""

import os
import re

import numpy as np

from typing import Tuple, Set, Iterator
from dataclasses import dataclass, replace
from enum import Enum

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = r"""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

with open("inputs/day-18.txt", "r") as f:
    inp_string = f.read()


inps = inp_string.split('\n')
part_1 = False
pat = re.compile(r'^(?P<direction>[UDLR]{1}) (?P<steps>\d+) \(#(?P<colour>\w+)\)$')


def get_next(cur_node: Tuple[int, int], direction: str) -> Tuple[int, int]:
    """Get the next node following 1 step in direction."""
    if direction == 'U':
        return (cur_node[0] - 1, cur_node[1])
    if direction == 'D':
        return (cur_node[0] + 1, cur_node[1])
    if direction == 'L':
        return (cur_node[0], cur_node[1] - 1)
    if direction == 'R':
        return (cur_node[0], cur_node[1] + 1)
    
    raise Exception('ee')


def get_dug_lines(dug: Set[Tuple[int, int]]) -> Iterator[str]:
    for i in range(min_i, max_i + 1):
        line = ''
        for j in range(min_j, max_j + 1):
            if (i, j) in dug:
                line += '#'
            else:
                line += '.'
        yield line


def print_dug(dug: Set[Tuple[int, int]]):
    print('-' * 50)
    for line in get_dug_lines(dug):
        print(line)


if part_1:
    print('Digging first round')
    cur_node = (0, 0)
    dug = set([cur_node])
    min_j = 0
    max_j = 0
    min_i = 0
    max_i = 0
    for row in inps:
        m = pat.match(row)
        for _ in range(int(m.group('steps'))):
            cur_node = get_next(cur_node, m.group('direction'))
            dug.add(cur_node)
        if cur_node[0] > max_i:
            max_i = cur_node[0]
        if cur_node[0] < min_i:
            min_i = cur_node[0]
        if cur_node[1] > max_j:
            max_j = cur_node[1]
        elif cur_node[1] < min_j:
            min_j = cur_node[1]


    with open('day18-dug.txt', 'w') as f:
        for line in get_dug_lines(dug):
            f.write(line + '\n')


    print('Digging in-between')
    first_inside = (1, 1)

    queue = [first_inside]
    while queue:
        p = queue.pop(0)
        if p in dug:
            continue
        dug.add(p)
        for dir in 'UDLR':
            queue.append(get_next(p, dir))

    with open('day18-dug-all.txt', 'w') as f:
        for line in get_dug_lines(dug):
            f.write(line + '\n')

    print('Answer 1:', len(dug))


@dataclass(frozen=True)
class Point:
    i: int
    j: int


print('Digging first round')
cur_node = Point(0, 0)
nodes_in_order = [cur_node]
dir_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
for row in inps:
    m = pat.match(row)
    colour = m.group('colour')
    dir = dir_map[colour[-1]]
    steps = int(colour[:-1], 16)
    if dir == 'U':
        new_node = replace(cur_node, i=cur_node.i - steps)
    elif dir == 'D':
        new_node = replace(cur_node, i=cur_node.i + steps)
    elif dir == 'L':
        new_node = replace(cur_node, j=cur_node.j - steps)
    elif dir == 'R':
        new_node = replace(cur_node, j=cur_node.j + steps)
    else:
        raise Exception('ee')

    nodes_in_order.append(new_node)
    cur_node = new_node

# I found our about shoelace!
# We will try to get all rectangles, from each vector
A = 0
E = 2
for k in range(len(nodes_in_order)):
    dv1 = nodes_in_order[k]
    dv2 = nodes_in_order[k + 1] if k < len(nodes_in_order) - 1 else nodes_in_order[0]
    A += (dv1.i + dv2.i) * (dv1.j - dv2.j)

    E += abs(dv1.i - dv2.i) + abs(dv1.j - dv2.j)

# get the area of the edges

print('Answer 2:', abs(A) // 2 + E//2)
