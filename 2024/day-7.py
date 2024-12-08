"""
Advent of Code 2024 day 7.

Created on Sat Dec 07 2024 5:58:25 PM

@author: Eftychios
"""

import os
import math

from typing import List


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


with open("inputs/day-7.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")


def can_get_result(res: int, cur_op: int, next_ops: List[int], step2: bool = False):
    if cur_op == res and len(next_ops) == 0:
        return True
    if len(next_ops) == 0 or cur_op > res:
        return False

    next_op = next_ops[0]

    add_op = cur_op + next_op
    if can_get_result(res, add_op, next_ops[1:], step2):
        return True

    mul_op = cur_op * next_op
    if can_get_result(res, mul_op, next_ops[1:], step2):
        return True

    if step2:
        concat_op = cur_op * 10**(math.ceil(math.log10(next_op + 0.5))) + next_op  # We add 0.5 so that multiples of 10 produce accurate num of digits
        if can_get_result(res, concat_op, next_ops[1:], step2):
            return True

    return False


ret = 0
for row in inp:
    ro = row.split(':')
    result = int(ro[0])
    operands = [int(r) for r in ro[1].split()]

    if can_get_result(result, operands[0], operands[1:]):
        ret += result

print('Answer 1:', ret)


ret = 0
for row in inp:
    ro = row.split(':')
    result = int(ro[0])
    operands = [int(r) for r in ro[1].split()]

    if can_get_result(result, operands[0], operands[1:], step2=True):
        ret += result

print('Answer 2:', ret)
