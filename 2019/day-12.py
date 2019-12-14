# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 20:25:36 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List

os.chdir("C:/Repos/advent-of-code-python")

class Tuple3d:
    
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        x = str(self.x).rjust(4, " ")
        y = str(self.y).rjust(4, " ")
        z = str(self.z).rjust(4, " ")
        return f'<x={x}, y={y}, z={z}>'
    
    def __eq__(self, other):
        if not isinstance(other, Tuple3d):
            return False
        
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def abs_sum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

class Moon:
    def __init__(self,
                 pos: Tuple3d,
                 vel: Tuple3d = None):
        self.pos = pos
        self.vel = vel or Tuple3d(0,0,0)
        
    def __repr__(self):
        return f'pos={self.pos}, vel={self.vel}'
        
    def __eq__(self, other):
        if not isinstance(other, Moon):
            return False
        
        return self.pos == other.pos and self.vel == other.vel
    
    def apply_gravity_x_from(self, moon: "Moon") -> None:
        if self.pos.x < moon.pos.x:
            self.vel.x += 1
        elif self.pos.x > moon.pos.x:
            self.vel.x -= 1
    
    def apply_gravity_y_from(self, moon: "Moon") -> None:
        if self.pos.y < moon.pos.y:
            self.vel.y += 1
        elif self.pos.y > moon.pos.y:
            self.vel.y -= 1
            
    def apply_gravity_z_from(self, moon: "Moon") -> None:
        if self.pos.z < moon.pos.z:
            self.vel.z += 1
        elif self.pos.z > moon.pos.z:
            self.vel.z -= 1

    def apply_gravity_from(self, moon: "Moon") -> None:
        self.apply_gravity_x_from(moon);
        self.apply_gravity_y_from(moon);
        self.apply_gravity_z_from(moon);

    def apply_velocity(self) -> None:
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def get_total_energy(self):
        pot = self.pos.abs_sum()
        kin = self.vel.abs_sum()
        return pot*kin
        

def move_moons(moons: List[Moon], steps: int):
    
    for i in range(0, steps):
        for i, a in enumerate(moons):
            for b in moons[i+1:len(moons)]:
                a.apply_gravity_from(b)
                b.apply_gravity_from(a)
            
            a.apply_velocity()


def print_x(moons: List[Moon], offset: int = 20) -> None:

    ret = [' ']*offset
    for i, m in enumerate(moons):
        ret[m.pos.x+offset//2] = str(i)
    
    return ''.join(ret)


def gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def lcm(x, y):
   lcm = (x*y)//gcd(x,y)
   return lcm
    
moons = [Moon(Tuple3d(13,9,5)),
         Moon(Tuple3d(8,14,-2)),
         Moon(Tuple3d(-5,4,11)),
         Moon(Tuple3d(2,-6,1))]

move_moons(moons, 1000)

answer_1 = sum([m.get_total_energy() for m in moons])

moons = [Moon(Tuple3d(13,9,5)),
         Moon(Tuple3d(8,14,-2)),
         Moon(Tuple3d(-5,4,11)),
         Moon(Tuple3d(2,-6,1))]

# we find the period on each dimension
past_sets_x = set()
past_sets_y = set()
past_sets_z = set()

x_done = False
y_done = False
z_done = False
while not x_done or not y_done or not z_done:
    if not x_done:
        cur_set_x = tuple([m.pos.x for m in moons]+[m.vel.x for m in moons])
        if cur_set_x in past_sets_x:
            x_done = True
        past_sets_x.add(cur_set_x)

    if not y_done:
        cur_set_y = tuple([m.pos.y for m in moons]+[m.vel.y for m in moons])
        if cur_set_y in past_sets_y:
            y_done = True
    past_sets_y.add(cur_set_y)
    
    if not z_done:
        cur_set_z = tuple([m.pos.z for m in moons]+[m.vel.z for m in moons])
        if cur_set_z in past_sets_z:
            z_done = True
    past_sets_z.add(cur_set_z)
    
    move_moons(moons, 1)

# and then find the least common multiple of the periods

answer_2 = lcm(lcm(len(past_sets_x), len(past_sets_y)), len(past_sets_z))

print(answer_1, answer_2)

if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_1(self):
            moons = [Moon(Tuple3d(-1,0,2)),
                     Moon(Tuple3d(2,-10,-7)),
                     Moon(Tuple3d(4,-8,8)),
                     Moon(Tuple3d(3,5,-1))]
            
            move_moons(moons, 10)
            
            self.assertEqual(moons[0], Moon(Tuple3d(2,1,-3), Tuple3d(-3,-2,1)))
            self.assertEqual(moons[1], Moon(Tuple3d(1,-8,0), Tuple3d(-1,1,3)))
            self.assertEqual(moons[2], Moon(Tuple3d(3,-6,1), Tuple3d(3,2,-3)))
            self.assertEqual(moons[3], Moon(Tuple3d(2,0,4), Tuple3d(1,-1,-1)))
            
            total_energy = sum([m.get_total_energy() for m in moons])
            self.assertEqual(total_energy, 179)
            
        def test_2(self):
            moons = [Moon(Tuple3d(-8,-10,0)),
                     Moon(Tuple3d(5,5,10)),
                     Moon(Tuple3d(2,-7,3)),
                     Moon(Tuple3d(9,-8,-3))]
            
            move_moons(moons, 100)
            
            total_energy = sum([m.get_total_energy() for m in moons])
            self.assertEqual(total_energy, 1940)

    unittest.main()
