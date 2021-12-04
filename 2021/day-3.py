# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 3.

Created on Sat Dec  4 17:36:45 2021

@author: Eftychios
"""

import os

import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

with open("inputs/day-3.txt", "r") as f:
    inp_string = f.read()

inp = np.array([[int(s) for s in list(ss)]
                for ss in inp_string.split("\n")])

gamma = 0
epsilon = 0
half = len(inp) / 2
for onesum in np.sum(inp, axis=0):
    gamma = 2 * gamma
    epsilon = 2 * epsilon
    if onesum > half:
        gamma = gamma + 1
    elif onesum < half:
        epsilon = epsilon + 1
    else:
        raise Exception("Shouldn't happen!")

print('Gamma', gamma, 'Epsilon', epsilon, 'Answer 1', gamma * epsilon)


oxy = inp
co2 = inp
oxy_found = False
co2_found = False
for i in range(len(inp[0])):
    if not oxy_found:
        if sum(oxy[:, i]) >= len(oxy)/2:
            # most common is 1, keep it for oxy
            oxy = oxy[oxy[:, i] == 1, :]
        else:
            # most common is 0, keep it for oxy
            oxy = oxy[oxy[:, i] == 0, :]

        oxy_found = len(oxy) == 1

    if not co2_found:
        if sum(co2[:, i]) < len(co2)/2:
            # least common is 1, keep it for oxy
            co2 = co2[co2[:, i] == 1, :]
        else:
            # least common is 0, keep it for oxy
            co2 = co2[co2[:, i] == 0, :]

        co2_found = len(co2) == 1

    if oxy_found and co2_found:
        break

oxy = list(oxy[0])
co2 = list(co2[0])

oxy_num = 0
co2_num = 0
for i in range(len(oxy)):
    oxy_num = 2 * oxy_num + oxy[i]
    co2_num = 2 * co2_num + co2[i]

print('Oxy', oxy_num, 'CO2', co2, 'Answer 2', oxy_num * co2_num)
