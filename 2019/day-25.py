# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 11:00:10 2020

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List, NamedTuple
import numpy as np
import threading

os.chdir("C:/Repos/advent-of-code-python/2019")


from intcode_runner import IntcodeRunner

with open("inputs/day25.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]


class AsciiInputGenerator:
    def __init__(self):
        self.inputs = []
        self.next_idx = 0


    def input_iter(self) -> Iterator[int]:

        while True:
            while self.next_idx < len(self.inputs):
                yield self.inputs[self.next_idx]
                self.next_idx += 1

            time.sleep(1)

    def get_input_loop(self):

        while True:
            inp = input("Please enter program text input: ")
            if inp == "quit":
                print('Quitting input loop')
                return

            for ch in inp:
                self.inputs.append(ord(ch))

            self.inputs.append(10)

aig = AsciiInputGenerator()

stop_runner = False

def ascii_runner():
    runner = IntcodeRunner(inp, extend=10000, input_iterator=aig.input_iter())
    row = ''
    for b in runner.iter_run():
        global stop_runner
        if stop_runner:
            print('quitting runner loop')
            return
        if b == 10:
            if row != '':
                print(row)
                row = ''
            continue

        if b > 255:
            break
        row += chr(b)

    print('Execution stopped!')

thread = threading.Thread(target=ascii_runner)
thread.start()

aig.get_input_loop()
#stop_runner = True

#cake mug monolith coin
#19013632
