"""
Advent of Code 2023 day 12.

Created on Mon Dec 12 2023

@author: Eftychios
"""

import os

from itertools import combinations


os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1"""

inp_string = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

# with open("inputs/day-12.txt", "r") as f:
#     inp_string = f.read()

inp = inp_string.split('\n')


def get_springs_config(springs: str):
    """Calculate the springs configuration."""
    cur_block = 0
    ret = []
    for ch in springs:
        if ch == '#':
            cur_block += 1
        elif ch == '.':
            if cur_block > 0:
                ret.append(cur_block)
                cur_block = 0
        else:
            raise Exception(f'Unexpected char {ch}!')

    if cur_block > 0:
        ret.append(cur_block)
        cur_block = 0

    return tuple(ret)


total_arrangements = 0
for line in inp:
    parts = line.split(' ')
    springs = parts[0]
    config = tuple([int(num) for num in parts[1].split(',')])

    unknowns = []
    damaged = 0
    for i, ch in enumerate(springs):
        if ch == '?':
            unknowns.append(i)
        elif ch == '#':
            damaged += 1

    remaining = sum(config) - damaged
    print(springs, ',', len(unknowns), 'unknowns and', remaining, 'remaining')

    arrangements = 0
    for comb in combinations(unknowns, remaining):
        resprings = ''
        for i, ch in enumerate(springs):
            if ch == '?':
                if i in comb:
                    new_ch = '#'
                else:
                    new_ch = '.'
            else:
                new_ch = ch
            resprings += new_ch
        
        if get_springs_config(resprings) == config:
            arrangements += 1

    print(arrangements, 'arrangements')
    total_arrangements += arrangements

print('Answer 1:', total_arrangements)


total_arrangements = 0
for line in inp:
    parts = line.split(' ')
    springs = parts[0]
    config = tuple([int(num) for num in parts[1].split(',')])

    # unfold
    springs = ((springs + '?') * 5)[:-1]
    config = config * 5

    unknowns = []
    damaged = 0
    for i, ch in enumerate(springs):
        if ch == '?':
            unknowns.append(i)
        elif ch == '#':
            damaged += 1

    remaining = sum(config) - damaged
    print(springs, ',', len(unknowns), 'unknowns and', remaining, 'remaining')

    arrangements = 0
    for comb in combinations(unknowns, remaining):
        resprings = ''
        for i, ch in enumerate(springs):
            if ch == '?':
                if i in comb:
                    new_ch = '#'
                else:
                    new_ch = '.'
            else:
                new_ch = ch
            resprings += new_ch
        
        if get_springs_config(resprings) == config:
            arrangements += 1

    print(arrangements, 'arrangements')
    total_arrangements += arrangements

print('Answer 2:', total_arrangements)
