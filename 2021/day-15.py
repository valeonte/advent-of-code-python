# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 15.

Created on Wed Dec 15 10:44:04 2021

@author: Eftychios
"""

import os

import numpy as np

from typing import Iterator, Set, Tuple


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

with open("inputs/day-15.txt", "r") as f:
    inp_string = f.read()

inp = np.array([[int(s) for s in list(ss)]
                for ss in inp_string.split("\n")])


def neighbours(x: int, y: int, max_x: int, max_y: int
               ) -> Iterator[Tuple[int, int]]:
    """Return all valid neighbours of node x, y."""
    if x < max_x:
        yield x + 1, y
    if y < max_y:
        yield x, y + 1
    if x > 0:
        yield x - 1, y
    if y > 0:
        yield x, y - 1


def print_path(inp: np.array, visited: Set[Tuple[int, int]], x: int, y: int):
    """Print the current path to the screen, along with cheapest costs."""
    dim, _ = inp.shape
    if dim > 10:
        return
    pinp = inp.copy()
    for v in visited:
        pinp[v] = 0
    pinp[x, y] = -1
    print(pinp)


# OBSOLETE, worked well for answer 1
def get_best_path_from(inp: np.array,
                       cheapest: np.array,
                       x: int,
                       y: int,
                       visited: Set[Tuple[int, int]],
                       cost_so_far: int = 0,
                       best_so_far: int = 1e10) -> int:
    """Return the best path to end from node x, y, respecting visited."""
    if cost_so_far >= cheapest[x, y]:
        # We exceeded the cheapest cost to node, no point in continuing
        # print('Exceeded cheapest', cheapest[x, y], (x, y),
        #       cost_so_far, best_so_far)
        # print_path(visited, x, y)
        return best_so_far
    else:
        cheapest[x, y] = cost_so_far

    if cost_so_far >= best_so_far:
        # We exceeded best so far, no point in continuing
        # print('Exceeded best', cheapest[x, y], (x, y),
        #       cost_so_far, best_so_far)
        # print_path(visited, x, y)
        return best_so_far

    max_x, max_y = inp.shape
    if x == max_x - 1 and y == max_y - 1:
        # We reached final node, job done!
        if cost_so_far < best_so_far:
            print('New best!', cheapest[x, y], (x, y),
                  cost_so_far, best_so_far)
        else:
            print('Final node!', cheapest[x, y], (x, y),
                  cost_so_far, best_so_far)

#        print_path(visited, x, y)
        return cost_so_far

    v = visited.copy()
    v.add((x, y))

    for n in neighbours(x, y, max_x - 1, max_y - 1):
        if n in visited:
            # already visited, skip
            continue
        node_best = get_best_path_from(inp, cheapest, n[0], n[1], v,
                                       cost_so_far + inp[n],
                                       best_so_far)
        if node_best < best_so_far:
            best_so_far = node_best

    return best_so_far


# Initialising cheapest
def init_cheapest(inp: np.array) -> np.array:
    """Init cheapest for inp."""
    changes_made = 1
    cheapest = np.nan * np.ones(inp.shape)
    it = 0
    max_x, max_y = inp.shape
    max_x = max_x - 1
    max_y = max_y - 1
    while changes_made > 0:
        changes_made = 0
        for x in range(inp.shape[0]):
            for y in range(inp.shape[1]):
                if x == 0 and y == 0:
                    cheapest[x, y] = 0
                    continue

                node_cheapest = cheapest[x, y]
                change_made = False
                for n in neighbours(x, y, max_x, max_y):
                    if np.isnan(cheapest[n]):
                        continue
                    cur = cheapest[n] + inp[x, y]
                    if np.isnan(node_cheapest) or cur < node_cheapest:
                        change_made = True
                        node_cheapest = cur

                if change_made:
                    cheapest[x, y] = node_cheapest
                    changes_made = changes_made + 1

        it = it + 1
        print('Iteration', it, '- Changes made:', changes_made,
              '- Best:', cheapest[-1, -1])

    return cheapest


cheapest = init_cheapest(inp)
best_so_far = cheapest[-1, -1]
print('Answer 1:', get_best_path_from(inp, cheapest,
                                      0, 0, set(), best_so_far=best_so_far))


# Building new 5 times matrix
max_x, max_y = inp.shape
new_inp = np.nan * np.ones((5 * max_x, 5 * max_y))

for x in range(5):
    for y in range(5):
        tmp = inp + x + y
        while (tmp > 9).any():
            tmp[tmp > 9] = tmp[tmp > 9] - 9

        new_inp[x * max_x: (x + 1) * max_x,
                y * max_y: (y + 1) * max_y] = tmp


new_cheapest = init_cheapest(new_inp)
best_so_far = new_cheapest[-1, -1]

print('Answer 2:', get_best_path_from(new_inp, new_cheapest,
                                      0, 0, set(), best_so_far=best_so_far))
