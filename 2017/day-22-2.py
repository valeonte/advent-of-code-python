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

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3


class Sporifica:
    def __init__(self, virus_map: str):

        rows = virus_map.split('\n')
        size_x = len(rows)
        size_y = len(rows[0])
        self.virus_map = np.zeros((size_x, size_y), dtype=int)
        self.cur_pos = (size_x // 2, size_y // 2)
        self.direction = 'N'
        self.infection_counter = 0

        for i, row in enumerate(rows):
            for j, ch in enumerate(row):
                self.virus_map[i, j] = INFECTED if ch == '#' else CLEAN

    def print_map(self) -> None:
        (rows, cols) = self.virus_map.shape

        for row in range(rows):
            ret = ''
            for col in range(cols):
                cur = self.virus_map[row, col]
                if cur == CLEAN:
                    ch = '.'
                elif cur == WEAKENED:
                    ch = 'W'
                elif cur == INFECTED:
                    ch = '#'
                else:
                    ch = 'F'

                if (row, col) == self.cur_pos:
                    ret += f'[{ch}]'
                else:
                    ret += f' {ch} '
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
                                     dtype=int)
            new_virus_map[:, 1:] = self.virus_map
            self.virus_map = new_virus_map

            y = 0
        elif x < 0:
            new_virus_map = np.zeros((self.virus_map.shape[0] + 1,
                                      self.virus_map.shape[1]),
                                     dtype=int)
            new_virus_map[1:, :] = self.virus_map
            self.virus_map = new_virus_map

            x = 0
        elif x >= self.virus_map.shape[0]:
            new_virus_map = np.zeros((self.virus_map.shape[0] + 1,
                                      self.virus_map.shape[1]),
                                     dtype=int)
            new_virus_map[:-1, :] = self.virus_map
            self.virus_map = new_virus_map
        elif y >= self.virus_map.shape[1]:
            new_virus_map = np.zeros((self.virus_map.shape[0],
                                      self.virus_map.shape[1] + 1),
                                     dtype=int)
            new_virus_map[:, :-1] = self.virus_map
            self.virus_map = new_virus_map

        self.cur_pos = (x, y)

    def burst(self) -> None:
        cur = self.virus_map[self.cur_pos]
        if cur == CLEAN:
            self.turn_left()
            self.virus_map[self.cur_pos] = WEAKENED
        elif cur == WEAKENED:
            self.infection_counter += 1
            self.virus_map[self.cur_pos] = INFECTED
        elif cur == INFECTED:
            self.turn_right()
            self.virus_map[self.cur_pos] = FLAGGED
        else:
            self.turn_left()
            self.turn_left()
            self.virus_map[self.cur_pos] = CLEAN

        self.move_forward()


virus_map = """..#
#..
..."""

s = Sporifica(inp)
s.print_map()
for i in range(10000000):
    s.burst()
    if i % 1000000 == 0:
        print(100*i/10000000, '%')

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

        def test_counter_1(self):
            virus_map = """..#
#..
..."""

            s = Sporifica(virus_map)
            for i in range(0, 100):
                s.burst()

            self.assertEqual(s.infection_counter, 26)

    unittest.main()
