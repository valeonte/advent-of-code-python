# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 15:45:11 2020

@author: Eftychios
"""

import os
import time
import math

from typing import Dict, List, Tuple
from dataclasses import dataclass


os.chdir("C:/Repos/advent-of-code-python/2017")

with open("inputs/day24.txt", "r") as f:
    inp = f.read()


def build_parts_dict(comps: List[str]) -> Dict[int, List[Tuple[int, int]]]:

    ret = dict()

    for c in comps:
        cp = c.split('/')
        comp = (int(cp[0]), int(cp[1]))
        if comp[0] not in ret:
            ret[comp[0]] = []
        if comp[1] not in ret:
            ret[comp[1]] = []

        ret[comp[0]].append(comp)
        if comp[0] != comp[1]:
            ret[comp[1]].append(comp)

    return ret


def print_dict(d):
    for k in sorted(d.keys()):
        print(f'{k}:', d[k])


def build_best_path(pins: int,
                    comps: List[Tuple[int, int]],
                    d: Dict[int, List[Tuple[int, int]]],
                    best_so_far: int):
    best = best_so_far
    best_path = list(comps)
    new_comps = list(comps)
    available_comps = d[pins]
    for comp in available_comps:
        if comp in comps:
            continue  # already used

        new_pins = comp[0] if comp[1] == pins else comp[1]
        comp_str = comp[0] + comp[1]

        new_comps.append(comp)
        bridge_str, bridge_path = build_best_path(
            new_pins, new_comps, d, best_so_far + comp_str)
        new_comps.pop()

        if bridge_str > best:
            best = bridge_str
            best_path = bridge_path

    return best, best_path


def build_longest_path(pins: int,
                       comps: List[Tuple[int, int]],
                       d: Dict[int, List[Tuple[int, int]]],
                       best_so_far: int,
                       longest_so_far: int):
    best = best_so_far
    longest = longest_so_far
    best_path = list(comps)
    new_comps = list(comps)
    available_comps = d[pins]
    for comp in available_comps:
        if comp in comps:
            continue  # already used

        new_pins = comp[0] if comp[1] == pins else comp[1]
        comp_str = comp[0] + comp[1]

        new_comps.append(comp)
        bridge_str, bridge_path = build_longest_path(
            new_pins, new_comps, d, best_so_far + comp_str,
            longest_so_far + 1)
        new_comps.pop()

        if len(bridge_path) < longest:
            continue

        if len(bridge_path) > longest or bridge_str > best:
            best = bridge_str
            best_path = bridge_path
            longest = len(bridge_path)

    return best, best_path


inpa = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

d = build_parts_dict(inp.split("\n"))
#print_dict(d)
#best, best_path = build_best_path(0, [], d, 0)
longest, longest_path = build_longest_path(0, [], d, 0, 0)
