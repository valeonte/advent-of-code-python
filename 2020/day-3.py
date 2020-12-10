# -*- coding: utf-8 -*-
"""
Day 3 Advent of Code 2020 file.

@author: Eftychios
"""

import os
import re

import numpy as np

from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

with open("inputs/day-3.txt", "r") as f:
    inp_string = f.read()


@dataclass
class TreesArea:
    """TreesArea class."""

    def __init__(self, map_string: str):

        self.trees = []
        for i, line in enumerate(map_string.split("\n")):
            for tree in re.finditer('#', line):
                self.trees.append((i, tree.start()))

        self.height = i + 1
        self.width = len(line)

    def has_tree_at(self, row: int, col: int) -> bool:
        """Check for tree at coords."""
        col = col % self.width

        return (row, col) in self.trees

    def count_slop_trees(self, right: int, down: int) -> int:
        """Count the trees encountered for slope."""
        cur_row = 0
        cur_col = 0
        trees = 0

        while cur_row < self.height:
            cur_row += down
            cur_col += right

            if self.has_tree_at(cur_row, cur_col):
                trees += 1

        return trees


inp = []

ta = TreesArea(inp_string)

print('Answer 1:', ta.count_slop_trees(3, 1))

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print('Answer 2:', np.prod([ta.count_slop_trees(*slope)
                            for slope in slopes]))
