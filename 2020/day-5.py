# -*- coding: utf-8 -*-
"""
Day 5 Advent of Code 2020 file.

Created on Thu Dec 10 21:50:03 2020

@author: Eftychios
"""

import os
import re

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""

with open("inputs/day-5.txt", "r") as f:
    inp_string = f.read()


def get_seat_id(seat_str: str):
    """Get seat id from seat string."""
    bin_id = re.sub('(B|R)', '1', seat_str)
    bin_id = re.sub('(F|L)', '0', bin_id)

    return int(bin_id, 2)


all_seats = [get_seat_id(seat_str)
             for seat_str in inp_string.split("\n")]

print('Answer 1:', max(all_seats))

for i in range(min(all_seats), max(all_seats)):
    if i not in all_seats:
        break

print('Answer 2:', i)
