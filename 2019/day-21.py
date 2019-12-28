# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 08:08:09 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List
import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2019")

from intcode_runner import IntcodeRunner


with open("inputs/day21.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]


if not 'answer_1' in locals():

    program = [
            "NOT A T",
            "NOT B J",
            "OR T J",
            "NOT C T",
            "OR T J",
            "AND D J",
            "WALK"
            ]

    prog_inp = []
    for command in program:
        for ch in command:
            prog_inp.append(ord(ch))
        prog_inp.append(10)

    runner = IntcodeRunner(inp, inputs=prog_inp, extend=1000)
    row = ''
    for b in runner.iter_run():
        if b == 10:
            if row != '':
                print(row)
                row = ''
            continue

        if b > 255:
            break
        row += chr(b)

    answer_1 = b

print('answer_1', answer_1)

program = [
        "OR A T",   # T = A
        "AND B T",  # T = A AND B
        "AND C T",  # T = A AND B AND C
        "NOT T T",  # T = NOT (A AND B AND C)
        "AND D T",  # T = NOT (A AND B AND C) AND D

        "OR H J",   # J = H
        "OR E J",   # J = H OR E
        "AND T J",  # J = NOT (A AND B AND C) AND D AND (H OR E)
        "RUN"
        ]

prog_inp = []
for command in program:
    for ch in command:
        prog_inp.append(ord(ch))
    prog_inp.append(10)

runner = IntcodeRunner(inp, inputs=prog_inp, extend=1000)
row = ''
for b in runner.iter_run():
    if b == 10:
        if row != '':
            print(row)
            row = ''
        continue

    if b > 255:
        break
    row += chr(b)

answer_2 = b
print('answer_2', answer_2)
