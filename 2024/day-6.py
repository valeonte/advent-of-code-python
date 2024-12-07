"""
Advent of Code 2024 day 6.

Created on Sat Dec 07 2024 8:13:21 AM

@author: Eftychios
"""

import os

from common import Dir
from typing import List, Set, Tuple, Iterable


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


with open("inputs/day-6.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")

max_x = len(inp[0])
max_y = len(inp)


start_dir = None
for start_y, row in enumerate(inp):
    for start_x, ch in enumerate(row):
        if ch == '^':
            start_dir = Dir.N
        elif ch == '>':
            start_dir = Dir.E
        elif ch == 'v':
            start_dir = Dir.S
        elif ch == '<':
            start_dir = Dir.W
        else:
            continue
        break
    if start_dir is not None:
        break


def is_outside(x: int, y: int):
    return x < 0 or x >= max_x or y < 0 or y >= max_y


def is_obstacle(x: int, y: int, extra_obstacle: Tuple[int, int]):
    return (x, y) == extra_obstacle or inp[y][x] == '#'


def path_yielder(start_x: int, start_y: int, start_dir: Dir, extra_obstacle: Tuple[int, int] = (-1, -1)) -> Iterable[Tuple[int, int, Dir]]:
    x = start_x
    y = start_y
    cur_dir = start_dir
    while not is_outside(x, y):
        if is_obstacle(x, y, extra_obstacle):
            # if on obstacle, step back and turn
            if cur_dir == Dir.N:
                y += 1
                cur_dir = Dir.E
            elif cur_dir == Dir.E:
                x -= 1
                cur_dir = Dir.S
            elif cur_dir == Dir.S:
                y -= 1
                cur_dir = Dir.W
            elif cur_dir == Dir.W:
                x += 1
                cur_dir = Dir.N
            else:
                raise Exception('Impossible!')
        else:
            yield x, y, cur_dir

            # move forward
            if cur_dir == Dir.N:
                y -= 1
            elif cur_dir == Dir.E:
                x += 1
            elif cur_dir == Dir.S:
                y += 1
            elif cur_dir == Dir.W:
                x -= 1
            else:
                raise Exception('Impossible!')


def is_infinite_loop(start_x: int, start_y: int, start_dir: Dir, extra_obstacle: Tuple[int, int]) -> bool:
    pre_pos: set[Tuple[int, int, Dir]] = set()
    for xydir in path_yielder(start_x, start_y, start_dir, extra_obstacle):
        if xydir in pre_pos:
            return True
        pre_pos.add(xydir)

    return False



visited: Set[Tuple[int, int]] = set()

x = start_x
y = start_y

for x, y, _ in path_yielder(start_x, start_y, start_dir):
    visited.add((x, y))

print('Answer 1:', len(visited))


infinite_loops = 0
for i, extra_obstacle in enumerate(visited):
    if extra_obstacle == (start_x, start_y):
        continue
    if i % 1000 == 0:
        print(0)
    elif i % 10 == 0:
        print((i // 10) % 10, end='')

    if is_infinite_loop(start_x, start_y, start_dir, extra_obstacle):
        infinite_loops += 1

print('Answer 2:', infinite_loops)
