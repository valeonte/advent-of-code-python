# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 17:51:41 2020

@author: Eftychios
"""

import os
import time
import math
import re

from typing import Dict, List, Tuple
from dataclasses import dataclass


os.chdir("C:/Repos/advent-of-code-python/2017")

with open("inputs/day25.txt", "r") as f:
    inp = f.read()


@dataclass
class StateMove:
    write_one: bool
    idx_increment: int = 0
    next_state: int = 0


class Turing:
    def __init__(self, inp: str, start_state: str):
        self.ones = set()
        self.idx = 0
        self.state = 0
        self.state_dict = dict()
        self.max_steps = 0
        self.process_input(inp)

    def process_input(self, inp: str):
        cur_state = 0
        cur_value = False
        cur_state_move = None
        ret = dict()
        for line in inp.split('\n'):
            r = re.search('Begin in state (\\w)\\.', line)
            if r:
                self.state = ord(r.group(1))
                print('Got start state', r.group(1), self.state)
                continue

            r = re.search('Perform a diagnostic checksum after (\\d+) steps.',
                          line)
            if r:
                self.max_steps = int(r.group(1))
                print('Got max steps', r.group(1), self.max_steps)
                continue

            r = re.search('In state (\\w)\\:', line)
            if r:
                cur_state = ord(r.group(1))
                print('Got new state', r.group(1), cur_state)
                continue

            r = re.search('If the current value is (\\d)\\:', line)
            if r:
                cur_value = r.group(1) == '1'
                print('Got if line', r.group(1), cur_value)
                continue

            r = re.search('Write the value (\\d)\\.', line)
            if r:
                cur_state_move = StateMove(r.group(1) == '1')
                print('Got write value', r.group(1), cur_state_move)
                continue

            r = re.search('Move one slot to the (right|left)\\.', line)
            if r:
                if r.group(1) == 'right':
                    cur_state_move.idx_increment = 1
                else:
                    cur_state_move.idx_increment = -1
                print('Got move', r.group(1), cur_state_move)
                continue

            r = re.search('Continue with state (\\w)\\.', line)
            if r:
                cur_state_move.next_state = ord(r.group(1))
                print('Got next state', r.group(1), cur_state_move)
                print('Saving', cur_state, cur_value, cur_state_move)
                if cur_state not in ret:
                    ret[cur_state] = dict()
                ret[cur_state][cur_value] = cur_state_move

        self.state_dict = ret

    def run_step(self):
        cur_value = self.idx in self.ones
        next_move = self.state_dict[self.state][cur_value]
        if next_move.write_one:
            self.ones.add(self.idx)
        else:
            if cur_value:
                self.ones.remove(self.idx)

        self.idx += next_move.idx_increment
        self.state = next_move.next_state

    def run_max_steps(self):
        for i in range(0, self.max_steps):
            self.run_step()

    def print_status(self):
        print('State:', chr(self.state))
        checksum = len(self.ones)
        print('Checksum:', checksum)
        if checksum == 0:
            min_idx = -3
            max_idx = 4
        else:
            min_idx = min(self.ones) - 3
            max_idx = max(self.ones) + 4

        p = ''
        for i in range(min_idx, max_idx):
            val = int(i in self.ones)
            if i == self.idx:
                p += f'[{val}]'
            else:
                p += f' {val} '

        print(p)


inpa = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

t = Turing(inp, 'A')
t.run_max_steps()
t.print_status()
max(t.ones)
