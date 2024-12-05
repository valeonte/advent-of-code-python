"""
Advent of Code 2024 day 5.

Created on Thu Dec 05 2024 6:23:11 PM

@author: Eftychios
"""

import os

from typing import Dict, List, Set


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


with open("inputs/day-5.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")


precedes: Dict[int, Set[int]] = dict()
updates = []


for row in inp:
    if '|' in row:
        first, second = tuple([int(r) for r in row.split('|')])
        if first not in precedes:
            precedes[first] = set()
        precedes[first].add(second)

    if ',' in row:
        updates.append([int(r) for r in row.split(',')])


# Almosts bubble sort
def is_valid_order(update: List[int]) -> bool:
    valid = True
    for i, u in enumerate(update[:-1]):
        if u not in precedes:
            continue

        uu = update[i+1]
        valid = valid and uu in precedes[u]

        if not valid:
            break

    return valid, i


incorrect_updates = []
ret = 0
for update in updates:
    valid, _ = is_valid_order(update)
    if valid:
        ret += update[len(update) // 2]
    else:
        incorrect_updates.append(update)


print('Answer 1:', ret)


ret = 0
for update in incorrect_updates:
    test_update = update.copy()
    while True:
        valid, i = is_valid_order(test_update)
        if valid:
            break

        # swapping problematic elements
        tmp = test_update[i]
        test_update[i] = test_update[i+1]
        test_update[i+1] = tmp

    ret += test_update[len(test_update) // 2]


print('Answer 2:', ret)