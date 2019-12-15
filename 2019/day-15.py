# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 09:06:31 2019

@author: Eftychios
"""

import os
import time
import random
import pickle
from typing import Iterator, Tuple, Dict, List


os.chdir("C:/Repos/advent-of-code-python/2019")

from intcode_runner import IntcodeRunner

with open("inputs/day15.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]


class Droid:
    def __init__(self,
                 pre_map: Dict[Tuple[int,int], int] = None):
        self._mover = IntcodeRunner(inp, inputs = [], extend=10000)
        self._try_move = self._mover.iter_run()
        # coords to tile type: 0 -> wall, 1 -> empty, 2 -> oxygen
        self.map = pre_map or {(0,0): 1}
        self.set_cur_pos(0, 0)
        

    def get_target_pos(self, direction: int) -> Tuple[int, int]:
        if direction == 1:
            return (self.cur_pos[0], self.cur_pos[1]-1)
        if direction == 2:
            return (self.cur_pos[0], self.cur_pos[1]+1)
        if direction == 3:
            return (self.cur_pos[0]+1, self.cur_pos[1])
        if direction == 4:
            return (self.cur_pos[0]-1, self.cur_pos[1])
        
        raise Exception(f'Invalid direction {direction}!')

    def set_cur_pos(self, x: int, y: int):
        self.cur_pos = (x, y)
        if self.map.get((x-1, y)) is None:
            self.map[(x-1, y)] = -1
        if self.map.get((x, y-1)) is None:
            self.map[(x, y-1)] = -1
        if self.map.get((x+1, y)) is None:
            self.map[(x+1, y)] = -1
        if self.map.get((x, y+1)) is None:
            self.map[(x, y+1)] = -1

    def get_avail_directions(self, of_kinds: List[int] = None) -> Iterator[int]:
        yielded = False
        if of_kinds is None:
            of_kinds = [-1]
        if self.map[(self.cur_pos[0], self.cur_pos[1]-1)] in of_kinds:
            yield 1
            yielded = True
        if self.map[(self.cur_pos[0], self.cur_pos[1]+1)] in of_kinds:
            yield 2
            yielded = True
        if self.map[(self.cur_pos[0]+1, self.cur_pos[1])] in of_kinds:
            yield 3
            yielded = True
        if self.map[(self.cur_pos[0]-1, self.cur_pos[1])] in of_kinds:
            yield 4
            yielded = True
        
        if yielded:
            return
        
        for d in self.get_avail_directions([-1, 1, 2]):
            yield d
    
    def move_many(self, directions: Iterator[int]):
        for d in directions:
            self.move(d)
    
    def move(self, direction: int) -> Tuple[int, int]:
        
        target_pos = self.get_target_pos(direction)
        target_tile = self.map.get(target_pos)
        if target_tile is not None and target_tile == 0:
            # tile already explored and is wall, so no moving
            return

        # or else we have to involve the program and move
        self._mover.inputs.append(direction)
        response = next(self._try_move)
        
        if response == 0: # wall
            self.map[target_pos] = 0
            return self.cur_pos
        if response == 1: # empty
            self.map[target_pos] = 1
            self.set_cur_pos(target_pos[0], target_pos[1])
            return target_pos
        
        if response == 2: # oxygen
            self.map[target_pos] = 2
            self.set_cur_pos(target_pos[0], target_pos[1])
            return target_pos
        
        raise Exception(f'Invalid response {response}!')

    def print_map(self):
        
        min_x = min([k[0] for k in self.map.keys()])
        max_x = max([k[0] for k in self.map.keys()])
        min_y = min([k[1] for k in self.map.keys()])
        max_y = max([k[1] for k in self.map.keys()])
        
        for y in range(min_y, max_y + 1):
            row = ''
            for x in range(min_x, max_x + 1):
                if self.cur_pos == (x, y):
                    row += 'D'
                    continue

                tile = self.map.get((x, y))
                if tile is None or tile == -1:
                    row += ' '
                elif tile == 0:
                    row += '#'
                elif tile == 1:
                    row += '.'
                else:
                    row += 'O'
            
            print(row)

def get_map_random_walk():
    map_file = "day-15-full-map.pickle"
    if os.path.exists(map_file):
        with open(map_file, "rb") as f:
            return pickle.load(f)
    
    droid = Droid()
    cnt = 0
    while True:
        next_move = random.choice(list(droid.get_avail_directions()))
        droid.move(next_move)
        unknowns = len([t for t in droid.map.values() if t == -1])
        if unknowns == 0:
            break
        if cnt % 10000 == 0:
            droid.print_map()
            print(unknowns, "unknowns remaining")
            
        cnt += 1

    droid.print_map()
    print("Done in", cnt, "iterations")
    
    with open(map_file, "wb") as f:
        pickle.dump(droid.map, f)
    
    return droid.map

def get_map_oxygen_steps():

    droid = Droid(get_map())
    moves = []
    idx = 0
    visited = set()
    crossroads = []
    while True:
        if idx % 100 == 0:
            droid.print_map()
    
        if droid.map[droid.cur_pos] == 2:
            droid.print_map()
            print("Found oxygen!!")
            return idx
        
        not_visited = [d 
                       for d in droid.get_avail_directions([-1, 1, 2])
                       if droid.get_target_pos(d) not in visited]
        if len(not_visited) == 1:
            new_pos = droid.move(not_visited[0])
            moves.append(not_visited[0])
            visited.add(new_pos)
            #print('single not visited', not_visited[0])
            #time.sleep(0.3)
            idx += 1
        elif len(not_visited) > 1:
            crossroads.append(idx)
            new_pos = droid.move(not_visited[0])
            moves.append(not_visited[0])
            visited.add(new_pos)
            #print('multiple not visited, going for first', not_visited[0])
            #time.sleep(3)
            idx += 1
        else:
            # dead end, go back to cross road
            crossroad = crossroads.pop()
            while idx > crossroad:
                idx -= 1
                moves.pop()
            # resetting droid
            droid = Droid(droid.map)
            # fast forward where we were
            droid.move_many(moves)
            #print("dead end, going back to crossroad", crossroad)
            #time.sleep(3)
        #time.sleep(0.3)
    

def get_map_smart():

    droid = Droid()
    moves = []
    idx = 0
    visited = set()
    crossroads = []
    while True:
        if idx % 100 == 0:
            droid.print_map()
    
    #    if droid.map[droid.cur_pos] == 2:
    #        print("Found oxygen!!")
    #        break
        
        not_visited = [d 
                       for d in droid.get_avail_directions([-1, 1, 2])
                       if droid.get_target_pos(d) not in visited]
        if len(not_visited) == 1:
            new_pos = droid.move(not_visited[0])
            moves.append(not_visited[0])
            visited.add(new_pos)
            #print('single not visited', not_visited[0])
            #time.sleep(0.3)
            idx += 1
        elif len(not_visited) > 1:
            crossroads.append(idx)
            new_pos = droid.move(not_visited[0])
            moves.append(not_visited[0])
            visited.add(new_pos)
            #print('multiple not visited, going for first', not_visited[0])
            #time.sleep(3)
            idx += 1
        else:
            if len(crossroads) == 0:
                droid.print_map()
                print("Full region mapped!")
                break
            # dead end, go back to cross road
            crossroad = crossroads.pop()
            while idx > crossroad:
                idx -= 1
                moves.pop()
            # resetting droid
            droid = Droid(droid.map)
            # fast forward where we were
            droid.move_many(moves)
            #print("dead end, going back to crossroad", crossroad)
            #time.sleep(3)
        #time.sleep(0.3)
    
    return droid.map


#answer_1 = get_map_oxygen_steps()

droid = Droid(get_map_random_walk())
border_tiles = [k for k, v in droid.map.items() if v == 2]

minutes = 0
while len(border_tiles) > 0:
    minutes += 1
    for i in range(0, len(border_tiles)):
        bt = border_tiles.pop(0)
        tiles = [(bt[0], bt[1]-1),
                 (bt[0], bt[1]+1),
                 (bt[0]-1, bt[1]),
                 (bt[0]+1, bt[1])]
        for tile in tiles:
            if droid.map[tile] == 1:
                droid.map[tile] = 2
                border_tiles.append(tile)
    
    droid.print_map()
    print('After', minutes, 'minutes')
    time.sleep(0.5)

answer_2 = minutes - 1