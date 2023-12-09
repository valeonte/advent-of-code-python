"""
Advent of Code 2023 day 5.

Created on Tue Dec 05 2023

@author: Eftychios
"""

import os

from typing import List
from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


with open("inputs/day-5.txt", "r") as f:
    inp_string = f.read()


@dataclass
class Rule:
    destination_start: int
    source_start: int
    range: int

    def map_number(self, source_number: int):
        """Map a number if captured by rule."""
        idx = source_number - self.source_start
        if idx < 0 or idx >= self.range:
            return -1
        return self.destination_start + idx
    

class Mapper:
    def __init__(self, name: str):
        self.name = name
        self.rules: List[Rule] = []

    def map_number(self, source_number: int):
        """Map a number using the mapper."""
        for rule in self.rules:
            ret = rule.map_number(source_number)
            if ret > -1:
                return ret
        return source_number

    def __repr__(self):
        return f'{self.name} mapper with {len(self.rules)} rules'


inp = inp_string.split("\n")

seeds: List[int] = None
mappers: List[Mapper] = []
cur_mapper: Mapper = None
for line in inp:
    if len(line.strip()) == 0:
        cur_mapper = None
        continue
    if line.startswith('seeds:'):
        seeds = [int(num) for num in line[7:].split(' ')]
        continue
    if line[0].isnumeric():
        # Add rule to existing mapper
        params = [int(num) for num in line.split(' ')]
        cur_mapper.rules.append(Rule(*params))
    else:
        mapper_name = line.split(' ')[0]
        print('Creating Mapper', mapper_name)
        cur_mapper = Mapper(mapper_name)
        mappers.append(cur_mapper)

min_location = 1000000000
for seed in seeds:
    location = seed
    for mapper in mappers:
        location = mapper.map_number(location)

    if location < min_location:
        print('Got new min location', location)
        min_location = location

print('Answer 1:', min_location)


@dataclass
class SmartRule:
    start: int
    add: int

    is_new: bool = True

dmapper: List[SmartRule] = [SmartRule(0, 0, False)]
for mapper in mappers:
    for dm in dmapper:
        dm.is_new = False
    for rule in mapper.rules:
        i = 0
        while i < len(dmapper):
            cur_dm = dmapper[i]
            if cur_dm.is_new:
                i += 1
                continue

            dest_start = cur_dm.start + cur_dm.add
            dest_end = 1_000_000_000_000
            if i < len(dmapper) - 1:
                dest_end = dmapper[i + 1].start - 1 + cur_dm.add

            rule_start = rule.source_start
            rule_end = rule.source_start + rule.range - 1
            if rule_start > dest_end or rule_end < dest_start:
                i += 1
                continue
            rule_add = rule.destination_start - rule.source_start

            # Here, there is overlap
            if rule_start <= dest_start and rule_end >= dest_end:
                # Full rule replace
                dmapper.pop(i)
                dmapper.insert(i, SmartRule(cur_dm.start, cur_dm.add + rule_add))
            elif rule_start > dest_start and rule_end >= dest_end:
                # Starts later, ends with cur rule
                dmapper.insert(i + 1, SmartRule(rule_start - cur_dm.add, cur_dm.add + rule_add))
                i += 1
            elif rule_start <= dest_start and rule_end < dest_end:
                # Starts from start, but ends early
                dmapper.pop(i)
                dmapper.insert(i, SmartRule(cur_dm.start, cur_dm.add + rule_add))
                dmapper.insert(i + 1, SmartRule(rule_end - cur_dm.add + 1, cur_dm.add, is_new=False))
                i += 1
            elif rule_start > dest_start and rule_end < dest_end:
                # Starts late and ends early
                dmapper.insert(i + 1, SmartRule(rule_start - cur_dm.add, cur_dm.add + rule_add))
                dmapper.insert(i + 2, SmartRule(rule_end - cur_dm.add + 1, cur_dm.add, is_new=False))
                i += 2

            i += 1

print('Got', len(dmapper), 'rules')

i = 0
min_location = 1_000_000_000_000
while i + 1 < len(seeds):
    cur_seed = seeds[i]
    max_seed = cur_seed + seeds[i + 1] - 1

    for j, dm in enumerate(dmapper):
        if max_seed < dm.start:
            break
        if j < len(dmapper) - 1 and cur_seed >= dmapper[j + 1].start:
            continue
        
        # Rule is applicable
        min_seed = max(cur_seed, dm.start)
        location = min_seed + dm.add
        if location < min_location:
            print('Got new min location', location)
            min_location = location
    
    i += 2

print('Answer 2:', min_location)
