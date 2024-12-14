"""
Advent of Code 2024 day 11.

Created on Fri Dec 13 2024 23:29:38 PM

@author: Eftychios
"""

import os
import math

from functools import lru_cache
from typing import Dict, Iterable, List, Set, Tuple


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """125 17"""


with open("inputs/day-11.txt", "r") as f:
    inp_string = f.read()


stones = [int(num) for num in inp_string.split(' ')]


blinks = 0
while blinks < 25:
    i = 0
    while i < len(stones):
        stone = stones[i]
        if stone == 0:
            stones[i] = 1
        else:
            num_digits = int(math.floor(math.log10(stone))) + 1
            if num_digits % 2 == 0:
                splitter = 10 ** (num_digits // 2)
                stones[i] = stone // splitter
                stones.insert(i + 1, stone % splitter)
                i += 1
            else:
                stones[i] = stone * 2024
        i += 1
    blinks += 1


print('Answer 1:', len(stones))


# How each stone develops has nothing to do with neighbours.
stones = [int(num) for num in inp_string.split(' ')]

@lru_cache(maxsize=500)
def get_length_of_number_in_blinks(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    if stone == 0:
        return get_length_of_number_in_blinks(1, blinks - 1)

    num_digits = int(math.floor(math.log10(stone))) + 1
    if num_digits % 2 == 0:
        splitter = 10 ** (num_digits // 2)
        left = stone // splitter
        right = stone % splitter
        return get_length_of_number_in_blinks(left, blinks=blinks-1) + get_length_of_number_in_blinks(right, blinks=blinks-1)

    return get_length_of_number_in_blinks(stone * 2024, blinks=blinks-1)


ret = 0
for num in stones:
    ret += get_length_of_number_in_blinks(num, blinks=25)

print('Redo answer 1:', ret)


ret = 0
for num in stones:
    ret += get_length_of_number_in_blinks(num, blinks=75)

print('Answer 1:', ret)
    
    
    