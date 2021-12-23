# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 22.

Created on Wed Dec 22 08:19:38 2021

@author: Eftychios
"""

import os
import re

import numpy as np

from typing import List, Iterator
from dataclasses import dataclass
from logging import getLogger

log = getLogger(__name__)

os.chdir("C:/Repos/advent-of-code-python/2021")


inp_string = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

inp_string = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15"""
# on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
# on x=967..23432,y=45373..81175,z=27513..53682"""

inp_string = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""

with open("inputs/day-22.txt", "r") as f:
    inp_string = f.read()


@dataclass
class CoordSet:
    """A rectangular cuboid defined by ranges along the 3 axis."""

    on: bool

    x1: int
    x2: int

    y1: int
    y2: int

    z1: int
    z2: int

    @staticmethod
    def from_row(row: str) -> 'CoordSet':
        """Get a coord set from a row."""
        pat = "^(on|off) x=([-\d]+)\.\.([-\d]+),y=([-\d]+)\.\.([-\d]+),z=([-\d]+)\.\.([-\d]+)$"  # noqa
        m = re.match(pat, inp)

        state, x1, x2, y1, y2, z1, z2 = m.groups()

        return CoordSet(state == 'on', int(x1), int(x2), int(y1), int(y2),
                        int(z1), int(z2))

    def __hash__(self):
        """Override hash."""
        return hash((self.x1, self.x2, self.y1, self.y2, self.z1, self.z2))

    def __eq__(self, obj: 'CoordSet'):
        """Override equals."""
        return (self.x1 == obj.x1 and self.x2 == obj.x2
                and self.y1 == obj.y1 and self.y2 == obj.y2
                and self.z1 == obj.z1 and self.z2 == obj.z2)

    def is_invalid(self) -> bool:
        """Check if coords are invalid."""
        return self.x2 < self.x1 or self.y2 < self.y1 or self.z2 < self.z1

    def overlaps(self, cs: 'CoordSet') -> bool:
        """Check whether the two cuboids overlap."""
        return ((self.x1 <= cs.x1 and cs.x1 <= self.x2
                 or self.x1 <= cs.x2 and cs.x2 <= self.x2
                 or cs.x1 <= self.x1 and self.x1 <= cs.x2
                 or cs.x1 <= self.x2 and self.x2 <= cs.x2)
                and
                (self.y1 <= cs.y1 and cs.y1 <= self.y2
                 or self.y1 <= cs.y2 and cs.y2 <= self.y2
                 or cs.y1 <= self.y1 and self.y1 <= cs.y2
                 or cs.y1 <= self.y2 and self.y2 <= cs.y2)
                and
                (self.z1 <= cs.z1 and cs.z1 <= self.z2
                 or self.z1 <= cs.z2 and cs.z2 <= self.z2
                 or cs.z1 <= self.z1 and self.z1 <= cs.z2
                 or cs.z1 <= self.z2 and self.z2 <= cs.z2))

    def count_cubes(self) -> int:
        """Count the cubes in the cuboid."""
        return ((self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)
                * (self.z2 - self.z1 + 1))

    def subtract(self, cs: 'CoordSet') -> Iterator['CoordSet']:
        """Return the resulting rectangular cuboids after removing cs."""
        for ret in self.__subtract(cs):
            if not ret.is_invalid():
                #print(ret)
                yield ret

    def __subtract(self, cs: 'CoordSet') -> Iterator['CoordSet']:
        """Return the difference including invalid ones as well."""
        if not self.overlaps(cs):
            yield self
            return

        # We assume cs in contained within self, and we return the 26
        # surrounding cuboids. 9 in the front layer, 9 at the back, and 8 all
        # around the middle. If our assumption is wrong, the extra cuboids will
        # have invalid coords, and will be auto-removed.

        # The edges need to be counted only once

        # Front Layer
        #print('Front Layer')
        # # bottom left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       self.y1, cs.y1 - 1,
                       self.z1, cs.z1 - 1)
        # # bottom center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       self.y1, cs.y1 - 1,
                       self.z1, cs.z1 - 1)
        # # bottom right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       self.y1, cs.y1 - 1,
                       self.z1, cs.z1 - 1)
        # # middle left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       self.y1, cs.y1 - 1,
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # middle center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       self.y1, cs.y1 - 1,
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # middle right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       self.y1, cs.y1 - 1,
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # top left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       self.y1, cs.y1 - 1,
                       cs.z2 + 1, self.z2)
        # # top center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       self.y1, cs.y1 - 1,
                       cs.z2 + 1, self.z2)
        # # top right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       self.y1, cs.y1 - 1,
                       cs.z2 + 1, self.z2)

        #print('Back Layer')
        # Back Layer - the x's and the z's are the same as front, y's change
        # # bottom left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       cs.y2 + 1, self.y2,
                       self.z1, cs.z1 - 1)
        # # bottom center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       cs.y2 + 1, self.y2,
                       self.z1, cs.z1 - 1)
        # # bottom right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       cs.y2 + 1, self.y2,
                       self.z1, cs.z1 - 1)
        # # middle left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       cs.y2 + 1, self.y2,
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # middle center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       cs.y2 + 1, self.y2,
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # middle right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       cs.y2 + 1, self.y2,
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # top left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       cs.y2 + 1, self.y2,
                       cs.z2 + 1, self.z2)
        # # top center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       cs.y2 + 1, self.y2,
                       cs.z2 + 1, self.z2)
        # # top right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       cs.y2 + 1, self.y2,
                       cs.z2 + 1, self.z2)

        #print('Middle Layer')
        # Middle layer - same x's and z's, different y's excluding middle
        # # bottom left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       self.z1, cs.z1 - 1)
        # # bottom center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       self.z1, cs.z1 - 1)
        # # bottom right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       self.z1, cs.z1 - 1)
        # # middle left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # middle right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       max(cs.z1, self.z1), min(cs.z2, self.z2))
        # # top left
        yield CoordSet(True, self.x1, cs.x1 - 1,
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       cs.z2 + 1, self.z2)
        # # top center
        yield CoordSet(True, max(cs.x1, self.x1), min(cs.x2, self.x2),
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       cs.z2 + 1, self.z2)
        # # top right
        yield CoordSet(True, cs.x2 + 1, self.x2,
                       max(cs.y1, self.y1), min(cs.y2, self.y2),
                       cs.z2 + 1, self.z2)


