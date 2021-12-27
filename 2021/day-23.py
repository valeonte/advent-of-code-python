# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 23.

Created on Thu Dec 23 21:31:11 2021

@author: Eftychios
"""

import numpy as np

from typing import Iterator, Tuple, Set


inp_string = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""


inps = inp_string.split('\n')

board = None
amphipods = dict()
for row, inp in enumerate(inps):
    if board is None:
        board = np.zeros((len(inps), len(inp)), dtype=int)

    for col, ch in enumerate(inp):
        if ch == '#' or ch == ' ':
            board[row, col] = 9
        elif ch in ['A', 'B', 'C', 'D']:
            amphi = ord(ch) - 64
            if np.any(board == amphi):
                amphi = amphi + 4

            board[row, col] = amphi
    while col < board.shape[1]:
        board[row, col] = 9
        col = col + 1


def print_board(board: np.array):
    """Print the board."""
    rows, cols = board.shape
    for row in range(rows):
        line = ''
        for col in range(cols):
            val = board[row, col]
            if val == 9:
                ch = '#'
            elif val > 0:
                ch = chr(65 + (val - 1) % 4)
            else:
                ch = ' '

            line = line + ch
        print(line)


def get_valid_moves(amphipod: int, board: np.array, moved: Set[int]
                    ) -> Iterator[Tuple[np.array, int]]:
    """Get amphipod's valid moves in given board."""
    brd = board.copy()

    my_row, my_col = np.where(board == amphipod)
    my_row = my_row[0]
    my_col = my_col[0]

    # If amphipod has moved, and is in a room, it cannot move again
    if amphipod in moved and my_row != 1:
        return

    position_col = ((amphipod - 1) % 4) * 2 + 3
    my_cost = 10 ** ((amphipod - 1) % 4)

    max_row = 4
    max_col = 12
    changed = True
    while changed:
        changed = False
        for idx, val in np.ndenumerate(brd):
            if val != 0:
                continue
            row, col = idx

            change = (row < max_row and brd[row + 1, col] == amphipod or
                      row > 0 and brd[row - 1, col] == amphipod or
                      col < max_col and brd[row, col + 1] == amphipod or
                      col > 0 and brd[row, col - 1] == amphipod)
            if change:
                brd[row, col] = amphipod
                changed = True

    for idx, val in np.ndenumerate(brd):
        if val != amphipod:
            continue
        row, col = idx
        if row == my_row and col == my_col:
            continue

        # Amphipods cannot stop in front of rooms
        if row == 1 and col in [3, 5, 7, 9]:
            continue

        # If initially in hallway, it can only move to the final position
        if my_row == 1 and (row == 1 or col != position_col):
            continue

        # if not stopping in hallway, it must stop in the right room
        if row != 1 and col != position_col:
            continue

        ret = brd.copy()
        ret[ret == amphipod] = 0
        ret[row, col] = amphipod

        cost = my_cost * (abs(row - my_row) + abs(col - my_col))

        yield ret, cost


def board_is_solved(board: np.array) -> bool:
    """Check whether board is solved."""
    for row in [2, 3]:
        for col in [3, 5, 7, 9]:
            if board[row, col] != (col - 3) // 2 + 1:
                return False

    return True


def board_is_unsolvable(board: np.array, moved: Set[int]) -> bool:
    """Check if board is impossible to solve."""
    for i in range(4):
        col = 3 + i * 2
        am = board[2, col]
        # If piece at top is moved, and piece at bottom is not the same, boom
        if am in moved and board[3, col] != am:
            return True

    return False


def get_best_solution(board: np.array, cur_cost: int, best_cost: int,
                      moved: Set[int], depth: int):
    """Get the best solution for the given board."""
    print('Solving at depth', depth, 'and cur cost', cur_cost)
    print_board(board)
    if board_is_unsolvable(board, moved):
        print('Unsolvable board!')
        return None

    local_best = None
    for amphi in range(1, 9):
        sub_moved = moved.copy()
        sub_moved.add(amphi)
        for brd, cost in get_valid_moves(amphi, board, moved):
            if cur_cost + cost >= best_cost:
                continue

            if board_is_solved(brd):
                return cur_cost + cost

            sub_best = get_best_solution(brd, cur_cost + cost, best_cost,
                                         sub_moved, depth + 1)
            if sub_best is None:
                continue

            if sub_best < best_cost:
                best_cost = sub_best
                local_best = sub_best

    return local_best





print_board(board)


get_best_solution(board, 0, 10000000000, set(), 1)

# print('-----moves')
# for brd, cost in get_valid_moves(2, board):
#     print_board(brd)
#     print(cost)

