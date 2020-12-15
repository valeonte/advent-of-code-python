# -*- coding: utf-8 -*-
"""
Day 12 Advent of Code 2020 file.

Created on Tue Dec 15 17:39:01 2020

@author: Eftychios
"""

import os
import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """F10
N3
F7
R90
F11"""

with open("inputs/day-12.txt", "r") as f:
    inp_string = f.read()


direction = 'E'
cur_x = 0
cur_y = 0


for action in inp_string.split('\n'):
    command = action[0]
    n = int(action[1:])

    if command == 'N':
        cur_y += n
    elif command == 'S':
        cur_y -= n
    elif command == 'E':
        cur_x += n
    elif command == 'W':
        cur_x -= n
    elif command == 'L':
        for _ in range(0, n, 90):
            if direction == 'E':
                direction = 'N'
            elif direction == 'N':
                direction = 'W'
            elif direction == 'W':
                direction = 'S'
            elif direction == 'S':
                direction = 'E'
            else:
                raise Exception(f'Bad current direction {direction}!')
    elif command == 'R':
        for _ in range(0, n, 90):
            if direction == 'E':
                direction = 'S'
            elif direction == 'N':
                direction = 'E'
            elif direction == 'W':
                direction = 'N'
            elif direction == 'S':
                direction = 'W'
            else:
                raise Exception(f'Bad current direction {direction}!')
    elif command == 'F':
        if direction == 'E':
            cur_x += n
        elif direction == 'N':
            cur_y += n
        elif direction == 'W':
            cur_x -= n
        elif direction == 'S':
            cur_y -= n
        else:
            raise Exception(f'Bad current direction {direction}!')
    else:
        raise Exception(f'Bad command {command}!')

print('Answer 1:', abs(cur_x) + abs(cur_y))


wp_x = 10
wp_y = 1
ship_x = 0
ship_y = 0

for action in inp_string.split('\n'):
    command = action[0]
    n = int(action[1:])

    if command == 'N':
        wp_y += n
    elif command == 'S':
        wp_y -= n
    elif command == 'E':
        wp_x += n
    elif command == 'W':
        wp_x -= n
    elif command == 'L':
        if n % 90 != 0:
            raise Exception(f'Bad number with turn {command}!')
        for _ in range(0, n, 90):
            new_wp_x = - wp_y
            new_wp_y = wp_x
            wp_y = new_wp_y
            wp_x = new_wp_x
    elif command == 'R':
        if n % 90 != 0:
            raise Exception(f'Bad number with turn {command}!')
        for _ in range(0, n, 90):
            s = np.sign(wp_x) * np.sign(wp_y)
            new_wp_x = wp_y
            new_wp_y = - wp_x
            wp_y = new_wp_y
            wp_x = new_wp_x
    elif command == 'F':
        ship_x += n * wp_x
        ship_y += n * wp_y
    else:
        raise Exception(f'Bad command {command}!')

print('Answer 2:', abs(ship_x) + abs(ship_y))
