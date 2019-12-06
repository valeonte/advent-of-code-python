# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 19:49:57 2019

@author: Eftychios
"""

import os
from typing import List, Dict, Iterator, Set

os.chdir("C:/Repos/advent-of-code-python")


class Planet:
    
    def __init__(self,
                 name: str):
        self.name = name
        self.satellites = []
        self.orbitted = []
        
    def __repr__(self):
        return f'{self.name}, {len(self.satellites)} sat, {len(self.satellites)} orb'
    
    def get_total_satellites(self) -> int:
        ret = 0
        for sat in self.satellites:
            ret += 1
            ret += sat.get_total_satellites()
            
        return ret
    

    def get_shortest_path_to(self, target: str, visited: Set[str]):
        
        all_orbit = self.satellites + self.orbitted
        if target in [s.name for s in all_orbit]:
            return 0
        
        v = visited.copy()
        v.add(self.name)
        
        min_path = 100000000000000
        for s in all_orbit:
            if s.name in v:
                continue
            
            p = s.get_shortest_path_to(target, v)
            if p < min_path:
                min_path = p
        
        return min_path + 1
        


def yield_from_file() -> Iterator[str]:

    with open("2019/inputs/day6.txt", "r") as f:
        line = f.readline()
        while line:
            yield line.strip()
            line = f.readline()

def yield_from_string(inp: str) -> Iterator[str]:
    
    for line in inp.split("\n"):
        yield line


def get_dict_from_input(inp: Iterator[str]) -> Dict[str, Planet]:

    planets = dict()
    
    for line in inp:
        planet_names = line.strip().split(')')
        
        p1 = planets.get(planet_names[0]) or Planet(planet_names[0])
        p2 = planets.get(planet_names[1]) or Planet(planet_names[1])
        p1.satellites.append(p2)
        p2.orbitted.append(p1)
        planets[p1.name] = p1
        planets[p2.name] = p2

    return planets



planets = get_dict_from_input(yield_from_file())

answer_1 = sum([planet.get_total_satellites() for planet in planets.values()])
answer_2 = planets['YOU'].get_shortest_path_to("SAN", set()) - 1

print(answer_1, answer_2)

if __name__ == "__main__":
    
    import unittest
    
    class TestAll(unittest.TestCase):
        
        def test_1(self):
            planets = get_dict_from_input(yield_from_string("""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""))
            
            total_sats = sum([
                    planet.get_total_satellites()
                    for planet in planets.values()])
    
            self.assertEqual(total_sats, 42)

        def test_2(self):
            planets = get_dict_from_input(yield_from_string("""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""))
            self.assertEqual(planets['YOU'].get_shortest_path_to("SAN", set()), 5)

    unittest.main()

