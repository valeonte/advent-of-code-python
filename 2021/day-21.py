# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 21.

Created on Tue Dec 21 08:22:38 2021

@author: Eftychios
"""

from typing import Iterator
from dataclasses import dataclass


start1 = 4
start2 = 8

start1 = 2
start2 = 7

last_die_roll = 0
rolls = 0


def get_new_pos(pos: int, roll: int) -> int:
    """Get the new position following a roll."""
    return (pos - 1 + roll) % 10 + 1


def roll_die(times: int) -> Iterator[int]:
    """Roll the die as many times."""
    global last_die_roll, rolls

    for _ in range(times):
        die = last_die_roll + 1
        if die > 100:
            die = 1

        last_die_roll = die
        rolls = rolls + 1
        yield die


score1 = 0
score2 = 0
pos1 = start1
pos2 = start2

while score1 < 1000 and score2 < 1000:
    roll1 = sum(roll_die(3))
    pos1 = get_new_pos(pos1, roll1)
    score1 = score1 + pos1
    if score1 >= 1000:
        break

    roll2 = sum(roll_die(3))
    pos2 = get_new_pos(pos2, roll2)
    score2 = score2 + pos2

print('Answer 1:', min(score1, score2) * rolls)


@dataclass
class EnvironmentState:
    """Keeps the environment state."""

    score1: int
    pos1: int

    score2: int
    pos2: int

    def __hash__(self) -> str:
        """Make hashable."""
        return self.score1 * 10000 + self.score2 * 100 + \
            (self.pos1 - 1) * 10 + self.pos2 - 1


# Potential sums on a turn / roll of 3 dice
roll_sums = {k: 0 for k in range(3, 10)}
for i in range(3):
    for j in range(3):
        for k in range(3):
            sm = i + j + k + 3
            roll_sums[sm] = roll_sums[sm] + 1


envs = {EnvironmentState(0, start1, 0, start2): 1}
envs_won_1 = 0
envs_won_2 = 0

iteration = 0
while len(envs) > 0:
    iteration = iteration + 1
    print('Iteration', iteration, '-', len(envs), 'distinct environments')
    cur_items = list(envs.items())
    envs = dict()
    for env, cnt in cur_items:
        # Player 1 rolls
        for roll_sum1, sum_count1 in roll_sums.items():
            new_pos1 = get_new_pos(env.pos1, roll_sum1)
            new_score1 = env.score1 + new_pos1
            if new_score1 >= 21:
                # Player 1 won the environment
                envs_won_1 = envs_won_1 + sum_count1 * cnt
                # No point in doing player 2's roll
                continue

            for roll_sum2, sum_count2 in roll_sums.items():
                # the actual number of environments in this state
                inc = cnt * sum_count1 * sum_count2

                new_pos2 = get_new_pos(env.pos2, roll_sum2)
                new_score2 = env.score2 + new_pos2
                if new_score2 >= 21:
                    # Player 1 won the environment
                    envs_won_2 = envs_won_2 + inc
                    # Environment got winner, continuing
                    continue

                # Add the environment for next iteration
                new_env = EnvironmentState(new_score1, new_pos1,
                                           new_score2, new_pos2)

                if new_env in envs:
                    envs[new_env] = envs[new_env] + inc
                else:
                    envs[new_env] = inc

print('Answer 2:', max(envs_won_1, envs_won_2))
