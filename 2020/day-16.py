# -*- coding: utf-8 -*-
"""
Day 16 Advent of Code 2020 file.

Created on Wed Dec 16 12:05:10 2020

@author: Eftychios
"""

import os
import re

from dataclasses import dataclass


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


with open("inputs/day-16.txt", "r") as f:
    inp_string = f.read()


@dataclass
class Rule:
    """Rule definition."""

    from1: int
    to1: int
    from2: int
    to2: int

    def is_valid(self, num: int) -> bool:
        """Check number validity for rule."""
        return (num >= self.from1 and num <= self.to1
                or num >= self.from2 and num <= self.to2)


rule_pat = re.compile(r'^(?P<word>[\s\w]+)\: (?P<from1>\d+)-(?P<to1>\d+) '
                      r'or (?P<from2>\d+)-(?P<to2>\d+)$')

rules = dict()
rows = inp_string.split("\n")
for i, row in enumerate(rows):
    m = rule_pat.match(row)
    if m is None:
        break

    rules[m.group("word")] = Rule(int(m.group("from1")),
                                  int(m.group("to1")),
                                  int(m.group("from2")),
                                  int(m.group("to2")))

your_ticket = [int(n) for n in rows[i + 2].split(',')]

nearby_tickets = []
for i in range(i + 5, len(rows)):
    nearby_tickets.append([int(n) for n in rows[i].split(',')])

error_rate = 0
bad_tickets = set()
for idx, ticket in enumerate(nearby_tickets):
    for num in ticket:
        found_valid = False
        for rule in rules.values():
            if rule.is_valid(num):
                found_valid = True
                break
        if not found_valid:
            error_rate += num
            bad_tickets.add(idx)

print('Answer 1:', error_rate)


bad_tickets = list(bad_tickets)
bad_tickets.sort(reverse=True)

for b in bad_tickets:
    nearby_tickets.pop(b)

potential = [list(rules.keys()) for _ in range(len(your_ticket))]

for ticket in nearby_tickets:
    for idx, num in enumerate(ticket):
        for field, rule in rules.items():
            if not rule.is_valid(num) and field in potential[idx]:
                potential[idx].remove(field)

change_made = True
while change_made:
    change_made = False
    singles = [pot[0]
               for pot in potential
               if len(pot) == 1]
    for pot in potential:
        if len(pot) == 1:
            continue
        for sing in singles:
            if sing in pot:
                pot.remove(sing)
                change_made = True

fields = [pot[0] for pot in potential]
answer_2 = 1
for idx, field in enumerate(fields):
    if field.startswith('departure'):
        answer_2 *= your_ticket[idx]

print('Answer 2:', answer_2)
