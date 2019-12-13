# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 19:40:11 2019

@author: Eftychios
"""

import os
from typing import Iterator, Tuple, Dict, Set
import matplotlib

from intcode_runner import IntcodeRunner
os.chdir("C:/Repos/advent-of-code-python")

with open("2019/inputs/day11.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]

def run_painting_robot(initial_input: int) -> Dict[Tuple[int, int], int]:
    
    r = IntcodeRunner(inp, inputs=[initial_input], extend=10000)
    
    itrun = r.iter_run()
    
    painted_nodes: Dict[Tuple[int, int], int] = dict()
    orientation = 'N'
    cur_node = (0,0)
    
    while True:
        
        try:
            next_colour = next(itrun)
            next_direction = next(itrun)
        except StopIteration:
            return painted_nodes
        
        painted_nodes[cur_node] = next_colour
        if (next_direction == 0 and orientation == 'N'
            or next_direction == 1 and orientation == 'S'):
            # western square
            cur_node = (cur_node[0] - 1, cur_node[1])
            orientation = 'W'
        elif (next_direction == 0 and orientation == 'W'
              or next_direction == 1 and orientation == 'E'):
            # southern square
            cur_node = (cur_node[0], cur_node[1] - 1)
            orientation = 'S'
        elif (next_direction == 0 and orientation == 'S'
              or next_direction == 1 and orientation == 'N'):
            # eastern square
            cur_node = (cur_node[0] + 1, cur_node[1])
            orientation = 'E'
        elif (next_direction == 0 and orientation == 'E'
              or next_direction == 1 and orientation == 'W'):
            # southern square
            cur_node = (cur_node[0], cur_node[1] + 1)
            orientation = 'N'
        
        cur_colour = painted_nodes.get(cur_node) or 0
        r.inputs.append(cur_colour)

painted_nodes = run_painting_robot(0)
answer_1 = len(painted_nodes)

painted_nodes = run_painting_robot(1)

black_nodes = {k for k, v in painted_nodes.items() if v == 1}

x,y = zip(*black_nodes)
matplotlib.pyplot.scatter(x,y)

# inspection yields RAPRCBPH
