# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 20:23:05 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List, NamedTuple
import numpy as np
import threading

os.chdir("C:/Repos/advent-of-code-python/2019")


class BugSpaceGenerator:
    def get_bug_space(self, initial: str) -> BugSpace:
        return BugSpace(initial, self)

    def get_empty_bug_space(self,
                            depth: int,
                            inner_space: BugSpace = None,
                            outer_space: BugSpace = None) -> BugSpace:
        return BugSpace('.'*25, self,
                        depth,
                        inner_space,
                        outer_space)

class BugSpace:
    def __init__(self,
                 initial: str,
                 bsg: BugSpaceGenerator,
                 depth: int = 0,
                 inner_space: BugSpace = None,
                 outer_space: BugSpace = None):
        self.space = []
        self.bsg = bsg
        self.depth = depth

        for ch in initial:
            if ch == '.' or ch == '?':
                self.space.append(False)
            elif ch == '#':
                self.space.append(True)

        self.inner_space: BugSpace = inner_space
        self.outer_space: BugSpace = outer_space
        self.evolved_space = None

    def has_inner_bugs(self) -> int:
        ret = sum(self.space[6:9] + self.space[11:14] + self.space[16:19])
        #print('depth', self.depth, 'has', ret, 'inner bugs')
        return ret > 0

    def has_outer_bugs(self) -> int:
        ret = sum([self.east_bugs(),
                   self.west_bugs(),
                   sum(self.space[1:4]),
                   sum(self.space[21:24])])

        #print('depth', self.depth, 'has', ret, 'outer bugs')

        return ret

    def has_bugs(self) -> bool:
        return any(self.space)

    def north_bugs(self) -> int:
        return sum(self.space[0:5])

    def south_bugs(self) -> int:
        return sum(self.space[20:25])

    def east_bugs(self) -> int:
        return sum([self.get_cell(c * 5 + 4)
                    for c in range(0, 5)])

    def west_bugs(self) -> int:
        return sum([self.get_cell(c * 5)
                    for c in range(0, 5)])

    def bug_space_bugs(self) -> int:
        return sum(self.space)

    def all_bugs(self) -> int:
        ret = self.bug_space_bugs()

        bs = self
        while bs.inner_space is not None:
            bs = bs.inner_space
            ret += bs.bug_space_bugs()

        bs = self
        while bs.outer_space is not None:
            bs = bs.outer_space
            ret += bs.bug_space_bugs()

        return ret

    def get_cell(self, idx: int):
        if idx < 0 or idx > 24:
            return False
        return self.space[idx]

    def count_adjacent_bugs(self,
                            cell: int):

        mod5 = cell % 5

        adj = [cell - 5,  # cell above
               cell + 5,  # cell below
               mod5 - 1 + 5 * (cell // 5) if mod5 > 0 else -1,  # left cell
               mod5 + 1 + 5 * (cell // 5) if mod5 < 4 else -1]  # right cell

        return sum([self.get_cell(a) for a in adj])

    def count_adjacent_bugs_rec(self, cell: int):

        adjacent = 0

        # north border
        if cell < 5:
            if self.outer_space is not None:
                adjacent += self.outer_space.space[7]
        elif cell == 17:
            if self.inner_space is not None:
                adjacent += self.inner_space.south_bugs()
        else:
            adjacent += self.space[cell - 5]

        # south border
        if cell > 19:
            if self.outer_space is not None:
                adjacent += self.outer_space.space[17]
        elif cell == 7:
            if self.inner_space is not None:
                adjacent += self.inner_space.north_bugs()
        else:
            adjacent += self.space[cell + 5]

        mod5 = cell % 5

        # east border
        if mod5 == 4:
            if self.outer_space is not None:
                adjacent += self.outer_space.space[13]
        elif cell == 11:
            if self.inner_space is not None:
                adjacent += self.inner_space.west_bugs()
        else:
            adjacent += self.get_cell(
                    mod5 + 1 + 5 * (cell // 5) if mod5 < 4 else -1)

        # west border
        if mod5 == 0:
            if self.outer_space is not None:
                adjacent += self.outer_space.space[11]
        elif cell == 13:
            if self.inner_space is not None:
                adjacent += self.inner_space.east_bugs()
        else:
            adjacent += self.get_cell(
                    mod5 - 1 + 5 * (cell // 5) if mod5 > 0 else -1)

        return adjacent

    def evolve(self):
        evolved_space = []

        for cell, bug in enumerate(self.space):
            adjacent = self.count_adjacent_bugs(cell)
            if bug and adjacent == 1:
                evolved_space.append(True)
            elif not bug and (adjacent == 1 or adjacent == 2):
                evolved_space.append(True)
            else:
                evolved_space.append(False)

        self.space = evolved_space

    def evolve_is_prepared(self):
        return self.evolved_space is not None

    def prepare_evolve(self):
        if self.inner_space is None and self.has_inner_bugs():
            self.inner_space = self.bsg.get_empty_bug_space(
                    depth=self.depth+1,
                    outer_space=self)

        if self.outer_space is None and self.has_outer_bugs():
            self.outer_space = self.bsg.get_empty_bug_space(
                    depth=self.depth-1,
                    inner_space=self)

        evolved_space = []

        for cell, bug in enumerate(self.space):
            if cell == 12:  # ignoring middle cell
                evolved_space.append(False)
                continue
            adjacent = self.count_adjacent_bugs_rec(cell)
            if bug and adjacent == 1:
                evolved_space.append(True)
            elif not bug and (adjacent == 1 or adjacent == 2):
                evolved_space.append(True)
            else:
                evolved_space.append(False)

        self.evolved_space = evolved_space

        if (self.inner_space is not None and
            not self.inner_space.evolve_is_prepared()):
            self.inner_space.prepare_evolve()
        if (self.outer_space is not None and
            not self.outer_space.evolve_is_prepared()):
            self.outer_space.prepare_evolve()

    def do_evolve(self):
        self.space = self.evolved_space
        self.evolved_space = None

        if (self.inner_space is not None and
            self.inner_space.evolve_is_prepared()):
            self.inner_space.do_evolve()

        if (self.outer_space is not None and
            self.outer_space.evolve_is_prepared()):
            self.outer_space.do_evolve()

    def calculate_biodiversity(self):

        bio = 0
        for cell, bug in enumerate(self.space):
            if bug:
                bio += 2**cell

        return bio

    def print_space(self):
        row = ''
        for cell, bug in enumerate(self.space):
            if cell > 0 and cell % 5 == 0:
                print(row)
                row = ''

            if cell == 12:
                row += '?'
            elif bug:
                row += '#'
            else:
                row += '.'

        print(row)

bsg = BugSpaceGenerator()

bs = bsg.get_bug_space("""##...
#.###
.#.#.
#....
..###""")

previous = []
while bs.space not in previous:
    previous.append(bs.space)
    bs.evolve()

answer_1 = bs.calculate_biodiversity()
print('answer_1', answer_1)
#18350099


bs = bsg.get_bug_space("""##...
#.###
.#.#.
#....
..###""")

for i in range(0, 200):
    bs.prepare_evolve()
    bs.do_evolve()

answer_2 = bs.all_bugs()
print('answer_2', answer_2)
#2037

if __name__ == "__main__":

    import unittest

    class TestAll(unittest.TestCase):

        def test_1(self):
            bs = bsg.get_bug_space("""....#
#..#.
#..##
..#..
#....""")

            for i in range(0, 10):
                bs.prepare_evolve()
                bs.do_evolve()

            self.assertEqual(bs.all_bugs(), 99)

    unittest.main()
