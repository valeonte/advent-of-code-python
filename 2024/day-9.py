"""
Advent of Code 2024 day 9.

Created on Tue Dec 10 2024 7:28:59 PM

@author: Eftychios
"""

import os
import math

from typing import Dict, Iterable, List, Set, Tuple


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """2333133121414131402"""


# with open("inputs/day-9.txt", "r") as f:
#     inp_string = f.read()


free_spaces = []
blocks = []
total_memory = 0

for i, ch in enumerate(inp_string):
    size = int(ch)
    total_memory += size
    if i % 2 == 0:
        blocks.append(size)
    else:
        free_spaces.append(size)


cur_pos = 0
cur_end_block_idx = len(blocks) - 1
reading_from_blocks = True
cur_idx = 0

ret = 0

while cur_end_block_idx > cur_idx:
    if reading_from_blocks:
        size = blocks[cur_idx]
        for i in range(size):
            ret += cur_pos * cur_idx
            cur_pos += 1
    else:
        size = free_spaces[cur_idx]
        for i in range(size):
            ret += cur_pos * cur_end_block_idx
            cur_pos += 1
            blocks[cur_end_block_idx] -= 1
            if blocks[cur_end_block_idx] == 0:
                cur_end_block_idx -= 1
                if cur_end_block_idx <= cur_idx:
                    break

        # Did one block, one free space, index increases
        cur_idx += 1
    
    reading_from_blocks = not reading_from_blocks

        



print('Answer 1:')
