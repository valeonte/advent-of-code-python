# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 21:02:42 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List, NamedTuple, Set
from random import shuffle

os.chdir("C:/Repos/advent-of-code-python/2019")


class KeySteps(NamedTuple):
    key: str
    destination: Tuple[int, int]
    steps: int


class Vault:
    def __init__(self,
                 vault_map: str):

        self.vault_map = vault_map.splitlines()

        self.entrance_nodes = []
        for y, line in enumerate(self.vault_map):
            for x, ch in enumerate(line):
                if ch == '@':
                    self.entrance_nodes.append((x, y))

        cnt = 0
        for line in self.vault_map:
            for ch in line:
                if ch.isalpha() and ch.islower():
                    cnt += 1

        self.key_count = cnt
        self.reset_steps_run()

        # dict from, keys+cur node, to cost/min path
        self.steps_cache: Dict[Tuple[str, str], Tuple[int, str]] = dict()



    def find_accessible_keys(self,
                             node: Tuple[int, int],
                             keys: str) -> Iterator[KeySteps]:

        border_nodes = [node]
        keys_returned = set()
        visited = set(border_nodes)

        steps = 0
        while len(border_nodes) > 0:
            steps += 1
            #print('step', steps)
            for i in range(0, len(border_nodes)):

                bt = border_nodes.pop(0)
                nodes = [(bt[0], bt[1]-1),
                         (bt[0], bt[1]+1),
                         (bt[0]-1, bt[1]),
                         (bt[0]+1, bt[1])]
                for n in nodes:
                    #print('Checking', n)
                    #track visited
                    if n in visited:
                        continue
                    visited.add(n)

                    #get tile
                    tile = self.vault_map[n[1]][n[0]]

                    #wall
                    if tile == '#':
                        continue
                    #open space, new border
                    if tile == '.' or tile == '@':
                        border_nodes.append(n)
                        continue

                    # not an upper or lower case letter?!?
                    if not tile.isalpha():
                        raise Exception(f'Unexpected tile {tile}!')

                    #key
                    if tile.islower():
                        #key returned already
                        if tile in keys_returned:
                            continue
                        #key already acquired => border
                        if tile in keys:
                            border_nodes.append(n)
                            continue

                        # return key and track
                        yield KeySteps(key = tile, destination = n, steps = steps)
                        keys_returned.add(tile)
                        continue

                    #door
                    key_needed = tile.lower()
                    # if we have the key we open the door, new border
                    if key_needed in keys:
                        border_nodes.append(n)

    def get_char_at(self,
                    coords: Tuple[int, int]) -> str:
        return self.vault_map[coords[1]][coords[0]]

    def reset_steps_run(self):
        self.min_steps_so_far = 99999999999999
        self.min_path = ''
        self.executions = 0

    def get_steps_to_clear_keys_from(self,
                                         nodes: List[Tuple[int, int]] = None,
                                         collected_keys: str = ''
                                         ) -> Tuple[int, str]:
        if nodes is None:
            nodes = self.entrance_nodes

        if len(collected_keys) == self.key_count:
            # nothing to consider
            return (0, '')

        keys_in_bag = ''.join(sorted(collected_keys))

        min_steps = 99999999999999999
        min_path = None

        for i in range(0, len(nodes)):
            node = nodes[i]
            for key_step in self.find_accessible_keys(node, collected_keys):

                new_keys = collected_keys+key_step.key

                new_nodes = nodes[0:i] + [key_step.destination] + nodes[i+1:len(nodes)]
                node_keys = ''.join([self.get_char_at(c) for c in new_nodes])

                dict_key = (keys_in_bag, node_keys)

                if dict_key in self.steps_cache:
                    #print('got', dict_key, 'from cache')
                    (sub_steps, sub_path) = self.steps_cache[dict_key]
                else:
                    self.executions += 1
                    (sub_steps, sub_path) = self.get_steps_to_clear_keys_from(
                            nodes=new_nodes,
                            collected_keys=new_keys)
                    self.steps_cache[dict_key] = (sub_steps, sub_path)

                    if self.executions % 1000 == 0:
                        print('calc', self.executions, 'calculated', dict_key, 'to be', (sub_steps, sub_path))

                steps = key_step.steps + sub_steps
                path = key_step.key + sub_path

                if steps < min_steps:
                    min_steps = steps
                    min_path = path


        return (min_steps, min_path)


if not 'answer_1' in locals():

    with open("inputs/day18.txt", "r") as f:
        inp = f.read()

    v = Vault(inp)

    (steps, path) = v.get_steps_to_clear_keys_from()

    answer_1 = steps
    print('answer_1', answer_1)

with open("inputs/day18-2.txt", "r") as f:
    inp = f.read()

v = Vault(inp)

(steps, path) = v.get_steps_to_clear_keys_from()

answer_2 = steps
print('answer_2', answer_2)


if __name__ == "__main__":

    import unittest

    class TestAll(unittest.TestCase):

        def test_1(self):
            v = Vault("""#########
#b.A.@.a#
#########""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 8)

        def test_2(self):
            v = Vault("""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 86)

        def test_3(self):
            v = Vault("""########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 132)

        def test_4(self):
            v = Vault("""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 136)

        def test_5(self):
            v = Vault("""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 81)

        def test_2_1(self):
            v = Vault("""#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#.b#
#######""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 8)

        def test_2_2(self):
            v = Vault("""###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 24)


        def test_2_3(self):
            v = Vault("""#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 32)

        def test_2_4(self):
            v = Vault("""#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""")

            (steps, path) = v.get_steps_to_clear_keys_from()
            self.assertEqual(steps, 72)

        unittest.main()
