# -*- coding: utf-8 -*-
"""
Day 14 Advent of Code 2020 file.

Created on Wed Dec 16 12:05:10 2020

@author: Eftychios
"""

import os
import re

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

inp_string = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

with open("inputs/day-14.txt", "r") as f:
    inp_string = f.read()


class BitmaskSystem:
    """The bitmask system status."""

    def __init__(self):
        self.mem = dict()

        self.mask = 'X' * 36
        self.mask_and = 2**36-1
        self.mask_plus = 0

    def store_number(self, address: int, value: int):
        """Store a number respecting the mask."""
        value &= self.mask_and

        self.mem[address] = value + self.mask_plus

    def store_number_v2(self, address: int, value: int):
        """Store the number using v2 decoder."""
        address |= self.mask_plus

        x_locs = [m.span()[0] for m in re.finditer('X', self.mask)]
        combs = 2 ** len(x_locs)
        for i in range(0, combs):
            a = list(bin(address)[2:].zfill(36))
            comb = bin(i)[2:].zfill(len(x_locs))
            for j, x in enumerate(x_locs):
                a[x] = comb[j]

            a = int(''.join(a), 2)
            self.mem[a] = value

    def set_mask(self, mask: str):
        """Update the mask."""
        self.mask = mask

        self.mask_and = int(mask.replace('1', '0').replace('X', '1'), 2)
        self.mask_plus = int(mask.replace('X', '0'), 2)


mask_pattern = re.compile(r'^mask = (?P<mask>[X\d]+)$')
value_pattern = re.compile(r'^mem\[(?P<address>\d+)\] = (?P<value>\d+)$')

bm = BitmaskSystem()
for row in inp_string.split("\n"):
    match = mask_pattern.match(row)
    if match is None:
        match = value_pattern.match(row)
        bm.store_number(int(match.group('address')),
                        int(match.group('value')))
    else:
        bm.set_mask(match.group('mask'))

print('Answer 1:', sum(bm.mem.values()))


bm = BitmaskSystem()
for row in inp_string.split("\n"):
    match = mask_pattern.match(row)
    if match is None:
        match = value_pattern.match(row)
        bm.store_number_v2(int(match.group('address')),
                        int(match.group('value')))
    else:
        bm.set_mask(match.group('mask'))

print('Answer 2:', sum(bm.mem.values()))
