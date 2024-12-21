"""
Advent of Code 2024 day 16.

Created on Tue Dec 17 2024 10:16:36 PM

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
from tqdm import tqdm
from common import Dir

# sys.setrecursionlimit(100000)
os.chdir("C:/Repos/advent-of-code-python/2024")


inp_string = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


inp_string = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""



with open("inputs/day-16.txt", "r") as f:
    inp_string = f.read()


def parse_map() -> Tuple[np.array, Tuple[int, int], Tuple[int, int]]:
    lab_rows = []
    start = None
    end = None
    for y, inp in enumerate(inp_string.split('\n')):
        row = np.zeros((1, len(inp)), dtype=int)
        for x, ch in enumerate(inp):
            if ch == '#':
                row[0, x] = -1
            elif ch == 'S':
                start = x, y
            elif ch == 'E':
                end = x, y
        lab_rows.append(row)

    assert start is not None and end is not None, 'BAD'

    return np.concatenate(lab_rows), start, end

lab, start, end = parse_map()


def gen_map(lab: np.array, visited: Dict[Tuple[int, int], Dir] = dict()):
    ret = []
    for y, row in enumerate(lab):
        line = ''
        for x, el in enumerate(row):
            if (x, y) in visited:
                dir = visited[(x, y)]
                if dir == Dir.E:
                    ch = '>'
                elif dir == Dir.W:
                    ch = '<'
                elif dir == Dir.N:
                    ch = '^'
                elif dir == Dir.S:
                    ch = 'v'
                else:
                    raise Exception('BAD')
            elif el == 0:
                ch = '.'
            elif el == -1:
                ch = '#'
            else:
                raise Exception('!!')
            line += ch
        ret.append(line)
    
    return '\n'.join(ret)


print(gen_map(lab))


def get_movement_change(dir: Dir) -> Tuple[int, int, Dir, Dir]:
    dx, dy = 0, 0
    if dir == Dir.E:
        dx = 1
        cw = Dir.S
        acw = Dir.N
    elif dir == Dir.W:
        dx = -1
        cw = Dir.N
        acw = Dir.S
    elif dir == Dir.N:
        dy = -1
        cw = Dir.E
        acw = Dir.W
    elif dir == Dir.S:
        dy = 1
        cw = Dir.W
        acw = Dir.E
    else:
        raise Exception('AA')

    return dx, dy, cw, acw


# max_depth = 0
# iterations = 0
# best_so_far = 1000000000

# def get_cheapest_path_from(x: int, y: int, dir: Dir, cur_cost: int = 0, visited: Dict[Tuple[int, int], Dir] = dict()):
#     global iterations, max_depth, best_so_far
#     if (x, y) in visited or cur_cost >= best_so_far:
#         return -1
#     if end == (x, y):
#         return cur_cost
#     if lab[y, x] == -1:
#         return -1

#     iterations += 1

#     visited[(x, y)] = dir
#     if len(visited) > max_depth:
#         max_depth = len(visited)
#         print('New record depth:', max_depth)
    
#     #print(gen_map(lab, visited))

#     dx, dy, cw, acw = get_movement_change(dir)

#     orig_best = best_so_far
#     # move forward
#     new_cost = get_cheapest_path_from(x+dx, y+dy, dir, cur_cost=cur_cost+1, visited=visited)
#     if new_cost != -1 and new_cost < best_so_far:
#         best_so_far = new_cost
#         print('New best!', best_so_far)

#     # clockwise and forward
#     dir = cw
#     dx, dy, _, _ = get_movement_change(dir)
#     new_cost = get_cheapest_path_from(x+dx, y+dy, dir, cur_cost=cur_cost+1001, visited=visited)
#     if new_cost != -1 and new_cost < best_so_far:
#         best_so_far = new_cost
#         print('New best!', best_so_far)

#     # anti-clockwise and forward
#     dir = acw
#     dx, dy, _, _ = get_movement_change(dir)
#     new_cost = get_cheapest_path_from(x+dx, y+dy, dir, cur_cost=cur_cost+1001, visited=visited)
#     if new_cost != -1 and new_cost < best_so_far:
#         best_so_far = new_cost
#         print('New best!', best_so_far)

#     # node done, remove from visited
#     del visited[(x, y)]

#     if best_so_far < orig_best:
#         #print(gen_map(lab, visited))
#         return best_so_far
    
#     return -1  # no need to bother


# Approach one failed on the actual data, trying alternate
# best_score = get_cheapest_path_from(start[0], start[1], Dir.E)


@dataclass(eq=True, frozen=True)
class DirCoords:
    x: int
    y: int
    dir: Dir

    def next_clockwise(self) -> 'DirCoords':
        new_dir = self.dir.next_clockwise(2)

        return DirCoords(self.x, self.y, new_dir)

    def next_anticlockwise(self) -> 'DirCoords':
        new_dir = self.dir.next_clockwise(-2)

        return DirCoords(self.x, self.y, new_dir)

    def opposite(self) -> 'DirCoords':
        new_dir = self.dir.next_clockwise(4)

        return DirCoords(self.x, self.y, new_dir)

    def next_forward(self) -> 'DirCoords':
        dx, dy, _, _ = get_movement_change(self.dir)
        return DirCoords(self.x + dx, self.y + dy, self.dir)



def get_all_possible_neighbours(x: int, y: int) -> Iterable[DirCoords]:
    """Get the neighbour and the direction one is moving from that to x, y."""
    yield DirCoords(x-1, y, Dir.E)
    yield DirCoords(x+1, y, Dir.W)
    yield DirCoords(x, y+1, Dir.N)
    yield DirCoords(x, y-1, Dir.S)

# We will start from end, and create a map with the shortest path for each node
shortest_paths: Dict[DirCoords, int] = dict()


def get_visited_from_shortest_paths() -> Dict[Tuple[int, int], Dir]:
    ret = dict()
    unique_nodes = {(dc.x, dc.y) for dc in shortest_paths.keys()}
    for node in unique_nodes:
        min_cost = 1000000000
        min_cost_dir = None
        for dc, cost in shortest_paths.items():
            if dc.x == node[0] and dc.y == node[1] and cost < min_cost:
                min_cost = cost
                min_cost_dir = dc.dir
        ret[node] = min_cost_dir
    return ret


def update_cost_if_smaller(key: DirCoords, new_value: int) -> Tuple[bool, int]:
    cur_value = shortest_paths.get(key, -1)
    if cur_value == -1 or cur_value > new_value:
        shortest_paths[key] = new_value
        return True, cur_value
    return False, cur_value


def print_node_costs(x: int, y: int):
    for d in all_dirs:
        print(d, shortest_paths.get(DirCoords(x, y, d), -1))


all_dirs = [Dir.N, Dir.S, Dir.W, Dir.E]

for d in all_dirs:
    shortest_paths[DirCoords(end[0], end[1], d)] = 0

check_q = [end]
while len(check_q) > 0:
    base_x, base_y = check_q.pop(0)
    for nc in get_all_possible_neighbours(base_x, base_y):
        if lab[nc.y, nc.x] == -1:
            # wall
            continue
        base_cost = shortest_paths[DirCoords(base_x, base_y, nc.dir)]
        new_cost = base_cost + 1

        change_made1, cur_cost1 = update_cost_if_smaller(nc, new_cost)
        change_made2, cur_cost2 = update_cost_if_smaller(nc.next_clockwise(), new_cost + 1000)
        change_made3, cur_cost3 = update_cost_if_smaller(nc.next_anticlockwise(), new_cost + 1000)
        change_made4, cur_cost4 = update_cost_if_smaller(nc.opposite(), new_cost + 2000)

        if change_made1 or change_made2 or change_made3 or change_made4:
            check_q.append((nc.x, nc.y))
        #  elif cur_cost1 > 0 and min(cur_cost1 + 1, cur_cost2 + 1001, cur_cost3 + 1001, cur_cost4 + 2001) < base_cost:
        #     # encountered cheaper node, re-refreshing
        #     check_q.append((base_x, base_y))

    #print(gen_map(lab, get_visited_from_shortest_paths()))


        
best_score = shortest_paths[DirCoords(start[0], start[1], Dir.E)]
#print(gen_map(lab, get_visited_from_shortest_paths()))

print('Answer 1:', best_score)

def get_next_step_cost(dc: DirCoords) -> Iterable[Tuple[DirCoords, int]]:
    yield dc.next_forward(), 1
    yield dc.next_clockwise(), 1000
    yield dc.next_anticlockwise(), 1000
    yield dc.opposite(), 2000


path: Set[DirCoords] = {DirCoords(start[0], start[1], Dir.E)}
check_q = [(DirCoords(start[0], start[1], Dir.E), best_score)]
while len(check_q) > 0:
    dc, remaining_cost = check_q.pop(0)

    for dc_next, cost in get_next_step_cost(dc):
        if lab[dc_next.y, dc_next.x] == -1:
            # wall
            continue
        if remaining_cost - cost == shortest_paths.get(dc_next, -1):
            path.add(dc_next)
            check_q.append((dc_next, remaining_cost - cost))

visited = dict()
for p in path:
    visited[(p.x, p.y)] = p.dir
    #print(gen_map(lab, visited))

print('Answer 2:', len(visited))
