# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 21:28:26 2019

@author: Eftychios
"""

import os
os.chdir("C:/Repos/advent-of-code-python")

class HexNode:
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def move(self, direction: str) -> 'HexNode':
        
        if direction == 's':
            return HexNode(self.x, self.y - 1)
        if direction == 'se':
            return HexNode(self.x + 1, self.y - (self.x % 2))
        if direction == 'sw':
            return HexNode(self.x - 1, self.y - (self.x % 2))
        if direction == 'n':
            return HexNode(self.x, self.y + 1)
        if direction == 'ne':
            return HexNode(self.x + 1, self.y + (1 ^ (self.x % 2)))
        if direction == 'nw':
            return HexNode(self.x - 1, self.y + (1 ^ (self.x % 2)))
        
        raise Exception(f'Unexpected direction {direction}!')

    def move_many(self, directions: str) -> 'HexNode':
        
        ret = self
        for d in directions.split(','):
            ret = ret.move(d)
        
        return ret

    def distance_from(self, node: 'HexNode') -> int:
        d = 0
        n = node

        while True:
            
            if n.x == self.x:
                if n.y == self.y:
                    return d # we're there
                if n.y < self.y:
                    next_move = 'n'
                else:
                    next_move = 's'
            elif n.x < self.x:
                if n.y == self.y:
                    if abs(n.x - self.x) == 1:
                        return d + 1
                    next_move = 'se' if n.y % 2 == 0 else 'ne'
                if n.y < self.y:
                    next_move = 'ne'
                else:
                    next_move = 'se'
            else:
                if n.y == self.y:
                    if abs(n.x - self.x) == 1:
                        return d + 1
                    next_move = 'sw' if n.y % 2 == 0 else 'nw'
                if n.y < self.y:
                    next_move = 'nw'
                else:
                    next_move = 'sw'
            
            n = n.move(next_move)
            d += 1

        
    def __repr__(self):
        return f'({self.x}, {self.y})'
    


with open("2017/inputs/day11.txt", "r") as f:
    inputs = f.read()

start_node = HexNode(0, 0)

furthest_distance = -1
furthest_node = None
end_node = start_node
for d in inputs.split(','):
    end_node = end_node.move(d)
    dist = start_node.distance_from(end_node)
    if dist > furthest_distance:
        furthest_node = end_node
        furthest_distance = dist

answer_1 = start_node.distance_from(end_node)
answer_2 = furthest_distance

print(answer_1, answer_2)


if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_1(self):
            start_node = HexNode(0, 0)
            end_node = start_node.move_many('ne,ne,ne')
            
            distance = start_node.distance_from(end_node)
            
            self.assertEqual(distance, 3)
            
        def test_2(self):
            start_node = HexNode(0, 0)
            end_node = start_node.move_many('ne,ne,sw,sw')
            
            distance = start_node.distance_from(end_node)
            
            self.assertEqual(distance, 0)

        def test_3(self):
            start_node = HexNode(0, 0)
            end_node = start_node.move_many('ne,ne,s,s')
            
            distance = start_node.distance_from(end_node)
            
            self.assertEqual(distance, 2)

        def test_4(self):
            start_node = HexNode(0, 0)
            end_node = start_node.move_many('se,sw,se,sw,sw')
            
            distance = start_node.distance_from(end_node)
            
            self.assertEqual(distance, 3)
    
    unittest.main()

