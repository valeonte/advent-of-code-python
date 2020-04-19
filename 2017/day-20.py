# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:29:14 2020

@author: Eftychios
"""

import os
import time
import re

from dataclasses import dataclass
from typing import Set

os.chdir("C:/Repos/advent-of-code-python/2017")

with open("inputs/day20.txt", "r") as f:
    inp = f.read()


@dataclass
class Coords:
    x: int
    y: int
    z: int

    def distance(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass
class Particle:
    pid: int
    p: Coords
    v: Coords
    a: Coords

    def distance(self):
        return self.p.distance()


class Gpu:
    def __init__(self, particles: str):
        pattern = ('^p=<([-\\d]+),([-\\d]+),([-\\d]+)>, '
                   'v=<([-\\d]+),([-\\d]+),([-\\d]+)>, '
                   'a=<([-\\d]+),([-\\d]+),([-\\d]+)>$')

        self.particles = []
        idx = 0
        for part in particles.split('\n'):
            r = re.search(pattern, part)
            p = Coords(int(r.group(1)), int(r.group(2)), int(r.group(3)))
            v = Coords(int(r.group(4)), int(r.group(5)), int(r.group(6)))
            a = Coords(int(r.group(7)), int(r.group(8)), int(r.group(9)))
            self.particles.append(Particle(idx, p, v, a))
            idx += 1

    def move_particle(self, particle: Particle):
        particle.v.x += particle.a.x
        particle.v.y += particle.a.y
        particle.v.z += particle.a.z

        particle.p.x += particle.v.x
        particle.p.y += particle.v.y
        particle.p.z += particle.v.z

    def move(self, moves: int = 1,
             remove_collided: bool = False):
        for _ in range(0, moves):
            for particle in self.particles:
                self.move_particle(particle)

            if remove_collided:
                self.remove_collided()

    def remove_collided(self):
        coll = self.locate_collided()
        if len(coll) > 0:
            print('Removing collided', coll)

            self.particles = [p
                              for p in self.particles
                              if p.pid not in coll]

    def locate_collided(self) -> Set[int]:
        ret = set()
        for idx, particle in enumerate(self.particles):
            for other in self.particles[idx + 1:]:
                if other.pid == particle.pid:
                    continue
                if other.p == particle.p:
                    ret.add(particle.pid)
                    ret.add(other.pid)
        return ret

    def get_closest(self):
        closest_distance = 999999999999
        closest_node = -1

        for particle in self.particles:
            dist = particle.distance()
            if dist < closest_distance:
                closest_distance = dist
                closest_node = particle.pid

        return closest_node, closest_distance


particles = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"""

g = Gpu(inp)
while True:
    g.move(100, True)
    print(g.get_closest())
    time.sleep(0.4)


if __name__ == '__main__':

    import unittest

    class TestAll(unittest.TestCase):

        def test_init(self):
            particles = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"""

            g = Gpu(particles)

            self.assertEqual(len(g.particles), 2)
            self.assertEqual(g.particles[0].p.x, 3)
            self.assertEqual(g.particles[1].a.x, -2)

        def test_move(self):
            particles = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"""

            g = Gpu(particles)
            g.move()

            self.assertEqual(g.particles[0].p.x, 4)
            self.assertEqual(g.particles[1].v.x, -2)
            self.assertEqual(g.particles[1].a.x, -2)

    unittest.main()
