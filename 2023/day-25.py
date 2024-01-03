"""
Advent of Code 2023 day 25.

Created on Thu Dec 28 2023 11:20:43 PM

@author: Eftychios
"""

import os
import json
import re
import math
import logging
import random

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from itertools import combinations, pairwise
from typing import Tuple, Set, Iterator, Dict, List
from dataclasses import dataclass, replace, field
from collections import Counter
from enum import Enum
from functools import cache

logging.basicConfig(format='%(asctime)s: %(name)s|%(levelname)s|%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


with open("inputs/day-25.txt", "r") as f:
    inp_string = f.read()


inps = inp_string.split('\n')


@dataclass(frozen=True)
class Path:
    start: str
    end: str

    def contains(self, other: str) -> bool:
        return self.start == other or self.end == other
    
    def other_node(self, one_node: str) -> bool:
        if not self.contains(one_node):
            raise Exception('ee')
        return self.end if self.start == one_node else self.start

    def __eq__(self, __value: 'Path') -> bool:
        return self.start == __value.start and self.end == __value.end or self.start == __value.end and self.end == __value.start
    
    def __hash__(self) -> int:
        if self.start < self.end:
            return hash(self.start + self.end)
        return hash(self.end + self.start)


all_nodes = set()
all_edges = []

comps = dict()
for row in inps:
    key = row[:3]
    conns = row[5:].split(' ')

    all_nodes.add(key)
    for c in conns:
        all_nodes.add(c)
        all_edges.append(Path(key, c))
    comps[key] = conns

G = nx.Graph()
for n, conns in comps.items():
    for c in conns:
        G.add_edge(n, c)

nodes = list(G)

@cache
def d1(node):
    return nx.descendants_at_distance(G, node, 1)


cut_candidates = {
    frozenset((a, b))
    for (a, b) in combinations(G, 2)
    if b in d1(a) and not (d1(a) & d1(b))
}

random.choices(nodes, k=2)
list(pairwise(nx.shortest_path(G, *random.choices(nodes, k=2))))

c = Counter()
for _ in range(1000):
    for edge in pairwise(nx.shortest_path(G, *random.choices(nodes, k=2))):
        edgefs = frozenset(edge)
        if edgefs in cut_candidates:
            c[edgefs] += 1


[tuple(edgefs) for (edgefs, count) in c.most_common(3)]

G1 = G.copy()
G1.remove_edges_from(tuple(edgefs) for (edgefs, count) in c.most_common(3))
cc = list(nx.connected_components(G1))
if len(cc) == 2:
    print(len(cc[0]) * len(cc[1]))



log.info('Done?')
