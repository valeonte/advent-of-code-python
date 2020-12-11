# -*- coding: utf-8 -*-
"""
Day 7 Advent of Code 2020 file.

Created on Fri Dec 11 09:45:44 2020

@author: Eftychios
"""

import os
import re
import math

from typing import Dict


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

with open("inputs/day-7.txt", "r") as f:
    inp_string = f.read()


rulebook = dict()

container_re = re.compile(r'^(?P<container>[\w\s]+) bags contain.+\.$')
contents_re = re.compile(r' (?P<count>\d+) (?P<content>[\w\s]+) bag')

for rule in inp_string.split("\n"):
    m = container_re.match(rule)

    container = m.group("container")
    rulebook[container] = dict()
    for m in contents_re.finditer(rule):
        rulebook[container][m.group("content")] = int(m.group("count"))


def count_colour_contents(container: str, colour: str) -> int:
    """Count all instances of colour contained in container."""
    d = rulebook[container]

    ret = 0
    for sub_colour, sub_count in d.items():

        if sub_colour == colour:
            ret += sub_count
            continue

        ret += sub_count * count_colour_contents(sub_colour, colour)

    return ret


answer_1 = 0
for container in rulebook.keys():
    if count_colour_contents(container, 'shiny gold') > 0:
        answer_1 += 1

print('Answer 1:', answer_1)


answer_2 = 0
for colour in rulebook.keys():
    if colour == 'shiny gold':
        continue
    answer_2 += count_colour_contents('shiny gold', colour)

print('Answer 2:', answer_2)
