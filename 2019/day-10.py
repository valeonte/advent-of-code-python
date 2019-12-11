# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 20:35:34 2019

@author: Eftychios
"""

import os
from typing import List, Set, Tuple, Iterator, Dict
from fractions import Fraction

os.chdir("C:/Repos/advent-of-code-python")


class AsteroidMap:
    def __init__(self, str_map: str):
        self.asteroids: Set[Tuple[int, int]] = []
        
        for y, line in enumerate(str_map.split("\n")):
            for x, ch in enumerate(line):
                if ch == '#':
                    self.asteroids.append((x, y))
            
        self.width = x+1
        self.height = y+1

    def __str__(self):
        
        ret = ''
        for x in range(0, self.width):
            for y in range(0, self.height):
                ret += '#' if (x, y) in self.asteroids else '.'
            
            ret += "\n"
        
        return ret

    def get_asteroid_dict(self, asteroid: Tuple[int, int]) -> Dict[Fraction, List[Tuple[int,int]]]:
        inf = Fraction(-1000000000, 1)

        visible: Dict[Fraction, List[Tuple[int,int]]] = dict()
        
        found_self = False
        for v in self.asteroids:
            if v == asteroid:
                found_self = True
                for l in visible.values():
                    l.append(asteroid)
                continue
            
            slope = Fraction(v[1] - asteroid[1], v[0] - asteroid[0]) if v[0] != asteroid[0] else inf
            
            if slope in visible.keys():
                asts = visible[slope]
            else:
                asts = [asteroid] if found_self else []
                visible[slope] = asts
            asts.append(v)
            
        return visible
        
    def get_vaporized_asteroids(self,
                                asteroid: Tuple[int, int],
                                asteroid_dict: Dict[Fraction, List[Tuple[int,int]]]) -> Iterator[Tuple[int, int]]:
        
        slopes = list(asteroid_dict.keys())
        slopes.sort()
        cnt = 0
        i = 0
        before = True
        while len(slopes) > 0:
            if i == len(slopes):
                before = not before
                i = 0
            
            slope = slopes[i]
            asteroids = asteroid_dict[slope]
            self_index = asteroids.index(asteroid)
            if (before and slope<0 or not before and slope>=0) and self_index != 0:
                cnt += 1
                #print(f'{cnt}. Fraction {slope}, vaporized {asteroids[self_index - 1]}')                
                yield asteroids[self_index - 1]
                del asteroids[self_index - 1]
            elif (not before and slope<0 or before and slope>=0) and self_index != len(asteroids) - 1:
                cnt += 1
                #print(f'{cnt}. Fraction {slope}, vaporized {asteroids[self_index + 1]}')
                yield asteroids[self_index + 1]
                del asteroids[self_index + 1]
            
            if len(asteroids) == 1: # just self remains
                del slopes[i]
            else:
                i += 1
    
    def get_best_asteroid(self) -> Tuple[int, Tuple[int,int]]:
        
        max_visible = -1
        max_visible_asteroid = None

        for asteroid in self.asteroids:
            visible = self.get_asteroid_dict(asteroid)
            
            cnt = 0
            for l in visible.values():
                self_index = l.index(asteroid)
                if self_index == 0 or self_index == len(l) - 1:
                    cnt += 1
                else:
                    cnt += 2
        
            if cnt > max_visible:
                max_visible = cnt
                max_visible_asteroid = asteroid
                
        return (max_visible, max_visible_asteroid)
        

with open("2019/inputs/day10.txt", "r") as f:
    inp = f.read()


m = AsteroidMap(inp)
answer_1 = m.get_best_asteroid()

best_asteroid = answer_1[1]
best_asteroid_dict = m.get_asteroid_dict(best_asteroid)

vap = list(m.get_vaporized_asteroids(best_asteroid, best_asteroid_dict))

answer_2 = vap[199][0]*100 + vap[199][1]

print(answer_1[0], answer_2)

if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_2_1(self):
            m = AsteroidMap(""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""")
            
            asteroid = (8,3)
            asteroid_dict = m.get_asteroid_dict(asteroid)
            
            vap = list(m.get_vaporized_asteroids(asteroid, asteroid_dict))
            
            self.assertEqual(vap[8], (15, 1))
            self.assertEqual(vap[17], (4, 4))
            self.assertEqual(vap[26], (5, 1))
            self.assertEqual(vap[35], (14, 3))
        
        def test_1(self):
            inp = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

            m = AsteroidMap(inp)
            
            self.assertEqual(m.get_best_asteroid(), (33, (5, 8)))


        def test_2(self):
            inp = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

            m = AsteroidMap(inp)
            
            self.assertEqual(m.get_best_asteroid(), (35, (1, 2)))


        def test_3(self):
            inp = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

            m = AsteroidMap(inp)
            
            self.assertEqual(m.get_best_asteroid(), (41, (6, 3)))

        def test_4(self):
            inp = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

            m = AsteroidMap(inp)
            
            self.assertEqual(m.get_best_asteroid(), (210, (11, 13)))


    unittest.main()
