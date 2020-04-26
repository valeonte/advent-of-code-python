# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:40:47 2020

@author: Eftychios
"""

import os

import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2017")

with open("inputs/day22.txt", "r") as f:
    inp = f.read()


class Sporifica:
    def __init__(self, virus_map: str):

        rows = virus_map.split('\n')
        size_x = len(rows)
        size_y = len(rows[0])
        self.virus_map = np.zeros((size_x, size_y), dtype=bool)
        self.cur_pos = (size_x // 2, size_y // 2)
        self.direction = 'N'
        self.infection_counter = 0

        for i, row in enumerate(rows):
            for j, ch in enumerate(row):
                self.virus_map[i, j] = ch == '#'

    def print_map(self) -> None:
        (rows, cols) = self.virus_map.shape

        for row in range(0, rows):
            ret = ''
            for col in range(0, cols):
                if (row, col) == self.cur_pos:
                    ret += '[#]' if self.virus_map[row, col] else '[.]'
                else:
                    ret += ' # ' if self.virus_map[row, col] else ' . '
            print(ret)

    def turn_right(self):
        if self.direction == 'N':
            self.direction = 'E'
        elif self.direction == 'E':
            self.direction = 'S'
        elif self.direction == 'S':
            self.direction = 'W'
        else:
            self.direction = 'N'

    def turn_left(self):
        if self.direction == 'N':
            self.direction = 'W'
        elif self.direction == 'W':
            self.direction = 'S'
        elif self.direction == 'S':
            self.direction = 'E'
        else:
            self.direction = 'N'

    def move_forward(self):
        if self.direction == 'N':
            self.set_cur_pos(self.cur_pos[0] - 1, self.cur_pos[1])
        elif self.direction == 'W':
            self.set_cur_pos(self.cur_pos[0], self.cur_pos[1] - 1)
        elif self.direction == 'S':
            self.set_cur_pos(self.cur_pos[0] + 1, self.cur_pos[1])
        else:
            self.set_cur_pos(self.cur_pos[0], self.cur_pos[1] + 1)

    def set_cur_pos(self, x, y):
        if y < 0:
            new_virus_map = np.zeros((self.virus_map.shape[0],
                                      self.virus_map.shape[1] + 1),
                                     dtype=bool)
            new_virus_map[:, 1:] = self.virus_map
            self.virus_map = new_virus_map

            y = 0
        elif x < 0:
            new_virus_map = np.zeros((self.virus_map.shape[0] + 1,
                                      self.virus_map.shape[1]),
                                     dtype=bool)
            new_virus_map[1:, :] = self.virus_map
            self.virus_map = new_virus_map

            x = 0
        elif x >= self.virus_map.shape[0]:
            new_virus_map = np.zeros((self.virus_map.shape[0] + 1,
                                      self.virus_map.shape[1]),
                                     dtype=bool)
            new_virus_map[:-1, :] = self.virus_map
            self.virus_map = new_virus_map
        elif y >= self.virus_map.shape[1]:
            new_virus_map = np.zeros((self.virus_map.shape[0],
                                      self.virus_map.shape[1] + 1),
                                     dtype=bool)
            new_virus_map[:, :-1] = self.virus_map
            self.virus_map = new_virus_map

        self.cur_pos = (x, y)

    def burst(self) -> None:
        cur = self.virus_map[self.cur_pos]
        if cur:
            self.turn_right()
        else:
            self.turn_left()

        if cur:
            self.virus_map[self.cur_pos] = False
        else:
            self.infection_counter += 1
            self.virus_map[self.cur_pos] = True

        self.move_forward()


virus_map = """..#
#..
..."""

s = Sporifica(inp)
for i in range(0, 10000):
    s.burst()
#    s.print_map()
#    input('pres a key')

print(s.infection_counter)


if __name__ == '__main__':

    import unittest

    class TestAll(unittest.TestCase):

        def test_init(self):
            virus_map = """..#
#..
..."""

            s = Sporifica(virus_map)

            self.assertEqual(s.virus_map.shape, (3, 3))

        def test_burst_1(self):
            virus_map = """..#
#..
..."""

            s = Sporifica(virus_map)
            s.burst()

            self.assertEqual(s.cur_pos, (1, 0))

        def test_burst_2(self):
            virus_map = """..#
#..
..."""

            s = Sporifica(virus_map)
            s.burst()
            s.burst()

            self.assertEqual(s.cur_pos, (0, 0))

        def test_counter_1(self):
            virus_map = """..#
#..
..."""

            s = Sporifica(virus_map)
            for i in range(0, 7):
                s.burst()

            self.assertEqual(s.infection_counter, 5)

        def test_counter_2(self):
            virus_map = """..#
#..
..."""

            s = Sporifica(virus_map)
            for i in range(0, 70):
                s.burst()

            self.assertEqual(s.infection_counter, 41)

        def test_counter_3(self):
            virus_map = """..#
#..
..."""

            s = Sporifica(virus_map)
            for i in range(0, 10000):
                s.burst()

            self.assertEqual(s.infection_counter, 5587)

    unittest.main()
