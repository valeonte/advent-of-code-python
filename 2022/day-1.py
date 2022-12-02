# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 1.

Created on Fri Dec  2 18:43:47 2022

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

with open("inputs/day-1.txt", "r") as f:
    inp_string = f.read()


elf_sum = 0
max_elf_sum = 0
for row in inp_string.split("\n"):
    if row.isnumeric():
        elf_sum += int(row)
        continue

    if elf_sum > max_elf_sum:
        max_elf_sum = elf_sum
    elf_sum = 0

print('Answer 1:', max_elf_sum)


top_elf_sums = [0, 0, 0]
elf_sum = 0
for row in inp_string.split("\n"):
    if row.isnumeric():
        elf_sum += int(row)
        continue

    for i in range(len(top_elf_sums)):
        if top_elf_sums[i] < elf_sum:
            print(top_elf_sums, elf_sum)
            for j in range(len(top_elf_sums) - 1, i, -1):
                top_elf_sums[j] = top_elf_sums[j - 1]
            top_elf_sums[i] = elf_sum
            print(top_elf_sums)
            break

    elf_sum = 0

for i in range(len(top_elf_sums)):
    if top_elf_sums[i] < elf_sum:
        print(top_elf_sums, elf_sum)
        for j in range(len(top_elf_sums) - 1, i, -1):
            top_elf_sums[j] = top_elf_sums[j - 1]
        top_elf_sums[i] = elf_sum
        print(top_elf_sums)
        break

print(top_elf_sums)
print('Answer 2:', sum(top_elf_sums))
