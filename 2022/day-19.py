# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 19.

Created on Thu Dec 22 21:34:35 2022

@author: Eftychios
"""

import os
import re
import time

import datetime as dt

from typing import Iterator
from dataclasses import dataclass, replace

from concurrent.futures import ProcessPoolExecutor


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

with open("inputs/day-19.txt", "r") as f:
    inp_string = f.read()

pat = re.compile(r'^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$')


@dataclass
class Blueprint:
    no: int
    ore_robot_ore: int

    clay_robot_ore: int

    obs_robot_ore: int
    obs_robot_clay: int

    geo_robot_ore: int
    geo_robot_obs: int

    most: int = None
    spent: dt.timedelta = None

    def quality(self) -> int:
        return self.most * self.no

    def latest_geo_robot_minute_left(self) -> int:
        """Return the latest minute you need to have at least 1 obs robot."""
        if self.geo_robot_obs == 1:
            # for 1 obs robot, you need 1 obs robot with 2 left, so you
            # get 1 obs with 1 left, you construct geo, and have a geo on last
            return 2
        if self.geo_robot_obs <= 3:
            # for 3 (or less) you need one obs robot with 3 left,
            # 1 obs create another obs robot with 2 left
            # 3 obs with 1 left, you create geo robot, and get 1 geo at last
            return 3
        if self.geo_robot_obs <= 6:
            # similar to above
            return 4
        if self.geo_robot_obs <= 10:
            # similar to above
            return 5
        if self.geo_robot_obs <= 15:
            # similar to above
            return 6
        if self.geo_robot_obs <= 21:
            # similar to above
            return 7

        raise Exception('Impossible')


@dataclass
class State:
    ore: int = 0
    clay: int = 0
    obs: int = 0
    geo: int = 0

    ore_robots: int = 1
    clay_robots: int = 0
    obs_robots: int = 0
    geo_robots: int = 0

    def work_the_robots(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obs += self.obs_robots
        self.geo += self.geo_robots

    def can_afford_geo_robot(self, blueprint: Blueprint) -> bool:
        return (blueprint.geo_robot_ore <= self.ore
                and blueprint.geo_robot_obs <= self.obs)


bps = []
for row in inp_string.split('\n'):
    m = pat.match(row)

    bps.append(Blueprint(*[int(c) for c in m.groups()]))


def get_next_states(state: State, blueprint: Blueprint) -> Iterator[State]:
    """Iterate through all possible next states."""
    if state.can_afford_geo_robot(blueprint):
        s = replace(state)
        s.work_the_robots()
        s.ore -= blueprint.geo_robot_ore
        s.obs -= blueprint.geo_robot_obs
        s.geo_robots += 1
        yield s
        # if geode can be created, create it!
        return

    can_create = 0
    if (blueprint.obs_robot_ore <= state.ore
            and blueprint.obs_robot_clay <= state.clay):
        s = replace(state)
        s.work_the_robots()
        s.ore -= blueprint.obs_robot_ore
        s.clay -= blueprint.obs_robot_clay
        s.obs_robots += 1
        yield s

        can_create += 1
        # if the first obs robot can be created, create it
        if s.obs_robots == 1:
            return

    if (state.clay < 2 * blueprint.obs_robot_clay
            and blueprint.clay_robot_ore <= state.ore):
        s = replace(state)
        s.work_the_robots()
        s.ore -= blueprint.clay_robot_ore
        s.clay_robots += 1
        yield s
        can_create += 1

    if state.ore < 10 and blueprint.ore_robot_ore <= state.ore:
        s = replace(state)
        s.work_the_robots()
        s.ore -= blueprint.ore_robot_ore
        s.ore_robots += 1
        yield s
        can_create += 1

    # if no robots have been created, but clay and ore can be created, do it
    if (can_create > 0
            and blueprint.clay_robot_ore <= state.ore
            and blueprint.ore_robot_ore <= state.ore
            and state.ore_robots == 1
            and state.clay_robots == 0):
        return

    # Just work the robots
    s = replace(state)
    s.work_the_robots()
    yield s


def get_most_geo_for(state: State,
                     blueprint: Blueprint,
                     minutes_left: int,
                     minutes_spent: int,
                     cur_max: int = 0) -> int:
    """Get the most geodes that can be farmed from blueprint."""
    #print(minutes_spent, ':', state)
    if minutes_left == 1:
        return state.geo + state.geo_robots
    if minutes_left == 2:
        if state.can_afford_geo_robot(blueprint):
            return state.geo + 2 * state.geo_robots + 1
        return state.geo + 2 * state.geo_robots

    if (state.ore > blueprint.clay_robot_ore
            and state.clay_robots == 0
            and state.ore_robots >= 5):
        return 0
    if (state.ore > blueprint.obs_robot_ore
            and state.clay > blueprint.obs_robot_clay
            and state.clay_robots >= 5
            and state.ore_robots >= 5):
        return 0

    latest_minute = blueprint.latest_geo_robot_minute_left()
    if cur_max > 0:
        if cur_max <= 3:
            latest_minute -= 1
        elif cur_max <= 6:
            latest_minute -= 2
        elif cur_max <= 10:
            latest_minute -= 3

    if state.obs_robots == 0 and latest_minute > minutes_left:
        return 0


    max_geo = cur_max
    for next_state in get_next_states(state, blueprint):
        geo = get_most_geo_for(next_state, blueprint, minutes_left - 1,
                               minutes_spent + 1, max_geo)
        if geo > max_geo:
            max_geo = geo

    return max_geo


def run_blueprint(bp: Blueprint):
    print(dt.datetime.now(), '-- Starting Blueprint', bp.no)
    start = time.time()
    most = get_most_geo_for(State(), bp, 24, 0)
    spent = time.time() - start

    bp.most = most
    bp.spent = dt.timedelta(seconds=spent)

    print(dt.datetime.now(), '-- Blueprint', bp.no, 'most', most,
          'in', bp.spent)

    return bp


def run_blueprint2(bp: Blueprint):
    print(dt.datetime.now(), '-- Starting Blueprint', bp.no)
    start = time.time()
    most = get_most_geo_for(State(), bp, 32, 0)
    spent = time.time() - start

    bp.most = most
    bp.spent = dt.timedelta(seconds=spent)

    print(dt.datetime.now(), '-- Blueprint', bp.no, 'most', most,
          'in', bp.spent)

    return bp


if __name__ == "__main__":

    if False:
        with ProcessPoolExecutor(max_workers=4) as ex:
            bps_done = ex.map(run_blueprint, bps)

        ss = 0
        total_spent = dt.timedelta(0)

        print('Blueprints dump:')
        for bp in bps_done:
            total_spent += bp.spent
            ss += bp.quality()

            print(f'{bp.no}\t{bp.most}\t{bp.spent}')

        print('Answer 1:', ss, 'in', total_spent)




    if True:
        with ProcessPoolExecutor(max_workers=3) as ex:
            bps_done = ex.map(run_blueprint2, bps[:3])

        ss = 1
        total_spent = dt.timedelta(0)

        print('Blueprints dump:')
        for bp in bps_done:
            total_spent += bp.spent
            ss *= bp.most

            print(f'{bp.no}\t{bp.most}\t{bp.spent}')

        print('Answer 1:', ss, 'in', total_spent)


# PART 1

# (base) C:\Users\Eftychios>python C:\Repos\advent-of-code-python\2022\day-19.py
# 2022-12-24 21:25:12.585479 -- Starting Blueprint 1
# 2022-12-24 21:25:12.586479 -- Starting Blueprint 2
# 2022-12-24 21:25:12.588478 -- Starting Blueprint 3
# 2022-12-24 21:25:12.588478 -- Starting Blueprint 4
# 2022-12-24 21:25:16.235475 -- Blueprint 3 most 2 in 0:00:03.646997
# 2022-12-24 21:25:16.238476 -- Starting Blueprint 5
# 2022-12-24 21:25:23.901495 -- Blueprint 1 most 0 in 0:00:11.315016
# 2022-12-24 21:25:23.916498 -- Starting Blueprint 6
# 2022-12-24 21:25:50.558101 -- Blueprint 6 most 4 in 0:00:26.640603
# 2022-12-24 21:25:50.559099 -- Starting Blueprint 7
# 2022-12-24 21:26:01.109136 -- Blueprint 7 most 13 in 0:00:10.550037
# 2022-12-24 21:26:01.110138 -- Starting Blueprint 8
# 2022-12-24 21:26:05.720136 -- Blueprint 2 most 2 in 0:00:53.132659
# 2022-12-24 21:26:05.721137 -- Starting Blueprint 9
# 2022-12-24 21:26:06.428136 -- Blueprint 4 most 2 in 0:00:53.837659
# 2022-12-24 21:26:06.429138 -- Starting Blueprint 10
# 2022-12-24 21:26:11.517176 -- Blueprint 10 most 0 in 0:00:05.088039
# 2022-12-24 21:26:11.518176 -- Starting Blueprint 11
# 2022-12-24 21:26:18.280197 -- Blueprint 11 most 1 in 0:00:06.762021
# 2022-12-24 21:26:18.282200 -- Starting Blueprint 12
# 2022-12-24 21:26:29.654217 -- Blueprint 9 most 0 in 0:00:23.933080
# 2022-12-24 21:26:29.655217 -- Starting Blueprint 13
# 2022-12-24 21:26:38.137237 -- Blueprint 13 most 3 in 0:00:08.482020
# 2022-12-24 21:26:38.159238 -- Starting Blueprint 14
# 2022-12-24 21:26:44.705257 -- Blueprint 12 most 1 in 0:00:26.423057
# 2022-12-24 21:26:44.706257 -- Starting Blueprint 15
# 2022-12-24 21:26:45.221257 -- Blueprint 14 most 4 in 0:00:07.029019
# 2022-12-24 21:26:45.222259 -- Starting Blueprint 16
# 2022-12-24 21:26:47.706257 -- Blueprint 8 most 5 in 0:00:46.596119
# 2022-12-24 21:26:47.707257 -- Starting Blueprint 17
# 2022-12-24 21:26:52.370811 -- Blueprint 16 most 1 in 0:00:07.148552
# 2022-12-24 21:26:52.373813 -- Starting Blueprint 18
# 2022-12-24 21:26:58.902827 -- Blueprint 15 most 5 in 0:00:14.196570
# 2022-12-24 21:26:58.903827 -- Starting Blueprint 19
# 2022-12-24 21:27:09.634380 -- Blueprint 5 most 6 in 0:01:53.394905
# 2022-12-24 21:27:09.636380 -- Starting Blueprint 20
# 2022-12-24 21:27:13.988886 -- Blueprint 20 most 9 in 0:00:04.351509
# 2022-12-24 21:27:13.992888 -- Starting Blueprint 21
# 2022-12-24 21:27:16.167889 -- Blueprint 21 most 0 in 0:00:02.175000
# 2022-12-24 21:27:16.169892 -- Starting Blueprint 22
# 2022-12-24 21:27:30.196924 -- Blueprint 22 most 1 in 0:00:14.027032
# 2022-12-24 21:27:30.198926 -- Starting Blueprint 23
# 2022-12-24 21:27:53.840497 -- Blueprint 17 most 2 in 0:01:06.132241
# 2022-12-24 21:27:53.870498 -- Starting Blueprint 24
# 2022-12-24 21:27:54.442496 -- Blueprint 19 most 1 in 0:00:55.538669
# 2022-12-24 21:27:54.446498 -- Starting Blueprint 25
# 2022-12-24 21:28:03.437010 -- Blueprint 18 most 3 in 0:01:11.063197
# 2022-12-24 21:28:03.440009 -- Starting Blueprint 26
# 2022-12-24 21:28:05.188007 -- Blueprint 23 most 1 in 0:00:34.988081
# 2022-12-24 21:28:05.191009 -- Starting Blueprint 27
# 2022-12-24 21:28:06.492010 -- Blueprint 26 most 0 in 0:00:03.051003
# 2022-12-24 21:28:06.495009 -- Starting Blueprint 28
# 2022-12-24 21:28:06.784029 -- Blueprint 24 most 7 in 0:00:12.895533
# 2022-12-24 21:28:06.790030 -- Starting Blueprint 29
# 2022-12-24 21:28:13.402565 -- Blueprint 29 most 1 in 0:00:06.609535
# 2022-12-24 21:28:13.405565 -- Starting Blueprint 30
# 2022-12-24 21:28:18.747564 -- Blueprint 25 most 0 in 0:00:24.299067
# 2022-12-24 21:28:40.454119 -- Blueprint 27 most 6 in 0:00:35.261112
# 2022-12-24 21:28:41.441121 -- Blueprint 30 most 12 in 0:00:28.034556
# 2022-12-24 21:28:49.243152 -- Blueprint 28 most 7 in 0:00:42.745145
# Blueprints dump:
# 1       0       0:00:11.315016
# 2       2       0:00:53.132659
# 3       2       0:00:03.646997
# 4       2       0:00:53.837659
# 5       6       0:01:53.394905
# 6       4       0:00:26.640603
# 7       13      0:00:10.550037
# 8       5       0:00:46.596119
# 9       0       0:00:23.933080
# 10      0       0:00:05.088039
# 11      1       0:00:06.762021
# 12      1       0:00:26.423057
# 13      3       0:00:08.482020
# 14      4       0:00:07.029019
# 15      5       0:00:14.196570
# 16      1       0:00:07.148552
# 17      2       0:01:06.132241
# 18      3       0:01:11.063197
# 19      1       0:00:55.538669
# 20      9       0:00:04.351509
# 21      0       0:00:02.175000
# 22      1       0:00:14.027032
# 23      1       0:00:34.988081
# 24      7       0:00:12.895533
# 25      0       0:00:24.299067
# 26      0       0:00:03.051003
# 27      6       0:00:35.261112
# 28      7       0:00:42.745145
# 29      1       0:00:06.609535
# 30      12      0:00:28.034556
# Answer 1: 1659 in 0:13:39.348033




# PART 2

# (base) C:\Users\Eftychios>python C:\Repos\advent-of-code-python\2022\day-19.py
# 2022-12-24 21:39:53.205261 -- Starting Blueprint 1
# 2022-12-24 21:39:53.208261 -- Starting Blueprint 2
# 2022-12-24 21:39:53.213260 -- Starting Blueprint 3
# 2022-12-24 21:53:04.636597 -- Blueprint 3 most 28 in 0:13:11.423337
# 2022-12-25 01:43:32.958720 -- Blueprint 1 most 9 in 4:03:39.751460
# 2022-12-25 04:36:17.554532 -- Blueprint 2 most 27 in 6:56:24.346271
# Blueprints dump:
# 1       9       4:03:39.751460
# 2       27      6:56:24.346271
# 3       28      0:13:11.423337
# Answer 1: 6804 in 11:13:15.521068
