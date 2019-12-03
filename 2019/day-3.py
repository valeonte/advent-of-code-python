# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 20:16:16 2019

@author: Eftychios
"""

import os
import sys
from typing import Iterator, Tuple, Set, Dict

os.chdir("C:/Repos/advent-of-code-python")

class PathTracker:
    
    def __init__(self):
        self.path_points: Dict[Tuple[int, int], int] = dict()
        self.cur_x: int = 0
        self.cur_y: int = 0
        self.steps: int = 0
        
    def GetPointsFromMovement(self,
                              movement_string: str) -> Iterator[Tuple[int, int]]:
        
        direction = movement_string[0]
        steps = int(movement_string[1:])

        for i in range(0, steps):
            
            if direction == 'U':
                self.cur_y += 1
            elif direction == 'D':
                self.cur_y -= 1
            elif direction == 'L':
                self.cur_x -= 1
            elif direction == 'R':
                self.cur_x += 1
            
            yield (self.cur_x, self.cur_y)
    
    def ProcessMovement(self, movement_string: str) -> None:
        
        for p in self.GetPointsFromMovement(movement_string):
            self.steps += 1
            if p in self.path_points.keys():
                continue
            
            self.path_points[p] = self.steps
        
with open("2019/inputs/day3.txt", "r") as f:
    cable1 = f.readline().strip().split(',')
    cable2 = f.readline().strip().split(',')


pt1 = PathTracker()
pt2 = PathTracker()

for m in cable1:
    pt1.ProcessMovement(m)

for m in cable2:
    pt2.ProcessMovement(m)

crossings = set(pt1.path_points.keys()).intersection(pt2.path_points.keys())

min_distance = 1000000000
min_total_steps = 1000000000

for c in crossings:
    distance = abs(c[0]) + abs(c[1])
    if distance < min_distance:
        min_distance = distance
    
    total_steps = pt1.path_points[c] + pt2.path_points[c]
    if total_steps < min_total_steps:
        min_total_steps = total_steps


answer_1 = min_distance
answer_2 = min_total_steps
print(answer_1, answer_2)
