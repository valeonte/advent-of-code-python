# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 17.

Created on Fri Dec 17 08:35:54 2021

@author: Eftychios
"""

from dataclasses import dataclass

target_x = (20, 30)
target_y = (-10, -5)

target_x = (201, 230)
target_y = (-99, -65)


@dataclass
class Res:
    """Result holder."""

    valid: bool
    x_short: bool
    x_long: bool
    max_height: int
    t: int


def check_valid_pair(x: int, y: int) -> Res:
    """Calculate the maximum height for x/y speed in time t."""
    cur_pos = (0, 0)
    max_height = 0
    t = 0
    # loop while before box edge
    while cur_pos[0] <= target_x[1] and cur_pos[1] >= target_y[0]:
        t = t + 1
        cur_pos = (cur_pos[0] + x, cur_pos[1] + y)
        if cur_pos[1] > max_height:
            max_height = cur_pos[1]

        if (cur_pos[0] >= target_x[0] and cur_pos[0] <= target_x[1]
                and cur_pos[1] >= target_y[0] and cur_pos[1] <= target_y[1]):
            # landed in target square, valid path
            return Res(True, False, False, max_height, t)

        if x > 0:
            x = x - 1
        elif x < 0:
            x = x + 1
        y = y - 1

    cur_x, cur_y = cur_pos
    # x is short if it is before the window when y is below it
    x_short = cur_x < target_x[0] and cur_y < target_y[0] and x == 0
    # x is long if it is after the window when y is above it
    x_long = cur_x > target_x[1] and cur_y > target_y[1]
    return Res(valid=False,
               x_short=x_short,
               x_long=x_long,
               max_height=max_height,
               t=t)


max_height = 0
cnt = 0
for x in range(target_x[1] + 1):
    y = min(target_y) - 1
    while y < -10 * min(target_y):
        y = y + 1
        res = check_valid_pair(x, y)
        if res.x_short or res.x_long:
            break
        if res.valid:
            if res.max_height > max_height:
                print('Got max height set!', x, y, res.max_height, res.t)
                max_height = res.max_height
            cnt = cnt + 1

print('Answer 1:', max_height)

print('Answer 2:', cnt)
