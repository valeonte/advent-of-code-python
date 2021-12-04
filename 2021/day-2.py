# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 2.

Created on Sat Dec  4 17:19:45 2021

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

with open("inputs/day-2.txt", "r") as f:
    inp_string = f.read()


inp = [s.split(' ') for s in inp_string.split("\n")]

horiz = 0
depth = 0
for move in inp:
    if move[0] == 'forward':
        horiz = horiz + int(move[1])
    elif move[0] == 'down':
        depth = depth + int(move[1])
    elif move[0] == 'up':
        depth = depth - int(move[1])

print('Horizontal', horiz, 'depth', depth, 'Answer 1:', horiz * depth)

horiz = 0
aim = 0
depth = 0
for move in inp:
    s = int(move[1])
    if move[0] == 'forward':
        horiz = horiz + s
        depth = depth + s * aim
    elif move[0] == 'down':
        aim = aim + s
    elif move[0] == 'up':
        aim = aim - s

print('Horizontal', horiz, 'depth', depth, 'aim', aim,
      'Answer 2:', horiz * depth)
