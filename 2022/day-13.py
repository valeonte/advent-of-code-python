# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 13.

Created on Tue Dec 13 12:22:04 2022

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

with open("inputs/day-13.txt", "r") as f:
    inp_string = f.read()

def try_next(it):
    try:
        return next(it)
    except StopIteration:
        return None


def is_in_right_order(left, right) -> bool:
    """Test whether pair is in the right order."""
    if type(left) is int and type(right) is int:
        if left < right:
            return True
        if left > right:
            return False
        return None
    if type(left) is list and type(right) is list:
        ileft = iter(left)
        iright = iter(right)
        while True:
            l = try_next(ileft)
            r = try_next(iright)
            if l is None and r is None:
                return None
            if l is None:
                return True
            if r is None:
                return False

            res = is_in_right_order(l, r)
            if res is None:
                continue

            return res

    if type(left) is int:
        return is_in_right_order([left], right)
    if type(right) is int:
        return is_in_right_order(left, [right])

    raise Exception('Impossible 3')


rows = []
left = None
right = None
pair_idx = 0
right_order = []

for i, row in enumerate(inp_string.split('\n')):
    if len(row) == 0:
        if left is None or right is None:
            raise Exception('Impossible 1')
        pair_idx += 1
        res = is_in_right_order(left, right)
        if res is not None and res:
            right_order.append(pair_idx)
        left = None
        right = None
        continue
    if left is None:
        left = eval(row)
        continue
    if right is None:
        right = eval(row)
        continue

    raise Exception('Impossible 2')

print('Answer 1:', sum(right_order))


packets = []
for row in inp_string.split('\n'):
    if len(row) > 0:
        packets.append(eval(row))

packets.append([[2]])
packets.append([[6]])

changes_made = True
i = 1
loops = 0
while i > 1 or changes_made:
    if i == 1:
        loops += 1
        changes_made = False
    res = is_in_right_order(packets[i - 1], packets[i])
    if res is None:
        raise Exception('?')
    if not res:
        tmp = packets[i - 1]
        packets[i - 1] = packets[i]
        packets[i] = tmp
        changes_made = True

    if i < len(packets) - 1:
        i += 1
    else:
        i = 1

res = 1
for i, p in enumerate(packets):
    if p == [[2]] or p == [[6]]:
        res *= i + 1

print('Answer 2:', res)
