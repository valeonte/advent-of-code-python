# -*- coding: utf-8 -*-
"""
Day 4 Advent of Code 2020 file.

Created on Thu Dec 10 21:13:03 2020

@author: Eftychios
"""

import os
import re

import numpy as np

from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

with open("inputs/day-4.txt", "r") as f:
    inp_string = f.read()


@dataclass
class Passport:
    """TreesArea class."""

    def __init__(self):
        self.missing = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    def process_line(self, line: str):
        """Process a line from the passport data."""
        for m in re.finditer(r'((?P<key>\w+):(?P<value>\S+))', line):
            key = m.group('key')
            if key in self.missing:
                self.missing.remove(key)

    def process_line_strict(self, line: str) -> bool:
        """Process a line from the passport data using strict rules."""
        for m in re.finditer(r'((?P<key>\w+):(?P<value>\S+))', line):
            key = m.group('key')
            if key not in self.missing:
                continue

            value = m.group('value')
            if key == 'byr':
                match = re.match(r'^(\d{4})$', value)
                if match is None:
                    return False
                year = int(match.group(1))
                if year < 1920 or year > 2002:
                    return False
            elif key == 'iyr':
                match = re.match(r'^(\d{4})$', value)
                if match is None:
                    return False
                year = int(match.group(1))
                if year < 2010 or year > 2020:
                    return False
            elif key == 'eyr':
                match = re.match(r'^(\d{4})$', value)
                if match is None:
                    return False
                year = int(match.group(1))
                if year < 2020 or year > 2030:
                    return False
            elif key == 'hgt':
                match = re.match(r'^(\d+)(cm|in)$', value)
                if match is None:
                    return False
                hgt = int(match.group(1))
                unit = match.group(2)
                if (unit == 'cm' and (hgt < 150 or hgt > 193)
                        or unit == 'in' and (hgt < 59 or hgt > 76)):
                    return False
            elif key == 'hcl':
                match = re.match(r'^#[0-9a-f]{6}$', value)
                if match is None:
                    return False
            elif key == 'ecl':
                match = re.match(r'^(amb|blu|brn|gry|grn|hzl|oth)$', value)
                if match is None:
                    return False
            elif key == 'pid':
                match = re.match(r'^\d{9}$', value)
                if match is None:
                    return False

            self.missing.remove(key)

    def is_valid(self) -> bool:
        """Check validity of passport."""
        return len(self.missing) == 0


cur_pass = Passport()
valid = 0

for line in inp_string.split("\n"):
    if len(line) == 0:
        if cur_pass.is_valid():
            valid += 1
        cur_pass = Passport()
    else:
        cur_pass.process_line(line)

print('Answer 1:', valid)

cur_pass = Passport()
valid = 0

for line in inp_string.split("\n"):
    if len(line) == 0:
        if cur_pass.is_valid():
            valid += 1
        cur_pass = Passport()
    else:
        cur_pass.process_line_strict(line)

print('Answer 2:', valid)
