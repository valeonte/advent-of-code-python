# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 20:08:58 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict

os.chdir("C:/Repos/advent-of-code-python/2017")

with open("inputs/day16.txt", "r") as f:
    inp = f.read().split(',')

class Dancers:
    def __init__(self, dancers: int):
        dance_string = ''
        base = ord('a')
        for i in range(0, dancers):
            dance_string += chr(base + i)
        
        self.dance_string = dance_string
        self.dancers = dancers
        
    def spin(self, x: int) -> str:
        return (self.dance_string[self.dancers-x:self.dancers] +
                self.dance_string[0:self.dancers-x])
        
    def exchange(self, a: int, b: int) -> Iterator[str]:
        val_a = self.dance_string[a]
        val_b = self.dance_string[b]
        for i, ch in enumerate(self.dance_string):
            if i == a:
                yield val_b
            elif i == b:
                yield val_a
            else:
                yield ch

    def partner(self, a: str, b: str) -> Iterator[str]:
        for ch in self.dance_string:
            if ch == a:
                yield b
            elif ch == b:
                yield a
            else:
                yield ch
    
    def dance_move(self, move: str) -> None:
        if move[0] == 's':
            self.dance_string = self.spin(int(move[1:len(move)]))
        elif move[0] == 'x':
            parts = move[1:len(move)].split('/')
            self.dance_string = ''.join(self.exchange(int(parts[0]), int(parts[1])))
        elif move[0] == 'p':
            self.dance_string = ''.join(self.partner(move[1], move[3]))
        else:
            raise Exception(f'Invalid move {move}!')


dan = Dancers(16)
for move in inp:
    dan.dance_move(move)

answer_1 = dan.dance_string


dan = Dancers(16)
orig = dan.dance_string

# we try to find a period in the output
for i in range(0, 1000000000):
    for move in inp:
        dan.dance_move(move)
    
    if orig == dan.dance_string:
        break

period = i+1
# then take the remnant
remn = 1000000000 % period

# and do as many dances
dan = Dancers(16)
for i in range(0, remn):
    for move in inp:
        dan.dance_move(move)

answer_2 = dan.dance_string

print(answer_1, answer_2)
