"""
Advent of Code 2023 day 1.

Created on Fri Dec 01 2023

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

inp_string = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

with open("inputs/day-1.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")

total = 0
for line in inp:
    first_digit = None
    last_digit = None
    for ch in line:
        o = ord(ch) - 48
        if o < 0 or o > 9:
            continue
        if first_digit is None:
            first_digit = o
        else:
            last_digit = o
    if first_digit is None:
        continue
    
    total += 10 * first_digit + (last_digit or first_digit)

print('Answer 1:', total)

nums = dict(one=1,
            two=2,
            three=3,
            four=4,
            five=5,
            six=6,
            seven=7,
            eight=8,
            nine=9)

total = 0
for line in inp:
    first_digit = None
    last_digit = None
    for i, ch in enumerate(line):
        o = ord(ch) - 48
        digit = None
        if o >= 0 and o <= 9:
            digit = o
        else:
            for sp, val in nums.items():
                if i < len(sp)-1:
                    continue
                if line[i-len(sp)+1:i+1] == sp:
                    digit = val
                    break

        if digit is None:
            continue
        if first_digit is None:
            first_digit = digit
        else:
            last_digit = digit
            
    
    total += 10 * first_digit + (last_digit or first_digit)

print('Answer 2:', total)
