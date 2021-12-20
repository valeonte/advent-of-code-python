# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 19.

Created on Sun Dec 19 09:12:10 2021

@author: Eftychios
"""

import os
import math

from dataclasses import dataclass
from typing import List, Iterator

os.chdir("C:/Repos/advent-of-code-python/2021")


with open("inputs/day-19-test.txt", "r") as f:
    inp_string = f.read()

with open("inputs/day-19.txt", "r") as f:
    inp_string = f.read()


@dataclass
class Beacon:
    """Beacon."""

    x: int
    y: int
    z: int

    def __hash__(self) -> str:
        """Make hashable."""
        return self.x * 10000 * 10000 + self.y * 10000 + self.z

    def get_transformations(self) -> Iterator['Beacon']:
        """Get all potential transformations."""
        yield Beacon(self.x, self.y, self.z)
        yield Beacon(-self.y, self.x, self.z)
        yield Beacon(-self.x, -self.y, self.z)
        yield Beacon(self.y, -self.x, self.z)

        yield Beacon(self.x, -self.y, -self.z)
        yield Beacon(self.y, self.x, -self.z)
        yield Beacon(-self.x, self.y, -self.z)
        yield Beacon(-self.y, -self.x, -self.z)

        yield Beacon(self.x, -self.z, self.y)
        yield Beacon(self.z, self.x, self.y)
        yield Beacon(-self.x, self.z, self.y)
        yield Beacon(-self.z, -self.x, self.y)

        yield Beacon(self.x, self.z, -self.y)
        yield Beacon(-self.z, self.x, -self.y)
        yield Beacon(-self.x, -self.z, -self.y)
        yield Beacon(self.z, -self.x, -self.y)

        yield Beacon(-self.z, self.y, self.x)
        yield Beacon(-self.y, -self.z, self.x)
        yield Beacon(self.z, -self.y, self.x)
        yield Beacon(self.y, self.z, self.x)

        yield Beacon(-self.z, -self.y, -self.x)
        yield Beacon(self.y, -self.z, -self.x)
        yield Beacon(self.z, self.y, -self.x)
        yield Beacon(-self.y, self.z, -self.x)

    def get_transformed(self, transformation: int) -> 'Beacon':
        """Get beacon transformed."""
        for i, tr in enumerate(self.get_transformations()):
            if i == transformation:
                return tr

        raise Exception('Transformation not found!')


class Scanner:
    """Scanner."""

    def __init__(self, aa: int):
        self.aa = aa

        self.x: int = None
        self.y: int = None
        self.z: int = None

        self.transformation: int = None

        self.beacons: List[Beacon] = []
        self.distances: List[float] = None

    def __repr__(self):
        """Generate string representation of Scanner."""
        s = f'Scanner {self.aa} with {len(self.beacons)} beacons'
        if self.x is not None:
            s = s + (f' at ({self.x}, {self.y}, {self.z}), '
                     f'trans {self.transformation}')
        return s

    def calculate_distances(self):
        """Calculate distances between all nodes using all as reference."""
        self.distances = []
        for b in self.beacons:
            dists = []
            for bb in self.beacons:
                dist = math.sqrt((b.x - bb.x)**2 +
                                 (b.y - bb.y)**2 +
                                 (b.z - bb.z)**2)
                dists.append(dist)

            self.distances.append(dists)

    def get_absolute_beacons(self):
        """Return beacons with absolute coordinates."""
        for b in self.beacons:
            bb = b.get_transformed(self.transformation)

            yield Beacon(bb.x + self.x, bb.y + self.y, bb.z + self.z)


scanners = []
cur_scanner = None
for row in inp_string.split('\n'):
    if row == '':
        continue

    if row.startswith("---"):
        if cur_scanner is not None:
            cur_scanner.calculate_distances()

        p = row.split(' ')
        aa = int(p[2])
        print('Got new scanner', aa)
        cur_scanner = Scanner(aa)

        scanners.append(cur_scanner)
    else:
        cur_scanner.beacons.append(Beacon(*[int(p) for p in row.split(',')]))
cur_scanner.calculate_distances()


print('Initialising scanner 0')
scanner = scanners[0]
scanner.x = 0
scanner.y = 0
scanner.z = 0
scanner.transformation = 0

while any([s.x is None for s in scanners]):
    for scanner in scanners:
        if scanner.x is None:
            continue

        for ss in scanners:
            if scanner.aa == ss.aa or ss.x is not None:
                continue

            equal_beacons = []
            for b1, d1 in enumerate(scanner.distances):
                dist1 = set(d1)
                if len(dist1) < len(d1):
                    raise Exception('Duplicate distances!')

                for b2, d2 in enumerate(ss.distances):
                    if len(set(d2)) < len(d2):
                        raise Exception('Duplicate distances!')
                    common = dist1.intersection(d2)
                    if len(common) >= 12:
                        # print(len(common), 'common between scanners',
                        #       scanner.aa, 'and', ss.aa, 'and beacons', b1,
                        #       'and', b2)
                        equal_beacons.append((b1, b2))

            if len(equal_beacons) > 0:
                break

        if len(equal_beacons) > 0:
            break

    ss_coords = None

    for b1, b2 in equal_beacons:
        beacon1 = scanner.beacons[b1].get_transformed(scanner.transformation)
        beacon2 = ss.beacons[b2]

        beacon_potential = []
        for tr in beacon2.get_transformations():
            sx = beacon1.x - tr.x
            sy = beacon1.y - tr.y
            sz = beacon1.z - tr.z

            beacon_potential.append((sx, sy, sz))

        if ss_coords is None:
            print('Populating potential ss coords')
            ss_coords = set(beacon_potential)
        else:
            ss_coords = ss_coords.intersection(beacon_potential)
            if len(ss_coords) == 0:
                raise Exception('No common coords!')

    if len(ss_coords) > 1:
        raise Exception('Too many common coords!')

    ss_coords = ss_coords.pop()
    ss.x, ss.y, ss.z = ss_coords
    ss.x = ss.x + scanner.x
    ss.y = ss.y + scanner.y
    ss.z = ss.z + scanner.z
    ss.transformation = beacon_potential.index(ss_coords)

    print('Found scanner', ss.aa, 'coords', ss_coords,
          'and transformation', ss.transformation)


all_beacons = set()
for ss in scanners:
    for b in ss.get_absolute_beacons():
        all_beacons.add(b)

print('Answer 1:', len(all_beacons))


max_distance = 0
for ss1 in scanners:
    for ss2 in scanners:
        distance = abs(ss1.x - ss2.x) + abs(ss1.y - ss2.y) + abs(ss1.z - ss2.z)
        if distance > max_distance:
            max_distance = distance

print('Answer 2:', max_distance)
