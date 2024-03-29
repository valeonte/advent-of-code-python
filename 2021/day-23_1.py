# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 23.

Created on Thu Dec 23 21:31:11 2021

@author: Eftychios
"""

import numpy as np

from typing import Iterator, Tuple, Dict


inp_string = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

inp_string = """#############
#...........#
###C#C#A#B###
  #D#D#B#A#
  #########"""


inps = inp_string.split('\n')

board = None
for row, inp in enumerate(inps):
    if board is None:
        board = np.ones((len(inps), len(inp)), dtype=int) * -1

    for col, ch in enumerate(inp):
        if ch == '#':
            board[row, col] = 9
        elif ch == '.':
            board[row, col] = 0
        elif ch in ['A', 'B', 'C', 'D']:
            amphi = (ord(ch) - 65) * 2 + 1
            if np.any(board == amphi):
                amphi = amphi + 1

            board[row, col] = amphi
    col += 1
    while col < board.shape[1]:
        board[row, col] = -1
        col = col + 1


def print_board(board: np.array):
    """Print the board."""
    rows, cols = board.shape
    for row in range(rows):
        line = ''
        for col in range(cols):
            val = board[row, col]
            if val == -1:
                ch = ' '
            elif val == 9:
                ch = '#'
            elif val > 0:
                ch = chr(65 + ((val - 1) // 2))
            else:
                ch = ' '

            line = line + ch
        print(line)


def get_amphipod_type(amphi: int) -> int:
    """0 for A, 1 for B, 2 for C and 3 for D."""
    return (amphi - 1) // 2


def moves_to_hallway_dest(board: np.array, start: Tuple[int, int], dest: Tuple[int, int]) -> int:
    """Get moves to destination, but only along hallway."""
    if start[0] != 1 or dest[0] != 1:
        raise Exception('eee')
    moves = 0
    if start[1] < dest[1]:
        rng = range(start[1] + 1, dest[1] + 1)
    else:
        rng = range(start[1] - 1, dest[1] - 1, -1)

    for j in rng:
        moves += 1
        if board[1, j] != 0:
            return -1
    
    return moves
    

def moves_to_dest(board: np.array, start: Tuple[int, int], dest: Tuple[int, int]) -> int:
    """Get moves to destination, if path is clear."""
    moves = 0
    if start[0] == 1:  # in hallway
        # first move to correct col
        hm = moves_to_hallway_dest(board, start, (1, dest[1]))
        if hm < 0:
            return -1
        moves += hm
        
        # then down
        for i in range(2, dest[0] + 1):
            moves += 1
            if board[i, dest[1]] != 0:
                return -1

        return moves

    # in room
    # first get to hallway
    for i in range(start[0] - 1, 0, -1):
        moves += 1
        if board[i, start[1]] != 0:
            return -1

    hm = moves_to_hallway_dest(board, (1, start[1]), dest)
    if hm < 0:
        return -1

    return moves + hm


def get_valid_moves(board: np.array, amph: Tuple[int, int]) -> Iterator[Tuple[int, int, int]]:
    """Get amphipod's valid moves in given board. Returns new position and moves taken."""
    amphi = board[amph]
    amphi_type = get_amphipod_type(amphi)
    amphi_room = amphi_type * 2 + 3

    if amph[0] == 1:  # in hallway
        # can only go directly in its room
        # first get to the room col
        if board[2, amphi_room] != 0 or board[3, amphi_room] != 0 and get_amphipod_type(board[3, amphi_room]) != amphi_type:
            # entrance blocked, or irrelecant amphipod in room
            return
        # at this point, room is either empty of half full
        moves = moves_to_dest(board, amph, (2, amphi_room))  # we get moves to get into the room
        if moves > 0:
            # path is clear
            if board[3, amphi_room] == 0:
                yield (3, amphi_room, moves + 1)
            else:
                yield (2, amphi_room, moves)
        return
    
    # in room, before its original move
    if amph[0] == 3 and (amph[1] == amphi_room or board[2, amph[1]] != 0):
        # already in position, or blocked
        return
    if amph[0] == 2 and amph[1] == amphi_room and get_amphipod_type(board[3, amphi_room]) == amphi_type:
        # in correct room, and correct type below, no reason to move
        return

    for dest in [(1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 11)]:
        moves = moves_to_dest(board, amph, dest)
        if moves > 0:
            yield (dest[0], dest[1], moves)


def board_is_solved(board: np.array) -> bool:
    """Check whether board is solved."""
    for row in [2, 3]:
        for col in [3, 5, 7, 9]:
            if get_amphipod_type(board[row, col]) != (col - 3) // 2:
                return False

    return True


best_cost_so_far: int = 1_000_000_000_000
grand_loop_count = 0

def get_all_solutions(board: np.array, moved: Dict[int, int], cost_so_far: int = 0) -> Iterator[int]:
    #print_board(board)
    if board_is_solved(board):
        yield cost_so_far
        return
    global grand_loop_count
    grand_loop_count += 1

    for amphipod, moves_made in moved.items():
        if cost_so_far >= best_cost_so_far - 1:
            break
        if moves_made > 1:  # done moving
            continue

        i, j = np.where(board == amphipod)
        amph = (i[0], j[0])
        valid_moves = list(get_valid_moves(board, amph))
        if len(valid_moves) == 0:
            continue
        if len(valid_moves) > 1:
            valid_moves = sorted(valid_moves, key=lambda x: x[2])
        move_cost = 10 ** get_amphipod_type(amphipod)

        moved[amphipod] += 1
        for i, j, moves in valid_moves:
            if cost_so_far >= best_cost_so_far - 1:
                break
            brd = board.copy()
            brd[i, j] = amphipod
            brd[amph] = 0
            new_cost_so_far = moves * move_cost + cost_so_far
            if new_cost_so_far >= best_cost_so_far - 1:
                continue
            for cost in get_all_solutions(brd, moved, new_cost_so_far):
                yield cost

        moved[amphipod] -= 1


moved = {a: 0 for a in range(1, 9)}
for cost in get_all_solutions(board, moved):
    print('Got solution with cost', cost, 'after', grand_loop_count, 'loops')
    if cost < best_cost_so_far:
        best_cost_so_far = cost

print('Answer 1:', best_cost_so_far, 'in', grand_loop_count, 'loops')
