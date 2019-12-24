# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 20:41:27 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List
import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2019")

from intcode_runner import IntcodeRunner


with open("inputs/day17.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]

if not 'answer_1' in locals():
    runner = IntcodeRunner(inp, extend=1000000)
    
    maze = []
    row = []
    
    for b in runner.iter_run():
        if b == 10 and row != []:
            maze.append(row)
            row = []
            continue
        
        row.append(chr(b))
    
    for row in maze:
        print(''.join(row))
        
    sum_align = 0
    for i in range(1, len(maze)-1):
        for j in range(1, len(maze[i])-1):
            if maze[i][j] != '#':
                continue
            
            if maze[i-1][j] == '#' and maze[i+1][j] == '#' and maze[i][j-1] == '#' and maze[i][j+1] == '#':
                par_align = i*j
                print('Got intersection at', i, j, 'with parameter', par_align)
                sum_align+=par_align
    
    answer_1 = sum_align

inp[0]=2

Main="A,B,A,B,C,C,B,A,C,A"
###12345678901234567890#
A="L,10,R,8,R,6,R,10"
B="L,12,R,8,L,12"
C="L,10,R,8,R,8"
continuous='n'

#L,10,R,8,R,6,R,10  ,L,12,R,8,L,12,  L,10,R,8,R,6,R,10   ,L,12,R,8,L,12      ,L,10,R,8,R,8    ,L,10,R,8,R,8,       L,12,R,8,L,12,  L,10,R,8,R,6,R,10  ,L,10,R,8,R,8,  L,10,R,8,R,6,R,10

prog_inp = []
for command in [Main, A, B, C, continuous]:
    for ch in command:
        prog_inp.append(ord(ch))
    prog_inp.append(10)

runner = IntcodeRunner(inp, inputs=prog_inp, extend=1000000)
row = ''
for b in runner.iter_run():
    if b == 10:
        if row != '':
            print(row)
            row = ''
        continue
    
    if b > 255:
        break
    row += chr(b)

answer_2 = b

print(answer_2)