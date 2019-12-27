# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:18:29 2019

@author: Eftychios
"""

import os
from typing import Iterator, Tuple, Dict

os.chdir("C:/Repos/advent-of-code-python/2019")


class Maze:
    def __init__(self,
                 maze_map: str):

        self.maze_map = maze_map.splitlines()
        self.portals = list(self.find_portal_nodes())
        self.portal_lookup = {(p[1], p[2]): p[0] for p in self.portals}
        self.height = len(self.maze_map)
        self.width = max([len(line) for line in self.maze_map])

        self.portal_map: Dict[Tuple[int, int], Tuple[int, int]] = dict()

        portal_cache = dict()
        for portal in self.portals:
            node = (portal[1], portal[2])
            if portal[0] == 'AA':
                self.entrance = node
            elif portal[0] == 'ZZ':
                self.exit = node
            elif portal[0] in portal_cache:
                self.portal_map[portal_cache[portal[0]]] = node
                self.portal_map[node] = portal_cache[portal[0]]
            else:
                portal_cache[portal[0]] = node

    def find_portal_nodes(self) -> Iterator[Tuple[str, int, int]]:

        visited = set()
        for y, line in enumerate(self.maze_map):
            for x, ch in enumerate(line):
                if (x, y) in visited:
                    continue
                visited.add((x, y))

                if ch < 'A' or ch > 'Z':
                    continue

                # checking in row
                if (len(line) > x + 1 and
                        line[x + 1] >= 'A' and
                        line[x + 1] <= 'Z'):
                    visited.add((x + 1, y))
                    portal = ch + line[x + 1]
                    if x > 0 and line[x - 1] == '.':
                        yield (portal, x - 1, y)
                    else:
                        yield (portal, x + 2, y)

                    continue

                # has to be in col
                portal = ch + self.maze_map[y+1][x]
                visited.add((x, y+1))
                if y > 0 and self.maze_map[y-1][x] == '.':
                    yield (portal, x, y-1)
                else:
                    yield (portal, x, y+2)

    def find_steps_to_exit(self):

        border_nodes = [self.entrance]
        visited = set(border_nodes)

        steps = 0
        while len(border_nodes) > 0:
            steps += 1

            for i in range(len(border_nodes)):

                bt = border_nodes.pop(0)
                nodes = [(bt[0], bt[1]-1),
                         (bt[0], bt[1]+1),
                         (bt[0]-1, bt[1]),
                         (bt[0]+1, bt[1])]

                if bt in self.portal_map:
                    nodes.append(self.portal_map[bt])

                for n in nodes:
                    if n in visited:
                        continue
                    visited.add(n)

                    if n == self.exit:
                        # job done
                        return steps

                    tile = self.maze_map[n[1]][n[0]]

                    # space
                    if tile == '.':
                        border_nodes.append(n)

        raise Exception("path to exit not found!")

    def is_outer_portal(self, node: Tuple[int, int]) -> bool:

        return (node[0] == 2 or node[1] == 2 or
                node[0] == self.width-3 or node[1] == self.height-3)

    def find_steps_to_exit_recursive(self):

        # we append the "level" to the tuple, as the same tile in different
        # level is essentially different tile
        border_nodes = [(self.entrance[0], self.entrance[1], 0)]
        visited = set(border_nodes)

        steps = 0
        while len(border_nodes) > 0:
            steps += 1

            for i in range(len(border_nodes)):

                bt = border_nodes.pop(0)
                nodes = [(bt[0], bt[1]-1, bt[2]),
                         (bt[0], bt[1]+1, bt[2]),
                         (bt[0]-1, bt[1], bt[2]),
                         (bt[0]+1, bt[1], bt[2])]

                plain_node = (bt[0], bt[1])

                if plain_node in self.portal_map:
                    if self.is_outer_portal(plain_node):
                        new_level = bt[2]-1
                    else:
                        new_level = bt[2]+1

                    tele_node = self.portal_map[plain_node]
                    extra_node = (tele_node[0], tele_node[1], new_level)
                    if new_level >= 0 and extra_node not in visited:
                        nodes.append(extra_node)

                for n in nodes:
                    if n in visited:
                        continue
                    visited.add(n)

                    if n[2] == 0 and (n[0], n[1]) == self.exit:
                        # job done
                        return steps

                    tile = self.maze_map[n[1]][n[0]]

                    # space
                    if tile == '.':
                        border_nodes.append(n)

        raise Exception("path to exit not found!")


with open("inputs/day20.txt", "r") as f:
    inp = f.read()

m = Maze(inp)
answer_1 = m.find_steps_to_exit()

print('answer_1', answer_1)

answer_2 = m.find_steps_to_exit_recursive()

print('answer_2', answer_2)


if __name__ == "__main__":

    import unittest

    class TestAll(unittest.TestCase):

        def test_1(self):
            m = Maze("""         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z      """)

            self.assertEqual(m.find_steps_to_exit(), 23)
            self.assertEqual(m.find_steps_to_exit_recursive(), 26)

        def test_2(self):
            m = Maze("""                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P               """)

            self.assertEqual(m.find_steps_to_exit(), 58)

        def test_2_2(self):
            m = Maze("""             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M                     """)

            self.assertEqual(m.find_steps_to_exit_recursive(), 396)



    unittest.main()

