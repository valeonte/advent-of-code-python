# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 09:58:31 2019

@author: Eftychios
"""

import os
from typing import List, Set, Iterator, Dict
os.chdir("C:/Repos/advent-of-code-python")

class Village:
    
    def __init__(self, name: int):
        self.name = name
        self.connected: List['Village'] = []

    def __repr__(self):
        return f'Village {self.name} with {len(self.connected)} connected'
    
    def get_all_connected(self, added: Set['Village']) -> Iterator['Village']:
        
        if self in added:
            return
        
        yield self
        added.add(self)
                
        for conn in self.connected:
            for coconn in conn.get_all_connected(added):
                yield coconn
            
        
    def get_all_villages(inp: str) -> Dict[int, 'Village']:
        villages = dict()

        for line in inp.split("\n"):
            p = line.split('<->')
            name = int(p[0].strip())
            
            village = villages.get(name, Village(name))
            connected = p[1].split(',')
            for conn in [int(c.strip()) for c in connected]:
                connvillage = villages.get(conn, Village(conn))
                village.connected.append(connvillage)
                villages[conn] = connvillage
        
            villages[name] = village
            
        return villages


with open("2017/inputs/day12.txt", "r") as f:
    inp = f.read()


villages = Village.get_all_villages(inp)
connected_with_0 = {v.name for v in villages[0].get_all_connected(set())}

answer_1 = len(connected_with_0)

ungrouped = set(villages.keys())

group_cnt = 0
while len(ungrouped) > 0:
    group_cnt += 1
    village = next(iter(ungrouped))
    connected = {v.name for v in villages[village].get_all_connected(set())}
    ungrouped = ungrouped.difference(connected)
    
answer_2 = group_cnt

print(answer_1, answer_2)


if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_1(self):
            inp = """0 <-> 2
            1 <-> 1
            2 <-> 0, 3, 4
            3 <-> 2, 4
            4 <-> 2, 3, 6
            5 <-> 6
            6 <-> 4, 5"""
            
            villages = Village.get_all_villages(inp)
            connected_with_0 = {v.name for v in villages[0].get_all_connected(set())}
            missing = set(villages.keys()).difference(connected_with_0)
            
            self.assertSetEqual(missing, {1})

    unittest.main()
