"""
Advent of Code 2023 day 14.

Created on Thu Dec 14 2023

@author: Eftychios
"""

import os

import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

with open("inputs/day-14.txt", "r") as f:
    inp_string = f.read()

inp = inp_string.split('\n')


def print_space(mat: np.array):
    print('--------------------------------------')
    for row in mat:
        line = ''
        for num in row:
            if num == -1:
                line += '#'
            elif num == 0:
                line += '.'
            elif num == 1:
                line += 'O'
            else:
                raise Exception('Eee')
        print(line)


mat = np.zeros((len(inp), len(inp[0])))
for i, line in enumerate(inp):
    for j, ch in enumerate(line):
        if ch == 'O':
            mat[i, j] = 1
        elif ch == '#':
            mat[i, j] = -1

#print_space(mat)

def roll(mat: np.array, dim: int, dir: int) -> np.array:
    """Roll mat in rows (dim = 0) or cols (dim = 1), up (dir = -1) or down (dir = 1)."""
    mat = mat.copy()
    for m in range(mat.shape[dim]):
        last_roll_space = -1
        for n in range(mat.shape[1 - dim]):
            if dir == 1:
                n = mat.shape[1 - dim] - n - 1

            el = mat[m, n] if dim == 0 else mat[n, m]

            if el == 0:
                if last_roll_space < 0:
                    last_roll_space = n
            elif el == 1:
                if last_roll_space > -1:
                    if dim == 1:
                        mat[last_roll_space, m] = el
                        mat[n, m] = 0
                    else:
                        mat[m, last_roll_space] = el
                        mat[m, n] = 0
                    if dir == -1:
                        last_roll_space += 1
                    else:
                        last_roll_space -= 1
            elif el == -1:
                last_roll_space = -1
        #print_space(mat)
    return mat


rolled_mat = roll(mat, 1, -1)


def evaluate_mat(mat: np.array) -> int:
    rows = mat.shape[0]
    score = 0
    for (i, _), el in np.ndenumerate(mat):
        if el != 1:
            continue
        score += rows - i

    return score

print('Answer 1:', evaluate_mat(rolled_mat))


def roll_cycle(mat: np.array) -> np.array:
    ret = roll(mat, 1, -1) # north
    ret = roll(ret, 0, -1) # west
    ret = roll(ret, 1, 1) # south
    ret = roll(ret, 0, 1) # east

    return ret


intermediate = []
for i in range(1_000_000_000):
    mat = roll_cycle(mat)
    matched = False
    for j, inter in enumerate(intermediate):
        if (inter == mat).all():
            print('Iteration', i, 'matched intermediate', j)
            matched = True
            break
    if matched:
        break
    intermediate.append(mat)

period = i - j
offset = j

print('Period', period, 'at offset', offset)

remaining = (1_000_000_000 - offset) % period

print('Rolling remaining', remaining)
mat = intermediate[offset]
for i in range(remaining - 1):
    mat = roll_cycle(mat)

print('Answer 2:', evaluate_mat(mat))
