# -*- coding: utf-8 -*-
"""
Advent of Code 2021 Day 4.

Created on Sat Dec  4 18:25:48 2021

@author: Eftychios
"""

import os

import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

with open("inputs/day-4.txt", "r") as f:
    inp_string = f.read()

# Parsing input

drawn = None

cur_board = np.zeros((5, 5))
cur_board_idx = 0
boards = []

for line in inp_string.split("\n"):
    if len(line) == 0:
        continue

    if drawn is None:
        drawn = [int(s) for s in line.split(',')]
        continue

    cur_board[cur_board_idx, :] = [int(s)
                                   for s in line.split(' ')
                                   if s != '']
    if cur_board_idx == 4:
        boards.append(cur_board)
        cur_board = np.zeros((5, 5))
        cur_board_idx = 0
    else:
        cur_board_idx = cur_board_idx + 1

marked = [np.zeros((5, 5), dtype=bool)
          for _ in range(len(boards))]

# Drawing numbers and marking
for i, num in enumerate(drawn):
    for j in range(len(boards)):
        new = boards[j] == num
        if new.any():
            new_marked = marked[j] | new
            marked[j] = new_marked
            got_row = any(new_marked.sum(axis=1) == 5)
            if got_row:
                print('Got row! Board', j + 1)
                break
            got_col = any(new_marked.sum(axis=0) == 5)
            if got_col:
                print('Got column! Board', j + 1)
                break

    if got_row or got_col:
        break

print('Answer 1:', sum(boards[j][~marked[j]]) * num)


boards_won = []
marked = [np.zeros((5, 5), dtype=bool)
          for _ in range(len(boards))]

# Drawing numbers and marking
for i, num in enumerate(drawn):
    for j in range(len(boards)):
        if j in boards_won:
            continue

        new = boards[j] == num
        if new.any():
            new_marked = marked[j] | new
            marked[j] = new_marked
            got_row = any(new_marked.sum(axis=1) == 5)
            if got_row:
                print('Got row! Board', j + 1)
                boards_won.append(j)
                continue
            got_col = any(new_marked.sum(axis=0) == 5)
            if got_col:
                print('Got column! Board', j + 1)
                boards_won.append(j)

    if len(boards_won) == len(boards):
        break

j = boards_won[-1]
print('Answer 2:', sum(boards[j][~marked[j]]) * num)
