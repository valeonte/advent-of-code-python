"""
Advent of Code 2023 day 17.

Created on Sun Dec 17 2023 9:26:30 AM

@author: Eftychios
"""

import os
import heapq

import numpy as np

from typing import Iterator, List
from dataclasses import dataclass, replace
from enum import Enum

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

with open("inputs/day-17.txt", "r") as f:
    inp_string = f.read()


inps = inp_string.split('\n')

heat_map = np.array([[int(num) for num in line]
                     for line in inps])
#heat_map = heat_map[4:, -3:]
max_i, max_j = [h - 1 for h in heat_map.shape]


class Heading(Enum):
    N: int = 0
    E: int = 1
    S: int = 2
    W: int = 3


@dataclass(eq=True, frozen=True)
class State:
    i: int
    j: int

    heading: Heading
    same_remaining: int = 3
    min_same_left: int = 0

    def __lt__(self, other):
        return (self.i, self.j) < (other.i, other.j)

    def turn_left(self) -> 'State':
        if self.min_same_left > 0:
            return None
        new_heading = self.heading.value - 1
        if new_heading < 0:
            new_heading = Heading.W
        else:
            new_heading = Heading(new_heading)
        return replace(self, heading=new_heading, same_remaining=10, min_same_left=4)
        return replace(self, heading=new_heading, same_remaining=3)

    def turn_right(self) -> 'State':
        if self.min_same_left > 0:
            return None
        new_heading = self.heading.value + 1
        if new_heading > 3:
            new_heading = Heading.N
        else:
            new_heading = Heading(new_heading)
        return replace(self, heading=new_heading, same_remaining=10, min_same_left=4)
        return replace(self, heading=new_heading, same_remaining=3)

    def move_ahead(self) -> 'State':
        if self.same_remaining == 0:
            return None
        changes = dict(same_remaining=self.same_remaining - 1,
                       min_same_left=max(0, self.min_same_left - 1))
        if self.heading == Heading.N:
            if self.i == 0:
                return None
            changes['i'] = self.i - 1
        elif self.heading == Heading.E:
            if self.j == max_j:
                return None
            changes['j'] = self.j + 1
        elif self.heading == Heading.S:
            if self.i == max_i:
                return None
            changes['i'] = self.i + 1
        elif self.heading == Heading.W:
            if self.j == 0:
                return None
            changes['j'] = self.j - 1

        return replace(self, **changes)


def get_potential_next(state: State) -> Iterator[State]:
    """Get all potential next nodes."""
    left = state.turn_left()
    right = state.turn_right()
    states = [s.move_ahead() for s in [left, right, state] if s is not None]
    return sorted([s
                   for s in states
                   if s is not None], key=lambda x: 0 if x.heading == Heading.S or x.heading == Heading.E else 1)


# Proper Dijkstra’s

# start = State(0, 0, heading=Heading.E)

# queue = []
# heapq.heappush(queue, (0, start))

# seen = set()
# while queue:
#     cost, state = heapq.heappop(queue)
#     #print(cost, state)

#     if state.i == max_i and state.j == max_j:
#         break

#     if state in seen:
#         continue

#     seen.add(state)

#     for n in get_potential_next(state):
#         new_cost = cost + heat_map[n.i, n.j]
#         heapq.heappush(queue, (new_cost, n))


# print('Answer 1:', cost)


start = State(0, 0, heading=Heading.E, same_remaining=10, min_same_left=4)

queue = []
heapq.heappush(queue, (0, start))

seen = set()
while queue:
    cost, state = heapq.heappop(queue)

    if state.i == max_i and state.j == max_j and state.min_same_left == 0:
        break

    if state in seen:
        continue

    #print(cost, state)
    seen.add(state)

    for n in get_potential_next(state):
        new_cost = cost + heat_map[n.i, n.j]
        heapq.heappush(queue, (new_cost, n))

print('Answer 2:', cost)
