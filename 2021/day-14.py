# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 14.

Created on Tue Dec 14 09:31:06 2021

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

with open("inputs/day-14.txt", "r") as f:
    inp_string = f.read()

alphabet = dict()
poly = None
rules = dict()
for row in inp_string.split('\n'):
    if poly is None:
        poly = row
        continue

    p = row.split(' -> ')
    if len(p) != 2:
        continue

    rules[p[0]] = p[1]
    if p[1] not in alphabet:
        alphabet[p[1]] = 0
    alphabet[p[1]] = alphabet[p[1]] + 1

orig_poly = poly

print(poly)
for i in range(10):
    new_poly = ''
    for j in range(len(poly) - 1):
        pair = poly[j:j + 2]
        new_poly = new_poly + pair[0]
        if pair in rules:
            new_poly = new_poly + rules[pair]

    poly = new_poly + poly[-1]
    print('Step', i + 1, ' -> length', len(poly))

counter = dict()
for ch in poly:
    if ch not in counter:
        counter[ch] = 0
    counter[ch] = counter[ch] + 1

max_count = max(counter.values())
min_count = min(counter.values())
print('Answer 1:', max_count - min_count)


cache = dict()


def count_chars(pair: str, cur_iter: int, max_iters: int):
    """Count characters of pair recursively."""
    if cur_iter >= max_iters:
        if pair[0] == pair[1]:
            return {pair[0]: 2}

        return {pair[0]: 1, pair[1]: 1}

    global cache

    key = (pair, cur_iter)
    if key in cache:
        return cache[key].copy()

    cur_iter = cur_iter + 1
    ch = rules[pair]

    cnt1 = count_chars(pair[0] + ch, cur_iter, max_iters)
    cnt2 = count_chars(ch + pair[1], cur_iter, max_iters)
    # reduce the common character by 1
    for k, v in cnt1.items():
        if k in cnt2:
            cnt2[k] = cnt2[k] + v
        else:
            cnt2[k] = v

    cnt2[ch] = cnt2[ch] - 1
    cache[key] = cnt2.copy()

    return cnt2


poly = orig_poly
print(poly)
cnts = []
for j in range(len(poly) - 1):
    pair = poly[j:j + 2]

    cnt = count_chars(pair, 0, 40)
    if j > 0:
        # avoid double counting middle char
        cnt[pair[0]] = cnt[pair[0]] - 1

    cnts.append(cnt)
    print(cnt)


counter = None
for cnt in cnts:
    if counter is None:
        counter = cnt
        continue
    for k, v in cnt.items():
        if k in counter:
            counter[k] = counter[k] + v
        else:
            counter[k] = v

max_count = max(counter.values())
min_count = min(counter.values())
print('Answer 2:', max_count - min_count)
