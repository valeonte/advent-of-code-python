# -*- coding: utf-8 -*-
"""
Day 20 Advent of Code 2020 file.

Created on Thu Dec 31 18:48:35 2020

@author: Eftychios
"""

import os

from typing import Dict, List, Tuple, Iterator
from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

# with open("inputs/day-20.txt", "r") as f:
#     inp_string = f.read()


class Tile:
    """A tile with its functionality."""

    def __init__(self, tile_id: int, tile_rows: List[str]):
        self.tile_id = tile_id
        self.tile_rows = [row.replace('.', '0').replace('#', '1')
                          for row in tile_rows]
        self.side = len(self.tile_rows)

        self.potential_edges = self.get_all_potential_edges()

    def get_current_edges(self) -> Tuple[int, int, int, int]:
        """Return current edges as top, bottom, left, right."""
        top = int(self.tile_rows[0], 2)
        bottom = int(self.tile_rows[-1], 2)
        left = int(''.join([r[0] for r in self.tile_rows]), 2)
        right = int(''.join([r[-1] for r in self.tile_rows]), 2)

        return (top, bottom, left, right)

    def get_all_potential_edges(self) -> Dict[str,
                                              Tuple[int, int, int, int]]:
        """Return a dictionary with all potential edge sets.

        (rotates, l_r_flips, t_b_flips) -> (top, bottom, left, right)
        """
        orig_rows = self.tile_rows

        ret = dict()

        for i in range(0, 4):
            self.rotate_right(i)
            for j in range(0, 2):
                self.flip_l_r(j)
                for k in range(0, 2):
                    self.flip_t_b(k)
                    edges = self.get_current_edges()
                    if edges not in ret.values():
                        ret[f'rr{i}_lr{j}_tb{k}'] = edges

                    self.tile_rows = orig_rows

        for j in range(0, 2):
            self.flip_l_r(j)
            for i in range(0, 4):
                self.rotate_right(i)
                for k in range(0, 2):
                    self.flip_t_b(k)
                    edges = self.get_current_edges()
                    if edges not in ret.values():
                        ret[f'lr{j}_rr{i}_tb{k}'] = edges

                    self.tile_rows = orig_rows

        for j in range(0, 2):
            self.flip_l_r(j)
            for k in range(0, 2):
                self.flip_t_b(k)
                for i in range(0, 4):
                    self.rotate_right(i)
                    edges = self.get_current_edges()
                    if edges not in ret.values():
                        ret[f'lr{j}_tb{k}_rr{i}'] = edges

                    self.tile_rows = orig_rows

        for k in range(0, 2):
            self.flip_t_b(k)
            for j in range(0, 2):
                self.flip_l_r(j)
                for i in range(0, 4):
                    self.rotate_right(i)
                    edges = self.get_current_edges()
                    if edges not in ret.values():
                        ret[f'tb{k}_lr{j}_rr{i}'] = edges

                    self.tile_rows = orig_rows

        for k in range(0, 2):
            self.flip_t_b(k)
            for i in range(0, 4):
                self.rotate_right(i)
                for j in range(0, 2):
                    self.flip_l_r(j)
                    edges = self.get_current_edges()
                    if edges not in ret.values():
                        ret[f'tb{k}_rr{i}_lr{j}'] = edges

                    self.tile_rows = orig_rows

        for i in range(0, 4):
            self.rotate_right(i)
            for k in range(0, 2):
                self.flip_t_b(k)
                for j in range(0, 2):
                    self.flip_l_r(j)
                    edges = self.get_current_edges()
                    if edges not in ret.values():
                        ret[f'rr{i}_tb{k}_lr{j}'] = edges

                    self.tile_rows = orig_rows

        return ret

    def rotate_right(self, times: int):
        """Rotate the tile once to the right."""
        for i in range(0, times):
            new_rows = [''] * self.side
            self.tile_rows.reverse()

            for row in self.tile_rows:
                for i, ch in enumerate(row):
                    new_rows[i] += ch

            self.tile_rows = new_rows

    def flip_l_r(self, times: int):
        """Flip the tile, left to right."""
        for i in range(0, times):
            new_rows = []
            for row in self.tile_rows:
                new_rows.append(row[::-1])

            self.tile_rows = new_rows

    def flip_t_b(self, times: int):
        """Flip the tile, top to bottom."""
        for i in range(0, times):
            self.tile_rows = self.tile_rows[::-1]

    def display(self):
        """Print out the tile."""
        for row in self.tile_rows:
            print(row)


rows = inp_string.split("\n")

tiles = []

idx = 0
tile_rows = None
tile_id = None
while idx < len(rows):
    row = rows[idx]
    if row.startswith('Tile'):
        if tile_id is not None:
            tiles.append(Tile(tile_id, tile_rows))

        tile_id = int(row[5:-1])
        tile_rows = []
    elif row != '':
        tile_rows.append(row.replace('.', '0').replace('#', '1'))

    idx += 1

tiles.append(Tile(tile_id, tile_rows))

tiles[0].potential_edges
