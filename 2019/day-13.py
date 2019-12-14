# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 13:20:07 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict

os.chdir("C:/Repos/advent-of-code-python/2019")

from intcode_runner import IntcodeRunner


with open("inputs/day13.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]

p = IntcodeRunner(inp, extend=100000)
output = p.run()


blocks = 0
for i in range(2, len(output), 3):
    tile = output[i]
    if tile < 0 or tile > 4:
        raise Exception(f'Invalid tile at {i} -> {tile}')
    
    if tile == 2:
        blocks+=1

answer_1 = blocks

def print_board(game_board, score = 0):
    score_str = str(score).rjust(10, '0')
    max_x = max([tile[0] for tile, typ in game_board.items()])
    max_y = max([tile[1] for tile, typ in game_board.items()])
    
    for y in range(0, max_y+1):
        row = ''
        for x in range(0, max_x+1):
            if y == 0 and max_x - x < len(score_str):
                row += score_str
                break
            
            tile = game_board.get((x,y))
            if tile is None:
                continue
            
            if tile == 0:
                ch = ' '
            elif tile == 1:
                ch = '#'
            elif tile == 2:
                ch = '*'
            elif tile == 3:
                ch = '-'
            else:
                ch = 'o'
            
            row += ch
        print(row)


game_board = dict()
for i, tile in enumerate(output):
    out_type = i % 3
    if out_type == 0:
        x = tile
    elif out_type == 1:
        y = tile
    else:
        game_board[(x, y)] = tile


p = IntcodeRunner(inp, inputs=[0], extend=100000)
p.program[0]=2

i = 0
game_board = dict()
last_paddle = None
last_ball = None
score_flag = False
score = 0

for tile in p.iter_run():
    out_type = i % 3
    if out_type == 0:
        if tile == -1:
            score_flag = True
        else:
            x = tile
            score_flag = False
    elif out_type == 1:
        if not score_flag:
            y = tile
    else:
        if score_flag:
            score = tile
            print("Got score", score)
        else:
            game_board[(x, y)] = tile
            
            if tile == 3:
                last_paddle = (x, y)
            elif tile == 4:
                last_ball = (x, y)
                if last_paddle is not None:
                    #print_board(game_board, score)
                    if x > last_paddle[0]:
                        #print("Moving right")
                        p.inputs.append(1)
                    elif x < last_paddle[0]:
                        #print("Moving left")
                        p.inputs.append(-1)
                    else:
                        #print("Not moving")
                        p.inputs.append(0)
                    
                    #time.sleep(0.1)

    i += 1

answer_2 = score
#11641

print(answer_1, answer_2)
