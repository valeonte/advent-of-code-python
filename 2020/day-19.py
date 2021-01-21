# -*- coding: utf-8 -*-
"""
Day 19 Advent of Code 2020 file.

Created on Thu Dec 31 20:51:29 2020

@author: Eftychios
"""

import os

from typing import Dict, List, Tuple
from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

inp_string = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

with open("inputs/day-19.txt", "r") as f:
    inp_string = f.read()


@dataclass
class Rule:
    """Holds a rule."""

    rule_num: int
    letter: str = None
    ruleset1: List[int] = None
    ruleset2: List[int] = None

    def is_valid(self, message: str, rulebook: Dict[int, object]
                 ) -> Tuple[bool, str]:
        """Check whether rule applies. If so return remaining message."""
        if self.letter is not None:
            valid = message.startswith(self.letter)
            remaining = message[1:]

            return (valid, remaining)

        remaining = message
        for rule_num in self.ruleset1:
            rule = rulebook[rule_num]
            valid, remaining = rule.is_valid(remaining, rulebook)

            if not valid:
                break

        if valid:
            return (valid, remaining)

        if self.ruleset2 is not None:
            remaining = message
            for rule_num in self.ruleset2:
                rule = rulebook[rule_num]
                valid, remaining = rule.is_valid(remaining, rulebook)

                if not valid:
                    break

        return (valid, remaining)


    def get_valid_messages(self, prefix: str, rulebook: Dict[int, object],
                           ruleset: List[int] = None) -> str:
        """Return all valid messages following on from prefix."""
        if self.letter is not None:
            yield prefix + self.letter
            return

        if ruleset is None:
            for m in self.get_valid_messages(prefix, rulebook,
                                             self.ruleset1):
                yield m
            if self.ruleset2 is not None:
                for m in self.get_valid_messages(prefix, rulebook,
                                                 self.ruleset2):
                    yield m
            return

        if len(ruleset) == 0:
            yield prefix
            return

        rule = rulebook[ruleset[0]]
        # get all messages of the first rule
        for m in rule.get_valid_messages(prefix, rulebook):
            # and run the rest of the rules in set
            for mm in self.get_valid_messages(m, rulebook, ruleset[1:]):
                yield mm


test_messages = []
rulebook = dict()
for row in inp_string.split("\n"):
    if ':' in row:
        sp = row.split(': ')
        rule_num = int(sp[0])
        if '"' in sp[1]:
            letter = sp[1][1]
            rule = Rule(rule_num, letter=letter)
        else:
            rs = sp[1].split(' | ')
            ruleset1 = [int(s) for s in rs[0].split(' ')]
            if len(rs) > 1:
                ruleset2 = [int(s) for s in rs[1].split(' ')]
                rule = Rule(rule_num, ruleset1=ruleset1, ruleset2=ruleset2)
            else:
                rule = Rule(rule_num, ruleset1=ruleset1)

        rulebook[rule_num] = rule
    elif len(row) > 0:
        test_messages.append(row)

cnt = 0
for message in test_messages:
    valid, remaining = rulebook[0].is_valid(message, rulebook)
    if valid and len(remaining) == 0:
        cnt += 1
        print(message)

print('Answer 1:', cnt)

rulebook[8] = Rule(8, ruleset1=[42], ruleset2=[42, 8])
rulebook[11] = Rule(11, ruleset1=[42, 31], ruleset2=[42, 11, 31])

rule_31_parts = list(rulebook[31].get_valid_messages('', rulebook))
rule_42_parts = list(rulebook[42].get_valid_messages('', rulebook))

step = len(rule_31_parts[0])

cnt = 0
for message in test_messages:
    print('Message:', message)
    # Count instances of 31 from the end
    cnt31 = 0
    replaced = True
    while replaced:
        replaced = False
        for part31 in rule_31_parts:
            while message.endswith(part31):
                message = message[:-step]
                cnt31 += 1
                replaced = True
    if cnt31 == 0:
        continue

    print('Got', cnt31, 'part 31s at the end, remaining:', message)

    # All the remaining should be part 42s
    cnt42 = 0
    for idx in range(0, len(message), step):
        part = message[idx: idx + step]
        if part not in rule_42_parts:
            print('Failed part', part)
            cnt42 = 0
            break
        cnt42 += 1

    if cnt42 > cnt31:
        print(message, 'SUCCESS!')
        cnt += 1

print('Answer 2:', cnt)
