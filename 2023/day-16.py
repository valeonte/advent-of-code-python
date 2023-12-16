"""
Advent of Code 2023 day 16.

Created on Σατ Dec 16 2023

@author: Eftychios
"""

import os

import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

with open("inputs/day-16.txt", "r") as f:
    inp_string = f.read()


inps = inp_string.split('\n')

lit = {'.': 0,
       '|': 0b001_0000,
       '/': 0b010_0000,
       '-': 0b011_0000,
       '\\': 0b100_0000,
       
       '^': 0b0001,
       '>': 0b0010,
       'v': 0b0100,
       '<': 0b1000}

for k, v in lit.copy().items():
    lit[v] = k


con = np.zeros((len(inps), len(inps[0])), dtype=np.int8)
for i, line in enumerate(inps):
    for j, ch in enumerate(line):
        if ch != '.':
            con[i, j] = lit[ch]

con_orig = con.copy()

def print_contraption(con: np.array):
    """Print contraption."""
    print('-' * 40)
    for line in con:
        row = ''
        for num in line:
            if num == 0:
                row += lit[num]
            elif num > 0b1111:
                row += lit[(num >> 4) << 4]
            else:
                dirs = ''
                for e in range(4):
                    dir = 2 ** e
                    if num & dir > 0:
                        dirs += lit[dir]
                if len(dirs) == 1:
                    row += dirs
                else:
                    row += str(len(dirs))

        print(row)


def count_energised_from_beam(i0: int, j0: int, dir0: str) -> int:
    to_process = [(i0, j0, dir0)]
    while len(to_process) > 0:
        #print_contraption(con)
        i, j, dir = to_process.pop(0)
        if i < 0 or i == con.shape[0] or j < 0 or j == con.shape[1]:
            # exceeded array bounds, nothing to do
            continue
        if con[i, j] & lit[dir] > 0:
                # direction already processed
                continue

        con[i, j] |= lit[dir]  # energising square with direction

        mirror = lit[(con[i, j] >> 4) << 4]
        if mirror == '|':
            if dir == '>' or dir == '<':
                to_process.append((i - 1, j, '^'))
                to_process.append((i + 1, j, 'v'))
            elif dir == 'v':
                to_process.append((i + 1, j, 'v'))
            elif dir == '^':
                to_process.append((i - 1, j, '^'))
        elif mirror == '/':
            if dir == '>':
                to_process.append((i - 1, j, '^'))
            elif dir == '<':
                to_process.append((i + 1, j, 'v'))
            elif dir == 'v':
                to_process.append((i, j - 1, '<'))
            elif dir == '^':
                to_process.append((i, j + 1, '>'))
        elif mirror == '-':
            if dir == '^' or dir == 'v':
                to_process.append((i, j - 1, '<'))
                to_process.append((i, j + 1, '>'))
            elif dir == '>':
                to_process.append((i, j + 1, '>'))
            elif dir == '<':
                to_process.append((i, j - 1, '<'))
        elif mirror == '\\':
            if dir == '>':
                to_process.append((i + 1, j, 'v'))
            elif dir == '<':
                to_process.append((i - 1, j, '^'))
            elif dir == 'v':
                to_process.append((i, j + 1, '>'))
            elif dir == '^':
                to_process.append((i, j - 1, '<'))
        else:
            # no mirror
            if dir == '>':
                to_process.append((i, j + 1, '>'))
            elif dir == '<':
                to_process.append((i, j - 1, '<'))
            elif dir == 'v':
                to_process.append((i + 1, j, 'v'))
            elif dir == '^':
                to_process.append((i - 1, j, '^'))

    return ((con & 0b1111) > 0).sum()

print('Answer 1', count_energised_from_beam(0, 0, '>'))


best = 0
for i0 in range(con.shape[0]):
    con = con_orig.copy()
    en = count_energised_from_beam(i0, 0, '>')
    if en > best:
        print('Got new best', en, 'for:', i0, '0', '>')
        best = en

    con = con_orig.copy()
    en = count_energised_from_beam(i0, con.shape[1] - 1, '<')
    if en > best:
        print('Got new best', en, 'for:', i0, con.shape[1] - 1, '<')
        best = en

for j0 in range(con.shape[1]):
    con = con_orig.copy()
    en = count_energised_from_beam(0, j0, 'v')
    if en > best:
        print('Got new best', en, 'for: 0', j0, 'v')
        best = en

    con = con_orig.copy()
    en = count_energised_from_beam(0, con.shape[0] - 1, '^')
    if en > best:
        print('Got new best', en, 'for:', con.shape[0] - 1, j0, '^')
        best = en


print('Answer 2:', best)
