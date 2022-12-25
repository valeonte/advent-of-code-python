# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 20.

Created on Sun Dec 25 10:18:42 2022

@author: Eftychios
"""

import os
import math

import datetime as dt

from typing import Iterator
from dataclasses import dataclass, replace

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

with open("inputs/day-21.txt", "r") as f:
    inp_string = f.read()


monkeys = dict()
cnt = 0
while 'root' not in monkeys:
    cnt += 1
    # print('Iteration', cnt, 'with', len(monkeys), 'known')
    for row in inp_string.split('\n'):
        monkey, operation = row.split(': ')
        if operation.isnumeric():
            monkeys[monkey] = int(operation)
            continue

        left = operation[:4]
        if left not in monkeys:
            continue
        right = operation[7:]
        if right not in monkeys:
            continue

        left = monkeys[left]
        right = monkeys[right]
        op = operation[5]
        if op == '+':
            monkeys[monkey] = left + right
        elif op == '-':
            monkeys[monkey] = left - right
        elif op == '*':
            monkeys[monkey] = left * right
        elif op == '/':
            monkeys[monkey] = left // right


print('Answer 1:', monkeys['root'])


def calculate_root(humn: int) -> tuple[int, int]:
    """Calculate the two parts of root."""
    monkeys = dict(humn=humn)
    while True:
        for row in inp_string.split('\n'):
            monkey, operation = row.split(': ')
            if monkey in monkeys:
                continue
            if operation.isnumeric():
                monkeys[monkey] = int(operation)
                continue

            left = operation[:4]
            if left not in monkeys:
                continue
            right = operation[7:]
            if right not in monkeys:
                continue

            left = monkeys[left]
            right = monkeys[right]

            if monkey == 'root':
                return left, right

            op = operation[5]
            if op == '+':
                monkeys[monkey] = left + right
            elif op == '-':
                monkeys[monkey] = left - right
            elif op == '*':
                monkeys[monkey] = left * right
            elif op == '/':
                monkeys[monkey] = left / right


left, right = calculate_root(3360561285172)
print(left, right, right - left)
