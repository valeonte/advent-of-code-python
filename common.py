"""
Shared helper data objects.

Created on Sat Dec 07 2024 8:15:56 AM

@author: Eftychios
"""

from enum import Enum
from typing import Iterable, Tuple

class Dir(Enum):
    N = 0
    NW = 1
    W = 2
    SW = 3
    S = 4
    SE = 5
    E = 6
    NE = 7

    def next_clockwise(self, steps: int = 1) -> 'Dir':
        new_d = (self.value + steps) % 8
        return Dir(new_d)
        

def get_neighbours(x: int, y: int) -> Iterable[Tuple[int, int]]:
    yield x-1, y
    yield x+1, y
    yield x, y-1
    yield x, y+1


if __name__ == "__main__":

    d = Dir.NW
    for i in range(-10, 10):
        print(d.next_clockwise(i))
