"""
Advent of Code 2024 day 17.

Created on Sat Dec 21 2024 1:19:37 AM

@author: Eftychios
"""

import re
import os
import math
import sys

import datetime as dt
import numpy as np

from functools import lru_cache
from typing import Dict, Iterable, List, Set, Tuple
from dataclasses import dataclass
from decimal import Decimal
from tqdm import tqdm, trange
from common import Dir
from itertools import product

# sys.setrecursionlimit(100000)
os.chdir("C:/Repos/advent-of-code-python/2024")


inp_string = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


# with open("inputs/day-17.txt", "r") as f:
#     inp_string = f.read()


@dataclass
class Machine:
    A: int = 0
    B: int = 0
    C: int = 0

    def combo_operand(self, operand: int) -> int:
        assert operand >= 0 and operand < 7, "Invalid operand"
        if operand < 4:
            return operand
        if operand == 4:
            return self.A
        if operand == 5:
            return self.B
        if operand == 6:
            return self.C

    def run_program(self, program: List[int]) -> List[int]:
        i = 0
        outputs = []
        while i < len(program):
            operand = program[i+1]
            if program[i] == 0:
                # adv
                self.A = int(self.A / 2**self.combo_operand(operand))
            elif program[i] == 1:
                # bxl
                self.B = self.B ^ operand
            elif program[i] == 2:
                # bst
                self.B = self.combo_operand(operand) % 8
            elif program[i] == 3:
                # jnz
                if self.A > 0:
                    i = operand
                    continue
            elif program[i] == 4:
                # bxc
                self.B = self.B ^ self.C
            elif program[i] == 5:
                # out
                outputs.append(self.combo_operand(operand) % 8)
            elif program[i] == 6:
                # bdv
                self.B = int(self.A / 2**self.combo_operand(operand))
            elif program[i] == 7:
                # cdv
                self.C = int(self.A / 2**self.combo_operand(operand))
            else:
                raise ValueError("Invalid opcode")

            i += 2

        return outputs


m = Machine(C=9)
m.run_program([2, 6])
assert m.B == 1

m = Machine(A=10)
ret = m.run_program([5,0,5,1,5,4])
assert ret == [0, 1, 2]

m = Machine(A=2024)
m.run_program([0,1,5,4,3,0])
assert m.A == 0

m = Machine(B=29)
m.run_program([1, 7])
assert m.B == 26

m = Machine(B=2024, C=43690)
m.run_program([4, 0])
assert m.B == 44354

m = Machine(A=729)
ret = m.run_program([0, 1, 5, 4, 3, 0])

# m = Machine(A=30553366)
# ret = m.run_program([2,4,1,1,7,5,4,7,1,4,0,3,5,5,3,0])


print('Answer 1:', ','.join([str(r) for r in ret]))

def program_function(A: int) -> int:
    t = (A % 8) ^ 1
    c = int(A / 2 ** t)
    return (t ^ c ^ 4) % 8

def program_iterator(A: int) -> Iterable[int]:
    yield program_function(A)
    A = int(A / 8)
    while A > 0:
        yield program_function(A)
        A = int(A / 8)


def program_iterator_rems(rems: List[int]) -> Iterable[int]:
    a = 0
    for i in range(len(rems)-1, -1, -1):
        a = 8*a + rems[i]
    for p in program_iterator(a):
        yield p


program = [0, 3, 5, 4, 3, 0]
program = [2,4,1,1,7,5,4,7,1,4,0,3,5,5,3,0]
output = []


# FAILED attempt to iterate
#
# max_matches = 0
# start_range = 8**15
# for a in trange(start_range, 8 ** 16):
#     matches = 0
#     for i, out in enumerate(program_iterator(a)):
#         if out != program[i]:
#             break
#         matches += 1
#         if matches > max_matches:
#             max_matches = matches
#             print(dt.datetime.now(), '- New max:', max_matches, 'for A:', a-start_range)


# FINAL (hopefully good) attempt
#
# for an output of size X, a must be at least 8^X
# In every machine cycle, the remainder of A divided by 8 is used to calculate the output (in combination with the quotient)
# while the quotient is the A for the next cycle

