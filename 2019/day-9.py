# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 20:16:28 2019

@author: Eftychios
"""

import os
from typing import Iterator, Tuple, Dict

from intcode_runner import IntcodeRunner


os.chdir("C:/Repos/advent-of-code-python")

with open("2019/inputs/day9.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]

runner = IntcodeRunner(inp, inputs=[1], extend=1000000)
ret = runner.run()
answer_1 = ret[0]

runner = IntcodeRunner(inp, inputs=[2], extend=1000000)
ret = runner.run()
answer_2 = ret[0]

print(answer_1, answer_2)
