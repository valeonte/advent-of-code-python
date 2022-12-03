# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 3.

Created on Sat Dec  3 10:02:44 2022

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

with open("inputs/day-3.txt", "r") as f:
    inp_string = f.read()


def letter_to_priority(letter):
    """Get the priority of a letter."""
    if letter.islower():
        return ord(letter) - 96
    return ord(letter) - 38


total_priority = 0
inp = inp_string.split("\n")
for row in inp:
    h = len(row)//2
    common = set(row[:h]).intersection(row[h:]).pop()

    total_priority += letter_to_priority(common)

print('Answer 1:', total_priority)


total_priority = 0
for i in range(0, len(inp), 3):
    common = None
    for j in range(i, i + 3):
        if common is None:
            common = set(inp[j])
        else:
            common = common.intersection(inp[j])

    total_priority += letter_to_priority(common.pop())

print('Answer 2:', total_priority)
