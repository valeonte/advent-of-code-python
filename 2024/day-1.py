"""
Advent of Code 2024 day 1.

Created on Sun Dec 01 2024 9:46:57 AM

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """3   4
4   3
2   5
1   3
3   9
3   3"""

with open("inputs/day-1.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")

list1 = []
list2 = []
imax = 0
for line in inp:
    nums = line.split()
    list1.append(int(nums[0]))
    list2.append(int(nums[1]))
    imax += 1

total = 0
sl1 = sorted(list1)
sl2 = sorted(list2)
for num1, num2 in zip(sl1, sl2):
    total += abs(num1 - num2)


print('Answer 1:', total)


num_appearances = dict()
total = 0
i1 = 0
i2 = 0
for left in sl1:
    if left in num_appearances:
        total += left * num_appearances[left]
        # counted already
        continue

    left_appearances = 0
    while i2 < imax and sl2[i2] <= left:
        if sl2[i2] == left:
            left_appearances += 1
        i2 += 1
    
    num_appearances[left] = left_appearances
    total += left * left_appearances

print('Answer 2:', total)
