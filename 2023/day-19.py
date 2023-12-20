"""
Advent of Code 2023 day 19.

Created on Wed Dec 20 2023 9:54:22 PM

@author: Eftychios
"""

import os
import json
import re

import numpy as np

from typing import Tuple, Set, Iterator, Dict
from dataclasses import dataclass, replace
from enum import Enum

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

with open("inputs/day-19.txt", "r") as f:
    inp_string = f.read()


@dataclass(init=False)
class Part:
    x: int
    m: int
    a: int
    s: int

    def __init__(self, part: str):
        cats = part[1:-1].split(',')
        self.x = int(cats[0][2:])
        self.m = int(cats[1][2:])
        self.a = int(cats[2][2:])
        self.s = int(cats[3][2:])
    
    def eval_rule(self, rule: str) -> bool:
        """Evaluate a simple rule, like a>123."""
        return eval('self.' + rule)
    
    def sum(self) -> int:
        return self.x + self.m + self.a + self.s


def process_rules(part: Part, rules: str) -> str:
    """Process the given rules for part."""
    for rule in rules.split(','):
        rr = rule.split(':')
        if len(rr) == 1:
            return rr[0]
        if part.eval_rule(rr[0]):
            return rr[1]
    
    raise Exception('eee')



inps = inp_string.split('\n')

pat = re.compile(r'^(?P<name>\w+)\{(?P<rules>.+)\}$')

workflows = dict()
parsing_workflows = True
A = 0
for inp in inps:
    if len(inp) == 0:
        parsing_workflows = False
        continue
    if parsing_workflows:
        m = pat.match(inp)
        workflows[m.group('name')] = m.group('rules')
        continue

    # Loading part
    part = Part(inp)
    res = process_rules(part, workflows['in'])
    while res not in ['A', 'R']:
        res = process_rules(part, workflows[res])
    
    if res == 'A':
        A += part.sum()



print('Answer 1:', A)

@dataclass(frozen=True)
class PartRanges:
    """Stores the potential values for each rating."""
    x: Tuple[int, int]
    m: Tuple[int, int]
    a: Tuple[int, int]
    s: Tuple[int, int]

    def get_rule_split(self, rule: str) -> Tuple['PartRanges', 'PartRanges']:
        """Evaluate a rule, and split to satisfiers and un-satisfiers."""
        rating_from, rating_to = getattr(self, rule[0])
        rule_val = int(rule[2:])

        if rule[1] == '<':
            if rating_from >= rule_val:
                # all un-satisfiers
                return None, self
            if rating_to < rule_val:
                # all satisfiers
                return self, None
            sat_changes = {rule[0]: (rating_from, rule_val - 1)}
            unsat_changes = {rule[0]: (rule_val, rating_to)}

            return replace(self, **sat_changes), replace(self, **unsat_changes)

        if rule[1] == '>':
            if rating_to <= rule_val:
                # all un-satisfiers
                return None, self
            if rating_from > rule_val:
                # all satisfiers
                return self, None
            sat_changes = {rule[0]: (rule_val + 1, rating_to)}
            unsat_changes = {rule[0]: (rating_from, rule_val)}

            return replace(self, **sat_changes), replace(self, **unsat_changes)
        
        raise Exception('eee')
    
    def get_combinations(self):
        return (self.x[1] - self.x[0] + 1) * (self.m[1] - self.m[0] + 1) * (self.a[1] - self.a[0] + 1) * (self.s[1] - self.s[0] + 1)


queue = [(PartRanges((1, 4000), (1, 4000), (1, 4000), (1, 4000)), 'in')]

A = 0
while queue:
    pr, wf = queue.pop(0)
    if wf == 'A':
        A += pr.get_combinations()
        continue
    if wf == 'R':
        continue
    rules = workflows[wf]

    for rule in rules.split(','):
        rr = rule.split(':')
        if len(rr) == 1:
            queue.append((pr, rr[0]))
            continue
        sat_pr, unsat_pr = pr.get_rule_split(rr[0])
        if sat_pr is not None:
            queue.append((sat_pr, rr[1]))
        if unsat_pr is not None:
            pr = unsat_pr
        else:
            break

print('Answer 2:', A)
