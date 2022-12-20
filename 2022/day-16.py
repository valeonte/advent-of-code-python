# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 16.

Created on Fri Dec 16 16:17:18 2022

@author: Eftychios
"""

import os
import re

import numpy as np
import pandas as pd

from typing import List, Set
from random import shuffle


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


with open("inputs/day-16.txt", "r") as f:
    inp_string = f.read()


pat = re.compile(r'^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$')

class Valve:
    def __init__(self, name: str, rate: int, conn: List[str]):
        self.name = name
        self.rate = rate
        self.conn = conn
        self.conn_valve = []

    def __repr__(self):
        return f'{self.name} / {self.rate} / {self.conn}'


valves = dict()
for row in inp_string.split('\n'):
    m = pat.match(row)
    name = m.group(1)
    rate = int(m.group(2))
    conn = m.group(3).split(', ')

    valves[name] = Valve(name, rate, conn)

for name, valve in valves.items():
    for v in valve.conn:
        valve.conn_valve.append(valves[v])


def get_cost_between(v1: Valve, v2: Valve,
                     visited: Set[str] = None,
                     max_cost: int = 10000000) -> int:
    """Get cost between valves."""
    if v1.name == v2.name:
        return 0
    if max_cost < 1:
        return 10  # something to make it large enough to be ignored

    if visited is None:
        visited = {v1.name}
    else:
        visited.add(v1.name)

    min_cost = 100000000
    for cv in v1.conn_valve:
        if cv.name == v2.name:
            return 1
        if max_cost < 2:
            continue
        if cv.name in visited:
            continue

        cost = 1 + get_cost_between(cv, v2, visited.copy(),
                                    min_cost - 2)
        if cost < min_cost:
            min_cost = cost

    return min_cost


print('Calculating costs')
vs = sorted(valves.keys())

costs = np.zeros((len(vs), len(vs)))
for i in range(len(vs)):
    for j in range(i + 1, len(vs)):
        v1 = valves[vs[i]]
        v2 = valves[vs[j]]
        costs[i, j] = get_cost_between(v1, v2)

costs = costs + costs.T

dcosts = pd.DataFrame(costs, columns=vs, index=vs)

non_zero = [valve
            for valve in valves.values()
            if valve.rate > 0]
non_zero.sort(key=lambda x: -x.rate)


def get_best_from(cur_valve: Valve,
                  minutes_remaining: int,
                  visited: List[str] = None):
    if visited is None:
        visited = {cur_valve.name}
    else:
        visited.add(cur_valve.name)

    best_gain = 0
    for cv in non_zero:
        if cv.name in visited:
            continue

        cost = dcosts.loc[cur_valve.name, cv.name]

        new_minutes_remaining = minutes_remaining - cost - 1
        if new_minutes_remaining < 0:
            continue

        gain = new_minutes_remaining * cv.rate

        if new_minutes_remaining > 2:
            gain += get_best_from(cv, new_minutes_remaining, visited.copy())

        if gain > best_gain:
            best_gain = gain

    return best_gain


print('Calculating best')
ret = get_best_from(valves['AA'], minutes_remaining=30)

print('Answer 1:', ret)

global loop_cnt
loop_cnt = 0


def get_max_gain_from_remaining(minutes_remaining, visited: Set[Valve]):
    ret = 0
    for nz in non_zero:
        if nz.name in visited:
            continue
        ret += nz.rate * (minutes_remaining - 1)
    return ret


def get_best_from2(cur_valve1: Valve,
                   dist_to_valve1: int,
                   cur_valve2: Valve,
                   dist_to_valve2: int,
                   minutes_remaining: int,
                   visited: Set[str],
                   cur_best: int = 0):
    global loop_cnt

    if dist_to_valve1 > 0:
        cv1s_costs = [(cur_valve1, dist_to_valve1)]
    else:
        cv1s_costs = []
        for cv1 in non_zero:
            if cv1.name == cur_valve2.name or cv1.name in visited:
                continue
            cost_cv1 = dcosts.loc[cur_valve1.name, cv1.name] + 1

            if minutes_remaining - cost_cv1 > 0:
                cv1s_costs.append((cv1, cost_cv1))

    best_gain = 0
    cnt = 0
    idx1 = 0

    for cv1, cost_cv1 in cv1s_costs:
        idx1 += 1

        if dist_to_valve2 > 0:
            cv2s_costs = [(cur_valve2, dist_to_valve2)]
        else:
            cv2s_costs = []
            for cv2 in non_zero:
                if (cv2.name == cur_valve1.name
                        or cv2.name == cv1.name
                        or cv2.name in visited):
                    continue
                cost_cv2 = dcosts.loc[cur_valve2.name, cv2.name] + 1

                if minutes_remaining - cost_cv2 > 0:
                    cv2s_costs.append((cv2, cost_cv2))

        idx2 = 0
        for cv2, cost_cv2 in cv2s_costs:
            cnt += 1
            idx2 += 1
            # We will open the closest one
            vis = visited.copy()
            if cost_cv1 < cost_cv2:
                new_minutes_remaining = minutes_remaining - cost_cv1
                new_dist_to_valve1 = 0
                new_dist_to_valve2 = cost_cv2 - cost_cv1
                gain = new_minutes_remaining * cv1.rate
                vis.add(cv1.name)
            elif cost_cv1 > cost_cv2:
                new_minutes_remaining = minutes_remaining - cost_cv2
                new_dist_to_valve1 = cost_cv1 - cost_cv2
                new_dist_to_valve2 = 0
                gain = new_minutes_remaining * cv2.rate
                vis.add(cv2.name)
            else:
                new_minutes_remaining = minutes_remaining - cost_cv1
                new_dist_to_valve1 = 0
                new_dist_to_valve2 = 0
                gain = new_minutes_remaining * (cv1.rate + cv2.rate)
                vis.add(cv1.name)
                vis.add(cv2.name)

            if best_gain > 0:
                max_rem = get_max_gain_from_remaining(
                    new_minutes_remaining, vis)
            else:
                max_rem = 100000000000

            if max_rem > best_gain - gain:
                gain += get_best_from2(cv1, new_dist_to_valve1,
                                       cv2, new_dist_to_valve2,
                                       new_minutes_remaining, vis)
            # else:
            #     print('impo')

            if len(visited) == 1:
                print('top level, checking', gain, best_gain,
                      'idx1:', idx1, '/', len(cv1s_costs),
                      'idx2:', idx2, '/', len(cv2s_costs))

            if gain > best_gain:
                best_gain = gain

        # There may be a case where no cv1 are available. In this case, we
        # progress just cv1
        if len(cv2s_costs) == 0:
            vis = visited.copy()
            vis.add(cv1.name)
            cnt += 1
            # using the single function, the other agent cannot move
            new_minutes_remaining = minutes_remaining - cost_cv1

            gain = new_minutes_remaining * cv1.rate

            if new_minutes_remaining > 2:
                gain += get_best_from(cv1, new_minutes_remaining,
                                      visited.copy())

            if gain > best_gain:
                best_gain = gain

            if len(visited) == 1:
                print('top level, checking 2', gain, best_gain)

    loop_cnt += 1
    if len(visited) <= 2:
        print('Got best', best_gain, 'in', cnt, 'loops and total loops',
              loop_cnt, 'with visited', visited)
    return best_gain


print('Calculating best 2')
ret = get_best_from2(valves['AA'], 0, valves['AA'], 0, minutes_remaining=26,
                     visited={'AA'})

print('Answer 2:', ret)


