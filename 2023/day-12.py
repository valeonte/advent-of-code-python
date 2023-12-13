"""
Advent of Code 2023 day 12.

Created on Tue Dec 12 2023

@author: Eftychios
"""

import os

from itertools import combinations
from typing import Tuple
from functools import cache

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

with open("inputs/day-12.txt", "r") as f:
    inp_string = f.read()

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



@cache
def get_arrangements_of(springs: str, config: Tuple[int]) -> int:
    """Return arrangements of set of springs for config."""
    if len(springs) < sum(config) + len(config) - 1:
        return 0
    cur_group = config[0]

    if springs[0] == '.':
        return get_arrangements_of(springs[1:], config)
    
    can_fit = True
    for i in range(cur_group):
        if springs[i] == '.':
            can_fit = False
            break
    # check if following our group is a hash
    can_fit = can_fit and not (len(springs) > cur_group and springs[cur_group] == '#')
    if not can_fit:
        if springs[0] == '#':
            return 0
        return get_arrangements_of(springs[1:], config)

    # group can fit and not hash is following
    if len(config) == 1:
        if '#' in springs[cur_group:]:
            # if there are more hashes, this is not a solution
            if springs[0] == '#':
                # if current start is hash, no solutions thereafter
                return 0
            # else, keep looking
            return get_arrangements_of(springs[1:], config)

        if springs[0] == '#':
            return 1
        return 1 + get_arrangements_of(springs[1:], config)

    rest_springs = springs[cur_group + 1:] # we skip one that should be the dot
    rest = get_arrangements_of(rest_springs, config[1:])

    if springs[0] == '#':  # if start is hash, we cannot omit in our config
        return rest
    return rest + get_arrangements_of(springs[1:], config)



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
    #print(springs, ',', len(unknowns), 'unknowns and', remaining, 'remaining')

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
    ret = get_arrangements_of(springs, config)
    print(springs, config, ':', ret, 'arrangements')

    if ret != arrangements:
        print('Gotcha!')
    #print(arrangements, 'arrangements')
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

    ret = get_arrangements_of(springs, config)
    print(springs, config, ':', ret, 'arrangements')
    total_arrangements += ret


print('Answer 2:', total_arrangements)
