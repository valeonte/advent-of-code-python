"""
Advent of Code 2024 day 8.

Created on Sun Dec 08 2024 10:13:13 AM

@author: Eftychios
"""

import os
import math

from typing import Dict, Iterable, List, Set, Tuple


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


with open("inputs/day-8.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")


antennas: Dict[str, List[Tuple[int, int]]] = dict()

max_x = len(inp[0])
max_y = len(inp)

for y, row in enumerate(inp):
    for x, ch in enumerate(row):
        if ch == '.':
            continue
        if ch not in antennas:
            antennas[ch] = list()
        antennas[ch].append((x, y))


def get_theoretical_antinode1(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int]:
    anti1_x = x1 - (x2 - x1)
    anti1_y = y1 - (y2 - y1)

    return anti1_x, anti1_y


def get_theoretical_antinodes(x1: int, y1: int, x2: int, y2: int) -> Iterable[Tuple[int, int]]:
    yield get_theoretical_antinode1(x1, y1, x2, y2)
    yield get_theoretical_antinode1(x2, y2, x1, y1)


antinodes: Set[Tuple[int, int]] = set()


def print_map():
    for y in range(max_y):
        for x in range(max_x):
            tup = x, y
            printed = False
            for freq, positions in antennas.items():
                if tup in positions:
                    print(freq, end='')
                    printed = True
                    break
            if not printed:
                if tup in antinodes:
                    print('#', end='')
                else:
                    print('.', end='')

        print()


for freq, positions in antennas.items():
    for i, (x1, y1) in enumerate(positions):
        for x2, y2 in positions[i+1:]:
            for anti_x, anti_y in get_theoretical_antinodes(x1, y1, x2, y2):
                if anti_x >= 0 and anti_x < max_x and anti_y >= 0 and anti_y < max_y:
                    antinodes.add((anti_x, anti_y))
                    # print_map()
                    # print('-------', freq, '-----', x1, y1, '-', x2, y2, '-----', anti_x, anti_y, '-------')
                    pass


print_map()
print('Answer 1:', len(antinodes))


def get_all_antinodes(x1: int, y1: int, x2: int, y2: int) -> Iterable[Tuple[int, int]]:
    diff_x = x2 - x1
    diff_y = y2 - y1

    g = math.gcd(diff_x, diff_y)
    step_x = diff_x // g
    step_y = diff_y // g

    mul = 0
    while True:
        anti_x = x1 - step_x * mul
        if anti_x < 0 or anti_x >= max_x:
            break
        anti_y = y1 - step_y * mul
        if anti_y < 0 or anti_y >= max_y:
            break
        mul += 1
        yield anti_x, anti_y

    mul = 1
    while True:
        anti_x = x1 + step_x * mul
        if anti_x < 0 or anti_x >= max_x:
            break
        anti_y = y1 + step_y * mul
        if anti_y < 0 or anti_y >= max_y:
            break
        mul += 1
        yield anti_x, anti_y


antinodes.clear()


for freq, positions in antennas.items():
    for i, (x1, y1) in enumerate(positions):
        for x2, y2 in positions[i+1:]:
            for anti_x, anti_y in get_all_antinodes(x1, y1, x2, y2):
                antinodes.add((anti_x, anti_y))
                # print_map()
                # print('-------', freq, '-----', x1, y1, '-', x2, y2, '-----', anti_x, anti_y, '-------')
                pass


print_map()
print('Answer 2:', len(antinodes))
