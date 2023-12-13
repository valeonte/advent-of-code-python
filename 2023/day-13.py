"""
Advent of Code 2023 day 13.

Created on Wed Dec 13 2023

@author: Eftychios
"""

import os

import numpy as np

from typing import List

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

with open("inputs/day-13.txt", "r") as f:
    inp_string = f.read()

inp = inp_string.split('\n')


def get_columns_left_reflect(pattern: List[List[int]]):
    """Look for vertical reflection and return columns on left."""
    pat = np.array(pattern)
    for ref in range(1, pat.shape[1]):
        is_reflector = True
        for comp in range(ref):
            if ref + comp >= pat.shape[1]:
                break
            if (pat[:, ref - comp - 1] != pat[:, ref + comp]).any():
                is_reflector = False
                break
        if is_reflector:
            print('Got vertical reflector between', ref, 'and', ref + 1)
            yield ref


def get_rows_top_reflect(pattern: List[List[int]]):
    """Look for horizontal reflection and return rows on top."""
    pat = np.array(pattern)
    for ref in range(1, pat.shape[0]):
        is_reflector = True
        for comp in range(ref):
            if ref + comp >= pat.shape[0]:
                break
            if (pat[ref - comp - 1, :] != pat[ref + comp, :]).any():
                is_reflector = False
                break
        if is_reflector:
            print('Got horizontal reflector between', ref, 'and', ref + 1)
            yield ref


pattern = []
cnt = 0
reflectors = []
for line in inp:
    if len(line) == 0:
        cnt += 1
        print('Pattern', cnt, 'complete')
        cols = 0
        for cols in get_columns_left_reflect(pattern):
            break
        rows = 0
        for rows in get_rows_top_reflect(pattern):
            break

        reflectors.append(cols + 100 * rows)

        pattern = []
        continue

    pattern.append([ch == '#' for ch in line])


cnt += 1
print('Pattern', cnt, 'complete')
cols = 0
for cols in get_columns_left_reflect(pattern):
    break
rows = 0
for rows in get_rows_top_reflect(pattern):
    break

reflectors.append(cols + 100 * rows)

print('Answer 1:', sum(reflectors))


def find_reflector_fixing_smudge(pattern: List[List[int]], previous: int):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            pattern[i][j] = not pattern[i][j]
            cols = 0
            for cols in get_columns_left_reflect(pattern):
                if cols == previous:
                    cols = 0
                    continue
                break

            rows = 0
            for rows in get_rows_top_reflect(pattern):
                if rows * 100 == previous:
                    rows = 0
                    continue
                break

            cr = cols + 100 * rows
            if cr == 0:
                pattern[i][j] = not pattern[i][j]
                continue
            
            print('Found smudge reflector', cr)
            return cr
    raise Exception('No smudge reflector found!')


pattern = []
cnt = 0
ret = 0
for line in inp:
    if len(line) == 0:
        print('Pattern', cnt + 1, 'complete')
        cr = find_reflector_fixing_smudge(pattern, reflectors[cnt])
        cnt += 1

        ret += cr

        pattern = []
        continue

    pattern.append([ch == '#' for ch in line])


print('Pattern', cnt + 1, 'complete')
cr = find_reflector_fixing_smudge(pattern, reflectors[cnt])

ret += cr

print('Answer 2:', ret)
