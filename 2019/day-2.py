# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:29:11 2019

@author: Eftychios
"""
import os
os.chdir("C:/Repos/advent-of-code-python")

import sys
sys.path.insert(1, "C:/Repos/advent-of-code-python/2019")

from intcode_runner import IntcodeRunner


with open("2019/inputs/day2.txt", "r") as f:
    inputs = f.read()

raw_program = [int(stritem) for stritem in inputs.split(",")]
input_program = list(raw_program)
input_program[1] = 12
input_program[2] = 2
runner = IntcodeRunner(input_program)
runner.run()
answer_1 = runner.program[0]

result = None
for noun in range(0, 100):
    for verb in range(0, 100):
        input_program = list(raw_program)
        input_program[1] = noun
        input_program[2] = verb

        runner = IntcodeRunner(input_program)
        runner.run()
        result = runner.program[0]
        
        if result == 19690720:
            break

    if result == 19690720:
            break

answer_2 = 100*noun + verb

print(answer_1, answer_2)        
#2890696 8226
