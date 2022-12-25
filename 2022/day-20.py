# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 20.

Created on Sun Dec 25 10:18:42 2022

@author: Eftychios
"""

import os

import datetime as dt

from typing import Iterator
from dataclasses import dataclass, replace

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """1
2
-3
3
-2
0
4"""

with open("inputs/day-20.txt", "r") as f:
    inp_string = f.read()


def get_index_at(arr: list[int], idx: int) -> int:

    return idx % len(arr)


nums = [int(i) for i in inp_string.split('\n')]

moved = [False] * len(nums)
idx = 0
while not all(moved):
    if moved[idx]:
        idx += 1
        continue

    num = nums.pop(idx)
    moved.pop(idx)
    new_pos = idx + num
    new_idx = get_index_at(nums, new_pos)

    nums.insert(new_idx, num)
    moved.insert(new_idx, True)

for i, num in enumerate(nums):
    if num == 0:
        zero_idx = i
        break

zero1000 = nums[get_index_at(nums, zero_idx + 1000)]
zero2000 = nums[get_index_at(nums, zero_idx + 2000)]
zero3000 = nums[get_index_at(nums, zero_idx + 3000)]

print('Answer 1:', zero1000 + zero2000 + zero3000)


nums = [811589153 * int(i) for i in inp_string.split('\n')]
order = list(range(len(nums)))

for mx in range(10):
    for ord_idx in range(len(nums)):
        idx = order.index(ord_idx)

        num = nums.pop(idx)
        order.pop(idx)
        new_pos = idx + num
        new_idx = get_index_at(nums, new_pos)

        nums.insert(new_idx, num)
        order.insert(new_idx, ord_idx)

#    print('Mixing round', mx, '=', nums)

for i, num in enumerate(nums):
    if num == 0:
        zero_idx = i
        break


zero1000 = nums[get_index_at(nums, zero_idx + 1000)]
zero2000 = nums[get_index_at(nums, zero_idx + 2000)]
zero3000 = nums[get_index_at(nums, zero_idx + 3000)]

print('Answer 2:', zero1000 + zero2000 + zero3000)

