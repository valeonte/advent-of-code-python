# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:33:46 2020

@author: valeo
"""

import os
from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

# with open("inputs/day-2.txt", "r") as f:
#     inp_string = f.read()


@dataclass
class Policy:
    count_min: int
    count_max: int
    character: str

    def test_string(self, input_string) -> bool:
        cnt = 0
        for c in input_string:
            if c == self.character:
                cnt += 1
                if cnt > self.count_max:
                    return False

        return cnt >= self.count_min


inp = []

inp = [int(s)
       for s in inp_string.split("\n")]

for i in range(0, len(inp)):
    for j in range(i + 1, len(inp)):
        for k in range(j + 1, len(inp)):
            x = inp[i]
            y = inp[j]
            z = inp[k]

            if x + y + z == 2020:
                break
        if x + y + z == 2020:
            break

    if x + y + z == 2020:
        print('Got solution')
        break

answer = x * y * z
print(answer)
