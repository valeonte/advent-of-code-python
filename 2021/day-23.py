# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 23.

Created on Thu Dec 23 21:31:11 2021

@author: Eftychios
"""

import numpy as np

from dataclasses import dataclass
from typing import Iterator


inp_string = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""


@dataclass
class Amphipod:
    row: int
    col: int

    cost: int

    def get_valid_moves(self, board: np.array) -> Iterator[np.array, int]:
        """Get amphipod's valid moves in given board."""
        brd = board.copy()
        changed = True
        while changed:
        for idx, val in np.ndenumerate(board):
            if val != 0:
                continue
            row, col = idx



inps = inp_string.split('\n')

board = None
amphipods = list()
for row, inp in enumerate(inps):
    if board is None:
        board = np.zeros((len(inps), len(inp)), dtype=int)

    for col, ch in enumerate(inp):
        if ch == '#' or ch == ' ':
            board[row, col] = 8
        elif ch in ['A', 'B', 'C', 'D']:
            amphi = ord(ch) - 64
            board[row, col] = amphi
            amphipods.append(Amphipod(row, col, 10 ** (amphi - 1)))
    while col < board.shape[1]:
        board[row, col] = 8
        col = col + 1


def print_board():
    rows, cols = board.shape
    for row in range(rows):
        line = ''
        for col in range(cols):
            val = board[row, col]
            if val == 8:
                ch = '#'
            elif val > 0:
                ch = chr(64 + val)
            else:
                ch = ' '

            line = line + ch
        print(line)


print_board()

