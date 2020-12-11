# -*- coding: utf-8 -*-
"""
Day 11 Advent of Code 2020 file.

Created on Fri Dec 11 20:56:20 2020

@author: Eftychios
"""

import os
import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

with open("inputs/day-11.txt", "r") as f:
    inp_string = f.read()


def load_plan() -> np.array:
    """Load the plan from strings."""
    lines = inp_string.split("\n")
    plan = np.ones([len(lines) + 2, len(lines[0]) + 2]) * -1

    for row_no, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == 'L':
                plan[row_no + 1, col + 1] = 0
            elif ch == '#':
                plan[row_no + 1, col + 1] = 1

    return plan


def count_occuppied(plan: np.array):
    """Count the occuppied seats in the provided plan."""
    return sum([b
                for a in plan
                for b in a
                if b != -1])


def count_adjacent_occuppied(plan: np.array,
                             row: int,
                             col: int) -> int:
    """Count occuppied in adjacent seats as per rule 1."""
    count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if r == row and c == col:
                continue
            if plan[r, c] == 1:
                count += 1

    return count


def count_adjacent_occuppied2(plan: np.array,
                              row: int,
                              col: int) -> int:
    """Count occuppied in adjacent seats as per rule 2."""
    rows, cols = plan.shape

    count = 0

    # top
    r = row - 1
    while r > 0 and plan[r, col] == -1:
        r -= 1
    if plan[r, col] == 1:
        count += 1

    # bottom
    r = row + 1
    while r < rows-1 and plan[r, col] == -1:
        r += 1
    if plan[r, col] == 1:
        count += 1

    # left
    c = col - 1
    while c > 0 and plan[row, c] == -1:
        c -= 1
    if plan[row, c] == 1:
        count += 1

    # right
    c = col + 1
    while c < cols-1 and plan[row, c] == -1:
        c += 1
    if plan[row, c] == 1:
        count += 1

    # top left
    r = row - 1
    c = col - 1
    while r > 0 and c > 0 and plan[r, c] == -1:
        r -= 1
        c -= 1
    if plan[r, c] == 1:
        count += 1

    # top right
    r = row - 1
    c = col + 1
    while r > 0 and c < cols-1 and plan[r, c] == -1:
        r -= 1
        c += 1
    if plan[r, c] == 1:
        count += 1

    # bottom left
    r = row + 1
    c = col - 1
    while r < rows-1 and c > 0 and plan[r, c] == -1:
        r += 1
        c -= 1
    if plan[r, c] == 1:
        count += 1

    # bottom right
    r = row + 1
    c = col + 1
    while r < rows-1 and c < cols-1 and plan[r, c] == -1:
        r += 1
        c += 1
    if plan[r, c] == 1:
        count += 1

    return count


def run_round(plan: np.array,
              new_method: bool = False) -> (bool, np.array):
    """Run a round of seating."""
    rows, cols = plan.shape
    new_plan = np.ones(plan.shape) * -1
    changed = False
    occ_threshold = 4 if new_method else 3

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            seat = plan[r, c]
            if seat == -1:
                continue

            if new_method:
                adj_occ = count_adjacent_occuppied2(plan, r, c)
            else:
                adj_occ = count_adjacent_occuppied(plan, r, c)

            if seat == 0 and adj_occ == 0:
                changed = True
                seat = 1
            elif seat == 1 and adj_occ > occ_threshold:
                changed = True
                seat = 0

            new_plan[r, c] = seat

    return changed, new_plan


def print_plan(plan: np.array):
    """Print plan."""
    rows, cols = plan.shape
    ret = []
    for row in plan[1:rows-1, 1:cols-1]:
        line = ''
        for cell in row:
            if cell == -1:
                line += '.'
            elif cell == 0:
                line += 'L'
            elif cell == 1:
                line += '#'
        ret.append(line)

    ret.append('-' * (cols + 10))

    print('\n'.join(ret))


plan = load_plan()

changed = True
while changed:
    changed, plan = run_round(plan)

print_plan(plan)

print('Answer 1:', count_occuppied(plan))

plan = load_plan()

changed = True
while changed:
    changed, plan = run_round(plan, new_method=True)

print_plan(plan)


print('Answer 2:', count_occuppied(plan))
