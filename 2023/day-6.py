"""
Advent of Code 2023 day 6.

Created on Thu Dec 07 2023

@author: Eftychios
"""

import os
import math

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """Time:      7  15   30
Distance:  9  40  200"""


with open("inputs/day-6.txt", "r") as f:
    inp_string = f.read()

# If we hold for u ms, and release for r ms, then if time available is T => T = u + r
# Speed would be u m/sec
# Distance travelled would be d = u * r = u * (T - u) = u*T - u^2

# We will solve for the provided distance and time, and the integers in-between
# the two solutions would be all the possible ways to beat the record

# We need to solve:  u^2 - T*u + d = 0
# Discriminant would be D = T^2 - 4 * d
# Solutions would be s1 = (T - sqrt(T^2 - 4*d)) / 2 and s2 = (T + sqrt(T^2 - 4*d)) / 2

inp = inp_string.split('\n')
times = [int(num.strip()) for num in inp[0][6:].split(' ') if len(num) > 0]
distances = [int(num.strip()) for num in inp[1][10:].split(' ') if len(num) > 0]

ret = 1
for T, d in zip(times, distances):
    s1 = (T - math.sqrt(T**2 - 4*d))/2 + 0.000001
    s2 = (T + math.sqrt(T**2 - 4*d))/2 - 0.000001

    solutions = int(math.floor(s2)) - int(math.ceil(s1)) + 1
    print(T, d, solutions)
    ret *= solutions

print('Answer 1:', ret)

T = int(''.join([num.strip() for num in inp[0][6:].split(' ') if len(num) > 0]))
d = int(''.join([num.strip() for num in inp[1][10:].split(' ') if len(num) > 0]))

s1 = (T - math.sqrt(T**2 - 4*d))/2 + 0.000001
s2 = (T + math.sqrt(T**2 - 4*d))/2 - 0.000001

solutions = int(math.floor(s2)) - int(math.ceil(s1)) + 1
print('Answer 2:', solutions)
