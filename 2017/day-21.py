# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:36:40 2020

@author: Eftychios
"""

import os
import time
import re

import numpy as np


from dataclasses import dataclass
from typing import Set

os.chdir("C:/Repos/advent-of-code-python/2017")

with open("inputs/day21.txt", "r") as f:
    inp = f.read()


class FractalArtist:
    def __init__(self, rulebook: str):

        self.pattern = np.array([[0, 1, 0],
                                 [0, 0, 1],
                                 [1, 1, 1]], dtype=bool)

        self.rules = {}
        for rule in rulebook.split('\n'):
            parts = rule.split(' => ')
            source = parts[0]
            target = self.str_to_array(parts[1])

            source_arr = self.str_to_array(source)
            for k in range(0, 4):
                source_new = np.rot90(source_arr, k)

                for ax in [None, 0, 1, (0, 1)]:

                    if ax is not None:
                        source_new = np.flip(source_arr, ax)
                    for kk in range(0, 4):
                        source_new = np.rot90(source_new, kk)

                        source_new_str = self.array_to_str(source_new)
                        if source_new_str in self.rules:
                            continue
                        self.rules[source_new_str] = target

    def str_to_array(self, str_array: str) -> np.ndarray:
        parts = str_array.split('/')

        ret = np.zeros([len(parts), len(parts)], dtype=bool)

        for i, part in enumerate(parts):
            for j, ch in enumerate(part):
                ret[i, j] = ch == '#'

        return ret

    def array_to_str(self, arr: np.ndarray) -> str:
        ret = ''
        for i in range(0, len(arr)):
            if i > 0:
                ret += '/'
            for j in range(0, len(arr)):
                if arr[i, j]:
                    ret += '#'
                else:
                    ret += '.'

        return ret

    def print_str(self, str_array: str) -> None:
        for row in str_array.split('/'):
            print(row)

    def print_arr(self, arr: np.ndarray) -> None:
        self.print_str(self.array_to_str(arr))

    def enhance(self):
        size = len(self.pattern)
        if size % 2 == 0:
            step = 2
        else:
            step = 3

        fractals = size // step
        new_size = fractals * (step + 1)
        new_pattern = np.zeros([new_size, new_size], dtype=bool)

        for row in range(0, fractals):
            for col in range(0, fractals):
                i = row * step
                j = col * step
                fractal = self.pattern[i:i + step, j:j + step]
                key = self.array_to_str(fractal)
                new_fractal = self.rules[key]

                i_new = row * (step + 1)
                j_new = col * (step + 1)
                new_pattern[i_new:i_new + step + 1,
                            j_new:j_new + step + 1] = new_fractal

        self.pattern = new_pattern




rulebook = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

fa = FractalArtist(inp)

for it in range(0, 5):
    fa.enhance()

answer_1 = sum(sum(fa.pattern))

for it in range(0, 13):
    fa.enhance()
answer_2 = sum(sum(fa.pattern))

print(answer_1, answer_2)


if __name__ == '__main__':

    import unittest

    class TestAll(unittest.TestCase):

        def test_init(self):
            rulebook = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

            fa = FractalArtist(rulebook)

            self.assertEqual(len(fa.rules), 12)

        def test_enhance_1(self):
            rulebook = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

            fa = FractalArtist(rulebook)
            fa.enhance()

            self.assertEqual(fa.array_to_str(fa.pattern),
                             '#..#/..../..../#..#')

        def test_enhance_2(self):
            rulebook = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

            fa = FractalArtist(rulebook)
            fa.enhance()
            fa.enhance()

            self.assertEqual(fa.array_to_str(fa.pattern),
                             '##.##./#..#../....../##.##./#..#../......')

    unittest.main()
