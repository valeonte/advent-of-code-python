# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 15.

Created on Thu Dec 15 12:42:56 2022

@author: Eftychios
"""

import os
import re


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

check_y = 10
max_dim = 20

with open("inputs/day-15.txt", "r") as f:
    inp_string = f.read()
check_y = 2000000
max_dim = 4000000

pat = re.compile(r'^Sensor at x=([\-\d]+), y=([\-\d]+): closest beacon is at x=([\-\d]+), y=([\-\d]+)$')

sensor_beacons = []
check_y_occuppied = set()
for row in inp_string.split('\n'):
    m = pat.match(row)
    g = m.groups()
    sx = int(g[0])
    sy = int(g[1])
    bx = int(g[2])
    by = int(g[3])
    bs = dict(sensor_x = sx,
              sensor_y = sy,
              beacon_x = bx,
              beacon_y = by)
    dist = (abs(bs['sensor_x'] - bs['beacon_x'])
            + abs(bs['sensor_y'] - bs['beacon_y']))
    bs['distance'] = dist

    dif_x = 0
    while abs(sy - check_y) + dif_x <= dist:
        check_y_occuppied.add(sx + dif_x)
        check_y_occuppied.add(sx - dif_x)
        dif_x += 1

    sensor_beacons.append(bs)

for bs in sensor_beacons:
    if bs['sensor_y'] == check_y and bs['sensor_x'] in check_y_occuppied:
        check_y_occuppied.remove(bs['sensor_x'])
    if bs['beacon_y'] == check_y and bs['beacon_x'] in check_y_occuppied:
        check_y_occuppied.remove(bs['beacon_x'])

print('Answer 1:', len(check_y_occuppied))


x = 0
y = max_dim
found = True
while found:
    found = False
    for bs in sensor_beacons:
        if (abs(x - bs['sensor_x'])
                + abs(y - bs['sensor_y']) <= bs['distance']):
            found = True
            avail_dist = bs['distance'] - abs(y - bs['sensor_y'])
            x = bs['sensor_x'] + avail_dist
            break
    if not found:
        print('Found possible beacon', x, y)
        break
    if x < max_dim:
        x += 1
    else:
        x = 0
        y -= 1
        if y % 100000 == 0:
            print('y =', y)

print('Answer 1:', x * 4000000 + y)
