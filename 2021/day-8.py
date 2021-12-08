# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 8.

Created on Wed Dec  8 07:48:30 2021

@author: Eftychios
"""

import os

from dataclasses import dataclass
from typing import List


@dataclass
class Entry:
    """Keep the data from one row."""

    patterns: List[int]
    output: List[int]


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""  # noqa

with open("inputs/day-8.txt", "r") as f:
    inp_string = f.read()

bit_map = {'a': 1,
           'b': 2,
           'c': 4,
           'd': 8,
           'e': 16,
           'f': 32,
           'g': 64}

entries = []
for row in inp_string.split('\n'):
    parts = row.split(' | ')
    pats = []
    for p in parts[0].split(' '):
        num = 0
        for k, v in bit_map.items():
            if k in p:
                num = num + v
        pats.append(num)

    out = []
    for p in parts[1].split(' '):
        num = 0
        for k, v in bit_map.items():
            if k in p:
                num = num + v
        out.append(num)

    entries.append(Entry(pats, out))


known_bits = [2, 3, 4, 7]
known_appearances = 0
for entry in entries:

    known_appearances = known_appearances + \
        sum([bin(e).count('1') in known_bits for e in entry.output])

print('Answer 1:', known_appearances)


nums = []
for entry in entries:
    mapp = dict()
    for p in entry.patterns:
        bits_set = bin(p).count('1')
        digit = -1
        if bits_set == 2:
            digit = 1
        elif bits_set == 3:
            digit = 7
        elif bits_set == 4:
            digit = 4
        elif bits_set == 7:
            digit = 8
        else:
            continue

        mapp[digit] = p

    # Looking at 5-bits. 2, 3 and 5
    for p in entry.patterns:
        bits_set = bin(p).count('1')
        if bits_set != 5:
            continue

        # The one containing the bits of 1, will be 3
        if p & mapp[1] == mapp[1]:
            mapp[3] = p
            continue
        # The one having 3 common with 4 will be 5, and the other 2
        res = p & mapp[4]
        common = bin(res).count('1')
        if common == 3:
            mapp[5] = p
        else:
            mapp[2] = p

    # Looking at 6-bits. 0, 9 and 6
    for p in entry.patterns:
        bits_set = bin(p).count('1')
        if bits_set != 6:
            continue

        # the one not containing all of 5 will be 0
        if p & mapp[5] != mapp[5]:
            mapp[0] = p
            continue
        # Of the other 2, the one containing 4 will be 9, and the other 6
        if p & mapp[4] == mapp[4]:
            mapp[9] = p
        else:
            mapp[6] = p

    mapp = {v: k for k, v in mapp.items()}

    num = mapp[entry.output[0]] * 1000 + \
        mapp[entry.output[1]] * 100 + \
        mapp[entry.output[2]] * 10 + \
        mapp[entry.output[3]]

    nums.append(num)

print('Answer 2:', sum(nums))
