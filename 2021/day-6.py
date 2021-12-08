# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 6.

Created on Tue Dec  7 15:20:24 2021

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = "3,4,3,1,2"

with open("inputs/day-6.txt", "r") as f:
    inp_string = f.read()

inp = [int(i) for i in inp_string.split(',')]

timer_count = {int(t): 0
               for t in range(9)}

for i in inp:
    timer_count[i] = timer_count[i] + 1

for i in range(80):
    new_count = dict()
    for timer, cnt in timer_count.items():
        if timer == 0:
            new_count[8] = cnt

            timer = 7

        if timer - 1 in new_count:
            new_count[timer - 1] = new_count[timer - 1] + cnt
        else:
            new_count[timer - 1] = cnt

    timer_count = new_count
#    print('After day', i + 1, '->', sum(timer_count.values()), 'fish')
    # print('\n'.join([f'{c}: {p}'
    #                  for c, p in timer_count.items()
    #                  if p > 0]))

print('Answer 1:', sum(timer_count.values()))


timer_count = {int(t): 0
               for t in range(9)}

for i in inp:
    timer_count[i] = timer_count[i] + 1

for i in range(256):
    new_count = dict()
    for timer, cnt in timer_count.items():
        if timer == 0:
            new_count[8] = cnt

            timer = 7

        if timer - 1 in new_count:
            new_count[timer - 1] = new_count[timer - 1] + cnt
        else:
            new_count[timer - 1] = cnt

    timer_count = new_count

print('Answer 2:', sum(timer_count.values()))
