# -*- coding: utf-8 -*-
"""
Day 13 Advent of Code 2020 file.

Created on Wed Dec 16 12:05:10 2020

@author: Eftychios
"""

import os

from math import gcd


def compute_lcm(a):
    """Compute the least common multiplier of the provided numbers."""
    lcm = a[0]
    for i in a[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """939
7,13,x,x,59,x,31,19"""

with open("inputs/day-13.txt", "r") as f:
    inp_string = f.read()

spl = inp_string.split("\n")

etime = int(spl[0])
bus_ids = [int(x)
           for x in spl[1].replace('x', '-1').split(",")]

min_bus = -1
min_wait = etime

for bid in bus_ids:
    if bid == -1:
        continue

    bus_wait = (bid - etime % bid) % bid
    if bus_wait < min_wait:
        min_bus = bid
        min_wait = bus_wait

print('Answer 1:', min_bus * min_wait)

timestamp = 0
matched_buses = [bus_ids[0]]
while True:
    timestamp += compute_lcm(matched_buses)
    for i, bus in enumerate(bus_ids):
        if bus != -1:
            if (timestamp + i) % bus == 0:
                if bus not in matched_buses:
                    matched_buses.append(bus)
    if len(matched_buses) == len(bus_ids) - bus_ids.count(-1):
        break

print('Answer 2:', timestamp)
