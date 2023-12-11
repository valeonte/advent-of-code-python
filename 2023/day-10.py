"""
Advent of Code 2023 day 10.

Created on Sun Dec 10 2023

@author: Eftychios
"""

import os
import math

import numpy as np

from typing import Tuple, Set

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

inp_string = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

inp_string = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

inp_string = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

inp_string = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

with open("inputs/day-10.txt", "r") as f:
    inp_string = f.read()

inp = inp_string.split('\n')

links = {ord('-'): [(0, -1), (0, 1)],
         ord('|'): [(-1, 0), (1, 0)],
         ord('L'): [(-1, 0), (0, 1)],
         ord('J'): [(-1, 0), (0, -1)],
         ord('7'): [(1, 0), (0, -1)],
         ord('F'): [(0, 1), (1, 0)]}


def tile_has_link(i: int, j: int, link: Tuple[int, int]) -> bool:
    """Check if tile has required link."""
    if i < 0 or j < 0 or i >= tiles.shape[0] or j >= tiles.shape[1]:
        return False
    tile = tiles[i, j]
    if tile == ord('S'):
        return True
    if tile not in links:
        return False
    
    return link in links[tile]


def print_tiles(path_tiles: Set[Tuple[int, int]] = None,
                enclosed: Set[Tuple[int, int]] = None):
    """Print tiles."""
    for i, row in enumerate(tiles):
        pr_row = ''
        for j, ch in enumerate(row):
            if path_tiles is not None and (i, j) in path_tiles:
                pr_row += '*'
            elif enclosed is not None and (i, j) in enclosed:
                pr_row += 'I'
            elif enclosed is not None and (i, j) not in enclosed:
                pr_row += 'O'
            else:
                pr_row += chr(ch)
        print(pr_row)


tiles = np.empty((len(inp), len(inp[0])), dtype=np.int32)

for i, line in enumerate(inp):
    for j, tile in enumerate(line):
        tiles[i, j] = ord(tile)
        if tile == 'S':
            s_pos = (i, j)

cur_tile = s_pos
for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
    s_links = [(di, dj)]
    link = (-di, -dj)
    new_tile = (cur_tile[0] + di, cur_tile[1] + dj)
    path_tiles = set()
    path_tiles.add(cur_tile)
    while new_tile != s_pos and tile_has_link(new_tile[0], new_tile[1], link):
        path_tiles.add(new_tile)
        new_tile_links = links[tiles[new_tile[0], new_tile[1]]]
        other_link = [l for l in new_tile_links if l != link][0]
        cur_tile = new_tile
        new_tile = (cur_tile[0] + other_link[0], cur_tile[1] + other_link[1])
        link = (-other_link[0], -other_link[1])

    if new_tile == s_pos:
        s_links.append(link)
        print('Found loop with', len(path_tiles), 'nodes')
        break


# Replacing S appropriately
for key, value in links.items():
    if s_links[0] in value and s_links[1] in value:
        tiles[s_pos] = key


print('Answer 1:', int(math.ceil((len(path_tiles) - 1) / 2)))

counting = 0
enclosed = 0
for i in range(tiles.shape[0]):
    line = tiles[i]
    last_path_char = ''
    for j in range(tiles.shape[1]):
        tile = line[j]
        c = chr(tile)
        if (i, j) in path_tiles:
            if c == '-':
                continue
            if c == '|' or c == 'J' and last_path_char == 'F' or c == '7' and last_path_char == 'L':
                counting = not counting
            last_path_char = c
            continue
        if counting:
            enclosed += 1
            tiles[i, j] = ord('I')
        else:
            tiles[i, j] = ord('O')
    # print_tiles()
    # print('Enclosed', enclosed)

print('Answer 2:', enclosed)
