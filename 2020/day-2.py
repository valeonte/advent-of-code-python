# -*- coding: utf-8 -*-
"""
Day 2 Advent of Code 2020 file.

Created on Tue Dec  8 22:33:46 2020

@author: valeo
"""

import os
import re

from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

with open("inputs/day-2.txt", "r") as f:
    inp_string = f.read()


@dataclass
class Policy:
    """Policy class."""

    count_min: int
    count_max: int
    character: str

    def test_policy_1(self, input_string: str) -> bool:
        """Test input_string according to policy 1."""
        cnt = 0
        for c in input_string:
            if c == self.character:
                cnt += 1
                if cnt > self.count_max:
                    return False

        return cnt >= self.count_min

    def test_policy_2(self, input_string: str) -> bool:
        """Test input_string according to policy 2."""
        return ((self.character == input_string[self.count_min - 1]) !=
                (self.character == input_string[self.count_max - 1]))


inp = []

inp = inp_string.split("\n")

regex = re.compile(r'^(?P<count_min>\d+)-(?P<count_max>\d+) '
                   r'(?P<character>\w): (?P<password>\w+)$')

passed_1 = 0
passed_2 = 0
for line in inp:
    match = regex.match(line)
    policy = Policy(int(match.group('count_min')),
                    int(match.group('count_max')),
                    match.group('character'))

    if policy.test_policy_1(match.group('password')):
        passed_1 += 1

    if policy.test_policy_2(match.group('password')):
        passed_2 += 1

print('Answer 1:', passed_1)
print('Answer 2:', passed_2)
