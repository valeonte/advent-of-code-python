"""
Advent of Code 2023 day 8.

Created on Sat Dec 09 2023

@author: Eftychios
"""

import os
import math

from dataclasses import dataclass

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


with open("inputs/day-8.txt", "r") as f:
    inp_string = f.read()

inp = inp_string.split('\n')

@dataclass
class Node:
    name: str

    left: str
    right: str

    def move(self, direction: str) -> int:
        if direction == 'R':
            return nodes[self.right]
        if direction == 'L':
            return nodes[self.left]
        raise Exception(f'Unexpected direction {direction}!')


nodes = dict()
for i, line in enumerate(inp):
    if i == 0:
        instructions = line
        continue
    if i > 1:
        name = line[:3]
        node = Node(name, line[7:10], line[12:15])
        nodes[name] = node


cur_node = nodes['AAA']
moves = 0
while cur_node.name != 'ZZZ':
    for inst in instructions:
        moves += 1
        cur_node = cur_node.move(inst)
        if cur_node.name == 'ZZZ':
            break

print('Answer 1', moves)


inp_string = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

# inp = inp_string.split('\n')

nodes = dict()
for i, line in enumerate(inp):
    if i == 0:
        instructions = line
        continue
    if i > 1:
        name = line[:3]
        node = Node(name, line[7:10], line[12:15])
        nodes[name] = node

cur_nodes = [n for n in nodes.values() if n.name.endswith('A')]
starting_nodes = cur_nodes.copy()
moves = 0
cur_inst_idx = 0
final_node_moves = []
while len(cur_nodes) > 0:
    # move all
    moves += 1
    cur_inst = instructions[cur_inst_idx]
    final_nodes = 0
    i = 0
    while i < len(cur_nodes):
        new_node = cur_nodes[i].move(cur_inst)
        cur_nodes[i] = new_node
        if new_node.name.endswith('Z'):
            print('Got final node for node', starting_nodes[i], 'in', moves, 'moves')
            final_node_moves.append(moves)
            cur_nodes.pop(i)
            starting_nodes.pop(i)
        else:
            i += 1
    
    cur_inst_idx += 1
    if cur_inst_idx >= len(instructions):
        cur_inst_idx = 0

print('Answer 2', math.lcm(*final_node_moves))
