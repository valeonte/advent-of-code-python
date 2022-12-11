# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 11.

Created on Sun Dec 11 17:21:44 2022

@author: Eftychios
"""

import os

import datetime as dt

from typing import List


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

with open("inputs/day-11.txt", "r") as f:
    inp_string = f.read()


class Monkey:
    def __init__(self, rows: List[str]):
        self.id = int(rows[0][7])
        self.items = [int(i) for i in rows[1][18:].split(', ')]
        self.op = eval('lambda old :' + rows[2][18:])
        self.test = int(rows[3].split(' by ')[1])
        self.res = {True: int(rows[4][-1]),
                    False: int(rows[5][-1])}
        self.inspections = 0

    def __repr__(self) -> str:
        s = f'Monkey {self.id}\n'
        s += f'Starting items: {", ".join([str(i) for i in self.items])}\n'
        s += f'Operation: 2 -> {self.op(2)}\n'
        s += f'Test divisible: {self.test}\n'
        s += f'Throw to: {self.res}\n'
        s += f'Inspections: {self.inspections}'

        return s

    def get_new_monkey(self, item: int):
        return self.res[item % self.test == 0]


monkey_string = []
monkeys = dict()

for row in inp_string.split('\n'):
    if len(row) == 0:
        monkey = Monkey(monkey_string)
        print('Added', monkey)
        monkeys[monkey.id] = monkey
        monkey_string = []

        continue

    monkey_string.append(row)

monkey = Monkey(monkey_string)
print('Added', monkey)
monkeys[monkey.id] = monkey

for _ in range(20):
    for idx in range(len(monkeys)):
        monkey = monkeys[idx]
        for item in monkey.items:
            monkey.inspections += 1
            new_item = monkey.op(item)
            new_item = new_item // 3
            new_monkey = monkeys[monkey.get_new_monkey(new_item)]
            new_monkey.items.append(new_item)
        monkey.items = []


insps = sorted([m.inspections for m in monkeys.values()])
print('Answer 1:', insps[-2] * insps[-1], '\n\n\n')


class Worry:
    def __init__(self, value, divisors):
        self.modulos = {d:value % d for d in divisors}

    def op(self, operator, val):
        if operator == '+':
            for d, mod in self.modulos.items():
                self.modulos[d] = (mod + val) % d
        elif operator == '*':
            if val is None:
                for d, mod in self.modulos.items():
                    self.modulos[d] = (mod * mod) % d
            else:
                for d, mod in self.modulos.items():
                    self.modulos[d] = (mod * (val % d)) % d
        else:
            raise Exception(f'Unexpected operator {operator}!')

    def __repr__(self):
        return str(self.modulos)


class Monkey2:
    def __init__(self, rows: List[str]):
        self.id = int(rows[0][7])
        self.items = [int(i) for i in rows[1][18:].split(', ')]
        self.test = int(rows[3].split(' by ')[1])
        self.res = {True: int(rows[4][-1]),
                    False: int(rows[5][-1])}
        self.inspections = 0

        op_row = rows[2][18:]
        self.operator = '*' if '*' in op_row else '+'
        self.multadd = op_row.split(' ')[-1]
        if self.multadd.isnumeric():
            self.multadd = int(self.multadd)
        else:
            self.multadd = None

    def op(self, w: Worry):
        w.op(self.operator, self.multadd)
        return w

    def __repr__(self) -> str:
        s = f'Monkey2 {self.id}\n'
        s += f'Starting items: {", ".join([str(i) for i in self.items])}\n'
        s += f'Test divisible: {self.test}\n'
        s += f'Throw to: {self.res}\n'
        s += f'Inspections: {self.inspections}'

        return s

    def get_new_monkey(self, item: Worry):
        return self.res[item.modulos[self.test] == 0]


monkey_string = []
monkeys = dict()

for row in inp_string.split('\n'):
    if len(row) == 0:
        monkey = Monkey2(monkey_string)
        print('Added', monkey)
        monkeys[monkey.id] = monkey
        monkey_string = []

        continue

    monkey_string.append(row)

monkey = Monkey2(monkey_string)
print('Added', monkey)
monkeys[monkey.id] = monkey

divisors = [m.test for m in monkeys.values()]
for m in monkeys.values():
    m.items = [Worry(i, divisors)
               for i in m.items]


for rnd in range(10000):
    for idx in range(len(monkeys)):
        monkey = monkeys[idx]
        for item in monkey.items:
            monkey.inspections += 1
            new_item = monkey.op(item)
            new_monkey = monkeys[monkey.get_new_monkey(new_item)]
            new_monkey.items.append(new_item)
        monkey.items = []

    # if (rnd + 1) % 1000 == 0:
    #     print(dt.datetime.now(), '== After round', rnd, '==')
    #     print(monkeys)
    #     for idx in range(len(monkeys)):
    #         print('Monkey', idx, 'inspected items',
    #               monkeys[idx].inspections, 'times.')
    #     pass


insps = sorted([m.inspections for m in monkeys.values()])
print('Answer 2:', insps[-2] * insps[-1])
