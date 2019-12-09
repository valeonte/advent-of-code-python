# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 20:06:38 2019

@author: Eftychios
"""

import os
from typing import List, Dict

os.chdir("C:/Repos/advent-of-code-python")


class Layer:
    def __init__(self, depth: int, rng: int):
        self.depth: int = depth
        self.rng: int = rng
        self.scanner: int = 0
        self.divisor: int = 2*(self.rng - 1)

    def reset(self):
        self.scanner = 0

    def move(self, times: int = 1):
        moves = times % self.divisor
        if moves < self.rng:
            self.scanner = moves
        else:
            self.scanner = self.rng - (moves - self.rng) - 2

    def crashed(self) -> bool:
        return self.scanner == 0

    def get_score_if_crashed(self) -> int:
        return self.depth*self.rng if self.crashed() else 0
    
    def __repr__(self):
        return f'Layer @{self.depth} with range {self.rng}'
        

class Firewall:
    def __init__(self):
        self.layers: Dict[int, Layer] = dict()
        self.max_depth: int = -1
    
    def initialise(self, config: str):
        for layer in config.split('\n'):
            parts = layer.strip().split(':')
            depth = int(parts[0].strip())
            rng = int(parts[1].strip())
            
            self.layers[depth] = Layer(depth, rng)
        
        self.max_depth = max(self.layers.keys())

    def move(self):
        for layer in self.layers.values():
            layer.move()

    def crashed(self, delay: int) -> bool:

        for l in self.layers.values():
            
            # move for the in-between missing layers
            l.move(delay + l.depth)
            if l.crashed():
                return True
            
        return False

    def reset(self):
        for layer in self.layers.values():
            layer.reset()

    def get_crash_score(self) -> int:
        crash_score = 0

        for l in self.layers.values():
            
            # move for the in-between missing layers
            l.move(l.depth)
            crash_score += l.get_score_if_crashed()
            
        return crash_score


with open("2017/inputs/day13.txt", "r") as f:
    inputs = f.read()

f = Firewall()
f.initialise(inputs)
answer_1 = f.get_crash_score()


delay = 0
f = Firewall()
f.initialise(inputs)

while f.crashed(delay):
    delay += 1
    if delay % 100000 == 0:
        print(f'Trying delay {delay}')
    f.reset()

answer_2 = delay

print(answer_1, answer_2)

if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_1(self):
            f = Firewall()
            f.initialise("""0: 3
            1: 2
            4: 4
            6: 4""")
            
            self.assertEqual(f.get_crash_score(), 24)

        def test_2(self):
            delay = 0
            f = Firewall()
            f.initialise("""0: 3
1: 2
4: 4
6: 4""")
            
            while f.crashed(delay):
                delay += 1
                f.reset()

            self.assertEqual(delay, 10)

    unittest.main()
