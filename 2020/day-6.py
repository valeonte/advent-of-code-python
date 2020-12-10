# -*- coding: utf-8 -*-
"""
Day 6 Advent of Code 2020 file.

Created on Thu Dec 10 22:06:39 2020

@author: Eftychios
"""

import os
import string

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """abc

a
b
c

ab
ac

a
a
a
a

b"""

with open("inputs/day-6.txt", "r") as f:
    inp_string = f.read()


questions = set()
count_sum = 0

for r in inp_string.split("\n"):
    if len(r) == 0:
        count_sum += len(questions)
        questions = set()
    else:
        for ch in r:
            questions.add(ch)

count_sum += len(questions)


print('Answer 1:', count_sum)


questions = set(string.ascii_lowercase)
count_sum = 0

for r in inp_string.split("\n"):
    if len(r) == 0:
        count_sum += len(questions)
        questions = set(string.ascii_lowercase)
    else:
        resp = [ch for ch in r]
        questions = questions.intersection(resp)

count_sum += len(questions)

print('Answer 2:', count_sum)