# We'll create a map of the outputs for each remainder of A (0 to 7), and the construct
# the starting A from end to start, by multiplying by 8 the previous A and adding the appropriate remainder

# The program
# bst A  --->  B = A % 8
# bxl 1  --->  B = B ^ 1
# cdv B  --->  C = A // 2^B
# bxc    --->  B = B ^ C
# bxl 4  --->  B = B ^ 4
# adv 3  --->  A = A // 8
# out B  --->  print(B % 8)
# jnz    --->  if A > 0: restart


# for remainder 0, the output is always 5
# for remainder 1, the output is always 5
# for remainder 2, the output is always 7
# for remainder 3, the output is always 6
# for remainder 4, the output is always 1
# for remainder 5, the output depends on the next level, if no next level then 0
# for remainder 6, the output depends on the second next level, if no second next level then 3
# for remainder 7, the output depends on the second next level, if no second next level then 2

# All outputs depend at most no the next two levels. We will calculate all
# for all possible 4 levels of A (8**4), and map the first remainder to the first output
remainder_outputs = dict()
for a in range(8**4):
    outputs = list(program_iterator(a))
    key = a % 8
    out = outputs[0]
    cur_outputs = remainder_outputs.get(a % 8, None)
    if cur_outputs is None:
        remainder_outputs[key] = [out]
    elif out not in cur_outputs:
        cur_outputs.append(out)

# Reverting to output remainders
output_remainders = dict()
for rem, outputs in remainder_outputs.items():
    for out in outputs:
        cur_rems = output_remainders.get(out, None)
        if cur_rems is None:
            output_remainders[out] = [rem]
        elif rem not in cur_rems:
            cur_rems.append(rem)


program_idx_to_q = list()
for i, out in enumerate(program):
    program_idx_to_q.append(output_remainders[out].copy())

# the only way to get 0 at the last position, with no next levels, is to have 5 remainder last.
program_idx_to_q[-1] = [5]
# the only way to get 3 at the second last position, is with 6 (no second next level). Tried 5 (with next level) and yields 2
program_idx_to_q[-2] = [6]
# with last 2 fixed, for position -3, 0 or 1 only works
program_idx_to_q[-3] = [0, 1]

#list(program_iterator(8*(8*5 + 6) + 0))

def get_all_possible_rems_from_idx(idx: int) -> Iterable[List[int]]:
    if idx == len(program):
        yield list()
        return
    for rems in get_all_possible_rems_from_idx(idx+1):
        for rem in program_idx_to_q[idx]:
            full_match = True
            try_rems = [rem] + rems
            for i, out in enumerate(program_iterator_rems(try_rems)):
                if out != program[idx+i]:
                    full_match = False
                    break
            if full_match:
                yield try_rems


min_a = 8**16
for rems in get_all_possible_rems_from_idx(0):
    a = 0
    for i in range(len(rems)-1, -1, -1):
        a = 8*a + rems[i]
    assert list(program_iterator(a)) == program, 'Not matching?!?'
    print('Got Rems!', rems, 'A:', a)
    if a < min_a:
        min_a = a
        print('New min!')

# total = math.prod([len(program_idx_to_q[i]) for i in range(len(program))])


# max_matches = 0
# for ci, comb in tqdm(enumerate(product(*[program_idx_to_q[i] for i in range(len(program))])), total=total):
#     a = 0
#     for i in range(len(comb)-1, -1, -1):
#         a = 8*a + comb[i]

#     matches = 0
#     for i, out in enumerate(program_iterator(a)):
#         if out != program[i]:
#             break
#         matches += 1

#     # matches = 0
#     # outputs = list(program_iterator(a))
#     # for i in range(len(outputs)-1, -1, -1):
#     #     if outputs[i] != program[i]:
#     #         break
#     #     matches += 1


#     if matches > max_matches:
#         max_matches = matches
#         print(dt.datetime.now(), '- New max:', max_matches, 'iteration:', ci, 'comb:', comb)

print('Answer 2:', min_a)
