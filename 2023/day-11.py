"""
Advent of Code 2023 day 11.

Created on Mon Dec 11 2023

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


with open("inputs/day-11.txt", "r") as f:
    inp_string = f.read()

inp = inp_string.split('\n')

galaxies = []
for i, line in enumerate(inp):
    for j, ch in enumerate(line):
        if ch == '#':
            galaxies.append((i, j))

all_is = {i for i, _ in galaxies}
all_js = {j for _, j in galaxies}

empty_rows = []
for i in range(min(all_is), max(all_is) + 1):
    if i not in all_is:
        empty_rows.append(i)
empty_cols = []
for j in range(min(all_js), max(all_js) + 1):
    if j not in all_js:
        empty_cols.append(j)

for k in range(len(galaxies)):
    g = galaxies[k]
    inc_i = 0
    for er in empty_rows:
        if g[0] > er:
            inc_i += 1
    inc_j = 0
    for ec in empty_cols:
        if g[1] > ec:
            inc_j += 1
    
    galaxies[k] = (g[0] + inc_i, g[1] + inc_j)

total_dist = 0
pairs = 0
for k in range(len(galaxies)):
    for l in range(k + 1, len(galaxies)):
        dist = abs(galaxies[k][0] - galaxies[l][0]) + abs(galaxies[k][1] - galaxies[l][1])
        total_dist += dist
        pairs += 1

print('Total dist', total_dist, 'with', pairs, 'pairs')

print('Answer 1:', total_dist)

galaxies = []
for i, line in enumerate(inp):
    for j, ch in enumerate(line):
        if ch == '#':
            galaxies.append((i, j))

increment = 1000000-1
for k in range(len(galaxies)):
    g = galaxies[k]
    inc_i = 0
    for er in empty_rows:
        if g[0] > er:
            inc_i += increment
    inc_j = 0
    for ec in empty_cols:
        if g[1] > ec:
            inc_j += increment
    
    galaxies[k] = (g[0] + inc_i, g[1] + inc_j)

total_dist = 0
pairs = 0
for k in range(len(galaxies)):
    for l in range(k + 1, len(galaxies)):
        dist = abs(galaxies[k][0] - galaxies[l][0]) + abs(galaxies[k][1] - galaxies[l][1])
        total_dist += dist
        pairs += 1

print('Total dist', total_dist, 'with', pairs, 'pairs')

print('Answer 2:', total_dist)
