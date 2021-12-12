# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 12.

Created on Sun Dec 12 20:24:17 2021

@author: Eftychios
"""

import os

from typing import List

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

inp_string = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

inp_string = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

with open("inputs/day-12.txt", "r") as f:
    inp_string = f.read()


class Node:
    """Node representation."""

    def __init__(self, name: str):
        self.name = name
        self.connected = list()
        self.is_small = True

        h = 0
        for i, ch in enumerate(self.name):
            h = h + i * 256 + ord(ch)
            if self.is_small and ch == ch.upper():
                self.is_small = False

        self.hash = h

    def __hash__(self) -> str:
        """Make hashable."""
        return self.hash

    def __eq__(self, other):
        """Make equatable."""
        return self.hash == other.hash

    def __repr__(self) -> str:
        """Human friendly representation."""
        return f'Node {self.name}'

    def get_paths_to_end(self, path_so_far: List):
        """Get all paths to end."""
        # small and already visited, no progress
        if self.is_small and self in path_so_far:
            return

        # We copy the list here
        p = list(path_so_far)
        p.append(self)
        if self.name == 'end':
            yield p
            return

        for conn in self.connected:
            for pp in conn.get_paths_to_end(p):
                yield pp

    def get_paths_to_end2(self, path_so_far: List, visited_twice: bool):
        """Get all paths to end."""
        # small and already visited
        if self.is_small and self in path_so_far:
            # no progress if we have already visited twice something, or start
            if visited_twice or self.name == 'start':
                return

            visited_twice = True

        # We copy the list here
        p = list(path_so_far)
        p.append(self)
        if self.name == 'end':
            yield (p, visited_twice)
            return

        for conn in self.connected:
            for pp in conn.get_paths_to_end2(p, visited_twice):
                yield (pp, visited_twice)


nodes = dict()

for conn in inp_string.split('\n'):
    p = conn.split('-')
    if p[0] not in nodes:
        nodes[p[0]] = Node(p[0])
    if p[1] not in nodes:
        nodes[p[1]] = Node(p[1])

    nodes[p[0]].connected.append(nodes[p[1]])
    nodes[p[1]].connected.append(nodes[p[0]])


paths = 0
for p in nodes['start'].get_paths_to_end([]):
    paths = paths + 1

print('Answer 1:', paths)


paths = 0
for p in nodes['start'].get_paths_to_end2([], False):
    paths = paths + 1

print('Answer 2:', paths)
