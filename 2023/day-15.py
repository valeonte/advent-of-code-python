"""
Advent of Code 2023 day 15.

Created on Fri Dec 15 2023

@author: Eftychios
"""

import os
import re

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

with open("inputs/day-15.txt", "r") as f:
    inp_string = f.read()


def hash_add(current_value: int, ch: str) -> int:
    """Add a character to an existing hash."""
    return (current_value + ord(ch)) * 17 % 256


def hash_string(hashable: str) -> int:
    """Get the hash value of a string"""
    current_value = 0
    for ch in hashable:
        current_value = hash_add(current_value, ch)
    return current_value


ret = 0
current_value = 0
for ch in inp_string:
    if ch == ',':
        ret += current_value
        current_value = 0
        continue
    current_value = hash_add(current_value, ch)

ret += current_value

print('Answer 1:', ret)

pat = re.compile(r'^(\w+)((\=(\d+))|\-)$')

boxes = dict()
for s in inp_string.split(','):
    m = pat.match(s)

    lens = m.group(1)
    box_id = hash_string(lens)
    if m.group(2) == '-':
        print(s,'- Removing', lens, 'from box', box_id)
        if box_id not in boxes:
            continue
        box = boxes[box_id]
        for i in range(len(box)):
            if box[i][0] == lens:
                box.pop(i)
                break
        continue

    length = int(m.group(4))
    print(s,'- Adding lens', lens, 'with length', length, 'in box', box_id)
    if box_id not in boxes:
        boxes[box_id] = []

    fl = (lens, length)
    box = boxes[box_id]
    added = False
    for i in range(len(box)):
        if box[i][0] == lens:
            box[i] = fl
            added = True
            break
    if not added:
        box.append(fl)

power = 0
for box_id, box in boxes.items():
    for i, (_, length) in enumerate(box):
        power += (box_id + 1) * (i + 1) * length


print('Answer 2', power)
