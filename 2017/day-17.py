# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 20:46:17 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict

os.chdir("C:/Repos/advent-of-code-python/2017")

class CircularBuffer:
    def __init__(self, step_move: int):
        self.buffer = [0]
        self.step_move = step_move
        self.cur_pos = 0
        self.buffer_fake_len = 1
    
    def move(self) -> int:
        if self.step_move + self.cur_pos < len(self.buffer):
            self.cur_pos += self.step_move
        else:
            remaining = self.step_move - (len(self.buffer) - self.cur_pos)
            self.cur_pos = remaining % len(self.buffer)

        return self.buffer[self.cur_pos]

    def move_and_fake_insert(self, num: int) -> int:
        remaining = -1
        if self.step_move + self.cur_pos < self.buffer_fake_len:
            self.cur_pos += self.step_move
        else:
            remaining = self.step_move - (self.buffer_fake_len - self.cur_pos)
            self.cur_pos = remaining % self.buffer_fake_len

        self.cur_pos += 1
        self.buffer_fake_len += 1

        if self.cur_pos == 1:
            return 0

        return -1
        

    def insert(self, num: int):
        self.cur_pos += 1
        self.buffer.insert(self.cur_pos, num)


b = CircularBuffer(359)

for i in range(1, 2018):
    b.move()
    b.insert(i)

answer_1 = b.buffer[b.cur_pos+1]

b = CircularBuffer(359)
last_idx = 0
for i in range(1, 50000000):
    if b.move_and_fake_insert(i) == 0:
        print('Got 0 at', i, 'diff', i - last_idx)
        last_idx = i
    if i % 1000000 == 0:
        print('Iteration', i)

answer_2 = last_idx
print(answer_1, answer_2)

if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_2_1(self):
            b = CircularBuffer(3)
            
            for i in range(1, 2018):
                b.move()
                b.insert(i)
            
            self.assertEqual(b.buffer[b.cur_pos+1], 638)
        
    unittest.main()
