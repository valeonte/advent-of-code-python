# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 23.

Created on Thu Dec 23 21:31:11 2021

@author: Eftychios
"""

import numpy as np

from dataclasses import dataclass
from typing import Iterator, Tuple


inp_string = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""


@dataclass
class Amphipod:
    """Represents an amphipod on the board."""

    row: int
    col: int

    no: int
    cost: int

    def in_hallway(self) -> bool:
        """Check if amphipod is in hallway."""
        return self.row == 1

    def position_col(self) -> int:
        """The col of the final position of the amphipod."""
        return (self.no - 1) * 2 + 3

    def in_position(self) -> bool:
        """Check if amphipod is in position."""
        return self.row != 1 and self.col == self.position_col()

    def get_valid_moves(self, board: np.array
                        ) -> Iterator[Tuple[np.array, int]]:
        """Get amphipod's valid moves in given board."""
        brd = board.copy()
        brd[self.row, self.col] = 9
        max_row, max_col = brd.shape
        max_row = max_row - 1
        max_col = max_col - 1
        changed = True
        while changed:
            changed = False
            for idx, val in np.ndenumerate(brd):
                if val != 0:
                    continue
                row, col = idx

                change = (row < max_row and brd[row + 1, col] == 9 or
                          row > 0 and brd[row - 1, col] == 9 or
                          col < max_col and brd[row, col + 1] == 9 or
                          col > 0 and brd[row, col - 1] == 9)
                if change:
                    brd[row, col] = 9
                    changed = True

        for idx, val in np.ndenumerate(brd):
            if val != 9:
                continue
            row, col = idx
            if row == self.row and col == self.col:
                continue

            # Amphipods cannot stop in front of rooms
            if row == 1 and col in [3, 5, 7, 9]:
                continue

            # If in hallway, it can only move to the final position
            if self.in_hallway() and (row == 1 or col != self.position_col()):
                continue

            # if not stopping in hallway, it must stop in the right room
            if row != 1 and col != self.position_col():
                continue

            ret = brd.copy()
            ret[ret == 9] = 0
            ret[row, col] = self.no

            cost = self.cost * (abs(row - self.row) + abs(col - self.col))

            yield ret, cost


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
            amphipods.append(Amphipod(row, col, amphi, 10 ** (amphi - 1)))
    while col < board.shape[1]:
        board[row, col] = 8
        col = col + 1


def print_board(board: np.array):
    """Print the board."""
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


print_board(board)

for brd, cost in amphipods[1].get_valid_moves(board):
    print_board(brd)
    print(cost)

