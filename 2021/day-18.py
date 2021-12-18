# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 18.

Created on Sat Dec 18 08:42:46 2021

@author: Eftychios
"""

import os
import math
import copy

os.chdir("C:/Repos/advent-of-code-python/2021")


inp_string = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""


inp_string = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


with open("inputs/day-18.txt", "r") as f:
    inp_string = f.read()


def add(pair1: list, pair2: list):
    """Add two pairs."""
    ret = [pair1, pair2]

    return reduce(ret)


def reduce(pair: list):
    """Reduce pair all the way."""
    def add_num_left(num: int):
        for i in list(range(len(pair_stack) - 1, -1, -1)):
            idx = idx_stack[i]
            if idx == 0:
                continue
            parent = pair_stack[i]
            if type(parent[0]) is int:
                parent[0] = parent[0] + num
                return

            parent = parent[0]
            while type(parent[1]) is list:
                parent = parent[1]

            # here parent[1] should be num
            parent[1] = parent[1] + num
            return

    def add_num_right(num: int):
        for i in list(range(len(pair_stack) - 1, -1, -1)):
            idx = idx_stack[i]
            if idx == 1:
                continue
            parent = pair_stack[i]
            if type(parent[1]) is int:
                parent[1] = parent[1] + num
                return

            parent = parent[1]
            while type(parent[0]) is list:
                parent = parent[0]

            # here parent[0] should be num
            parent[0] = parent[0] + num
            return

    pair_stack = []
    idx_stack = []
    cur_pair = pair

    # First rule no 1
    while True:
        if type(cur_pair) is list:
            if len(idx_stack) == 4:
                add_num_left(cur_pair[0])
                add_num_right(cur_pair[1])

                parent = pair_stack[-1]
                idx = idx_stack[-1]
                parent[idx] = 0
                cur_pair = 0

                continue

            pair_stack.append(cur_pair)
            idx_stack.append(0)
            cur_pair = cur_pair[0]
        else:
            while True:
                if len(idx_stack) == 0:
                    break  # done!

                parent_idx = idx_stack.pop()
                parent = pair_stack.pop()
                if parent_idx == 1:
                    continue

                idx_stack.append(1)
                pair_stack.append(parent)
                cur_pair = parent[1]
                break

            if len(idx_stack) == 0:
                break  # done!

    pair_stack = []
    idx_stack = []
    cur_pair = pair

    # Then rule no 2
    while True:
        if type(cur_pair) is list:
            pair_stack.append(cur_pair)
            idx_stack.append(0)
            cur_pair = cur_pair[0]
        else:
            if cur_pair > 9:
                cur_pair = [math.floor(cur_pair/2), math.ceil(cur_pair/2)]
                parent = pair_stack[-1]
                idx = idx_stack[-1]
                parent[idx] = cur_pair

                return reduce(pair)  # done 1 split, restart

            while True:
                if len(idx_stack) == 0:
                    return pair  # done!

                parent_idx = idx_stack.pop()
                parent = pair_stack.pop()
                if parent_idx == 1:
                    continue

                idx_stack.append(1)
                pair_stack.append(parent)
                cur_pair = parent[1]
                break

    raise Exception('???')


def calc_magnitude(pair):
    """Calculate pair's magnitude."""
    if type(pair) is list:
        return 3 * calc_magnitude(pair[0]) + 2 * calc_magnitude(pair[1])
    else:
        return pair


reduce([[[[[9,8],9],13],3],4])
reduce([7,[6,[5,[4,[3,2]]]]])
reduce([[6,[5,[4,[3,2]]]],1])
reduce([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1])


res = None
for row in inp_string.split('\n'):
    pair = eval(row)
    if res is None:
        res = pair
    else:
        res = add(res, pair)
        print(str(res).replace(' ', ''))

calc_magnitude([[9,1],[1,9]])
calc_magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])

print('Answer 1:', calc_magnitude(res))


pairs = [eval(row) for row in inp_string.split('\n')]
max_mag = 0
for i in range(len(pairs)):
    for j in range(len(pairs)):
        if i == j:
            continue
        pair1 = copy.deepcopy(pairs[i])
        pair2 = copy.deepcopy(pairs[j])
        mag = calc_magnitude(add(pair1, pair2))
        if mag > max_mag:
            max_mag = mag
            print('New max magnitude!', max_mag)

print('Answer 2:', max_mag)

