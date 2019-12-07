# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 20:08:02 2019

@author: Eftychios
"""

import os
os.chdir("C:/Repos/advent-of-code-python")
import sys
sys.path.insert(1, "C:/Repos/advent-of-code-python/2019")

from intcode_runner import IntcodeRunner


with open("2019/inputs/day5.txt", "r") as f:
    inputs = f.read()

raw_program = [int(stritem) for stritem in inputs.split(",")]
runner = IntcodeRunner(raw_program, [1])
answer_1 = runner.run()[-1]

raw_program = [int(stritem) for stritem in inputs.split(",")]
runner = IntcodeRunner(raw_program, [5])
answer_2 = runner.run()[-1]

print(answer_1, answer_2)
#12428642 918655
