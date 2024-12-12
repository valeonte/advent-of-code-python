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


with open("inputs/day-9.txt", "r") as f:
    inp_string = f.read()


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
# final = ''

while cur_end_block_idx > cur_idx:
    if reading_from_blocks:
        size = blocks[cur_idx]
        for i in range(size):
            ret += cur_pos * cur_idx
            cur_pos += 1
#             final += str(cur_idx)
    else:
        size = free_spaces[cur_idx]
        for i in range(size):
            ret += cur_pos * cur_end_block_idx
            cur_pos += 1
#             final += str(cur_end_block_idx)
            blocks[cur_end_block_idx] -= 1
            if blocks[cur_end_block_idx] == 0:
                cur_end_block_idx -= 1
                if cur_end_block_idx <= cur_idx:
                    break

        # Did one block, one free space, index increases
        cur_idx += 1
    
    reading_from_blocks = not reading_from_blocks


# Once more to take into account any left over blocks in the end
size = blocks[cur_idx]
for i in range(size):
    ret += cur_pos * cur_idx
    cur_pos += 1
#     final += str(cur_idx)


print('Answer 1:', ret)



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


# first add all blocks for checksum
ret = 0
cur_pos = 0

free_space_pos = []
block_pos = []
for idx, block_size in enumerate(blocks):
    block_pos.append(cur_pos)
    for i in range(block_size):
        ret += cur_pos * idx
        cur_pos += 1

    free_space_pos.append(cur_pos)
    if idx < len(free_spaces):
        cur_pos += free_spaces[idx]


# count down blocks to check for moves
for block_idx in range(len(blocks) - 1, -1, -1):
    block_size = blocks[block_idx]
    bp = block_pos[block_idx]
    for free_idx, free_size in enumerate(free_spaces):
        fp = free_space_pos[free_idx]
        if fp > bp:
            break
        if free_size < block_size:
            continue

        diff_pos = fp - bp
        ret += diff_pos * block_idx * block_size
        free_spaces[free_idx] -= block_size
        free_space_pos[free_idx] += block_size
        break



print('Answer 2:', ret)