space = np.zeros((101, 101, 101))


for i, inp in enumerate(inp_string.split('\n')):
    cs = CoordSet.from_row(inp)

    try:
        space[cs.x1 + 50: cs.x2 + 51,
              cs.y1 + 50: cs.y2 + 51,
              cs.z1 + 50: cs.z2 + 51] = 1 if cs.on else 0
        print('After cuboid', i + 1, ':', space.sum())
    except Exception:
        pass

print('Answer 1:', space.sum())


def sorted_coords(s: List[CoordSet]):
    """Sort cuiboids."""
    s = sorted(s, key=lambda x: x.z2)
    s = sorted(s, key=lambda x: x.z1)
    s = sorted(s, key=lambda x: x.y2)
    s = sorted(s, key=lambda x: x.y1)
    s = sorted(s, key=lambda x: x.x2)
    return sorted(s, key=lambda x: x.x1)


def consolidate_cuboids(cuboids: List[CoordSet]) -> List[CoordSet]:
    """Consolidate as many as you can cuboids into one."""
    consolidation_made = True
    while consolidation_made:
        consolidation_made = False
        consolidated_node = None
        for i, cs1 in enumerate(cuboids):
            for j, cs2 in enumerate(cuboids):
                if j <= i:
                    continue

                if ((cs2.x1 == cs1.x2 + 1 or cs1.x1 == cs2.x2 + 1)
                        and cs1.y1 == cs2.y1 and cs1.y2 == cs2.y2
                        and cs1.z1 == cs2.z1 and cs1.z2 == cs2.z2):
                    consolidated_node = CoordSet(
                        True, min(cs1.x1, cs2.x1), max(cs1.x2, cs2.x2),
                        cs1.y1, cs1.y2, cs1.z1, cs1.z2)
                elif ((cs2.y1 == cs1.y2 + 1 or cs1.y1 == cs2.y2 + 1)
                        and cs1.x1 == cs2.x1 and cs1.x2 == cs2.x2
                        and cs1.z1 == cs2.z1 and cs1.z2 == cs2.z2):
                    consolidated_node = CoordSet(
                        True, cs1.x1, cs2.x2,
                        min(cs1.y1, cs2.y1), max(cs1.y2, cs2.y2),
                        cs1.z1, cs1.z2)
                elif ((cs2.z1 == cs1.z2 + 1 or cs1.z1 == cs2.z2 + 1)
                        and cs1.x1 == cs2.x1 and cs1.x2 == cs2.x2
                        and cs1.y1 == cs2.y1 and cs1.y2 == cs2.y2):
                    consolidated_node = CoordSet(
                        True, cs1.x1, cs2.x2, cs1.y1, cs2.y2,
                        min(cs1.z1, cs2.z1), max(cs1.z2, cs2.z2))

                if consolidated_node is not None:
                    break
            if consolidated_node is not None:
                break

        if consolidated_node is not None:
            consolidation_made = True

            cuboids = [cub for idx, cub in enumerate(cuboids)
                       if idx != i and idx != j]
            cuboids.append(consolidated_node)

    return cuboids


def count_on(cuboids: List[CoordSet]) -> int:
    """Count on cubes."""
    on_cubes = 0
    for cub in sorted_coords(cuboids):
        cnt = cub.count_cubes()
        #print(cub, cnt, 'cubes')
        on_cubes = on_cubes + cnt

    return on_cubes


# Non overlapping, lit cuboids
cuboids = []
for i, inp in enumerate(inp_string.split('\n')):
    log.info('Processing cuboid %d', i + 1)
    cs = CoordSet.from_row(inp)
    if len(cuboids) == 0 and cs.on:
        cuboids.append(cs)
        continue

    #print(count_on(cuboids))
    # we subtract the new from all existing cuboids
    new_cuboids = []
    for existing in cuboids:
        for rem in existing.subtract(cs):
            new_cuboids.append(rem)

    # Then if on, we add it back
    if cs.on:
        new_cuboids.append(cs)

    #log.info('Consolidating %d new cuboids', len(new_cuboids))
    # In any case, we consolidate here
    cuboids = new_cuboids  # consolidate_cuboids(new_cuboids)
    log.info('%d final cuboids', len(cuboids))

# cs1 = CoordSet(True, 1, 3, 1, 3, 1, 3)
# cs2 = CoordSet(True, 1, 3, 1, 1, 1, 1)

# res = list(cs2.subtract(cs1))
# print('----- Result -----')
# for cub in res:
#     print(cub)



# print('Before---------')
# for cub in cuboids:
#     print(cub)

# print('After----------')
# for cub in new_cuboids:
#     print(cub)


# for cub in sorted_coords(consolidate_cuboids(new_cuboids)):
#     print(cub)


print('Answer 2:', count_on(cuboids))
