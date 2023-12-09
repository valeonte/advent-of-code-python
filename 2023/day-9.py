"""
Advent of Code 2023 day 8.

Created on Sat Dec 09 2023

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


with open("inputs/day-9.txt", "r") as f:
    inp_string = f.read()

inp = inp_string.split('\n')
ret = 0

for no, line in enumerate(inp):
    series = [int(num) for num in line.split(' ')]
    all_series = [series]
    while any([s != 0 for s in series]):
        series = [series[i] - series[i - 1] for i in range(1, len(series))]
        all_series.append(series)

    inc = 0
    for series in reversed(all_series):
        series.append(series[-1] + inc)
        inc = series[-1]
    print(no + 1, 'New number', inc)
    ret += inc

print('Answer 1:', ret)


ret = 0

for no, line in enumerate(inp):
    series = [int(num) for num in line.split(' ')]
    all_series = [series]
    while any([s != 0 for s in series]):
        series = [series[i] - series[i - 1] for i in range(1, len(series))]
        all_series.append(series)

    inc = 0
    for series in reversed(all_series):
        series.insert(0, series[0] - inc)
        inc = series[0]
    print(no + 1, 'New number', inc)
    ret += inc

print('Answer 2:', ret)
