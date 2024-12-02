"""
Advent of Code 2024 day 2.

Created on Mon Dec 02 2024 5:52:51 PM

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

with open("inputs/day-2.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")


class Report:
    def __init__(self):
        self.levels = []
        self.is_safe = True
        self.direction = 0
    
    def add_level(self, level: int):
        self.levels.append(level)
        if not self.is_safe:
            # No point in further checking
            return

        if len(self.levels) == 1:
            return

        previous_level = self.levels[-2]
        diff = level - previous_level
        if diff == 0 or abs(diff) > 3:
            self.is_safe = False
            return
        direction = diff // abs(diff)
        if self.direction == 0:
            self.direction = direction
            return
        if self.direction != direction:
            self.is_safe = False
        


safe_count = 0
for report in inp:
    r = Report()
    for level in report.split():
        r.add_level(int(level))
        if not r.is_safe:
            break
    if r.is_safe:
        safe_count += 1

print('Answer 1:', safe_count)


safe_count = 0
for report in inp:
    levels = [int(l) for l in report.split()]
    for skip_idx in range(-1, len(levels)):
        r = Report()
        for i, level in enumerate(levels):
            if skip_idx == i:
                continue
            r.add_level(int(level))
            if not r.is_safe:
                break
        if r.is_safe:
            safe_count += 1
            break
    

print('Answer 2:', safe_count)
