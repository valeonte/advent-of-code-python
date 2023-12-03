"""
Advent of Code 2023 day 3.

Created on Sun Dec 03 2023

@author: Eftychios
"""

import os

from typing import List
from collections import namedtuple

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


with open("inputs/day-3.txt", "r") as f:
    inp_string = f.read()


Num = namedtuple('Num', ['no', 'coords'])

inp = inp_string.split("\n")

def extract_line_numbers(line: str) -> List[Num]:
    """Return a dict of all numbers mapped to their coords."""
    ret = []
    num = ''
    cur_set = set()
    for i, ch in enumerate(line):
        if ch.isnumeric():
            num += ch
            cur_set.add(i - 1)
            cur_set.add(i)
            cur_set.add(i + 1)
            continue
        if len(num) > 0:
            ret.append(Num(int(num), cur_set))
            cur_set = set()
            num = ''

    if len(num) > 0:
        ret.append(Num(int(num), cur_set))

    return ret


numbers = [extract_line_numbers(line)
           for line in inp]

all_sum = sum([num.no 
               for row_nums in numbers
               for num in row_nums])

def get_neighbours_from_symbol_and_line(x: int, row_num: int):
    if row_num < 0:
        return 0
    ret = []
    z = 0
    nums = numbers[row_num]
    while z < len(nums):
        num = nums[z]
        if x in num.coords:
            ret.append(num)
            nums.pop(z)
        else:
            z += 1

    return ret


total = 0
for y, line in enumerate(inp):
    for x, ch in enumerate(line):
        if ch.isnumeric() or ch == '.':
            continue
        print('Got symbol', ch, 'on line', y)
        total += sum([num.no for num in get_neighbours_from_symbol_and_line(x, y - 1)])
        total += sum([num.no for num in get_neighbours_from_symbol_and_line(x, y)])
        total += sum([num.no for num in get_neighbours_from_symbol_and_line(x, y + 1)])

remaining_sum = sum([num.no 
                     for row_nums in numbers
                     for num in row_nums])

print('Answer 1:', total)
print('Total:', total, 'Remaining:', remaining_sum, 'All:', all_sum)

for y, line in enumerate(inp):
    print_line = ''
    for x, ch in enumerate(line):
        if not ch.isnumeric():
            print_line += ch
        else:
            found = False
            for num in numbers[y]:
                if x in num.coords:
                    found = True
                    print_line += ch
                    break
            if not found:
                print_line += '-'
    # print(print_line)

numbers = [extract_line_numbers(line)
           for line in inp]

total = 0
for y, line in enumerate(inp):
    for x, ch in enumerate(line):
        if ch != '*':
            continue
        print('Got symbol', ch, 'on line', y)
        neighbours = get_neighbours_from_symbol_and_line(x, y - 1)
        neighbours += get_neighbours_from_symbol_and_line(x, y)
        neighbours += get_neighbours_from_symbol_and_line(x, y + 1)

        if len(neighbours) == 2:
            # got gear
            total += neighbours[0].no * neighbours[1].no

print('Answer 2:', total)
