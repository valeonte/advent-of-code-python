# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 09:19:15 2019

@author: Eftychios
"""

import os
os.chdir("C:/Repos/advent-of-code-python")
import sys
sys.path.insert(1, "C:/Repos/advent-of-code-python/2019")

from typing import List
from itertools import permutations

from intcode_runner import IntcodeRunner

class AmplifierSet:
    def __init__(self, program: List[int]):
        self.program = program
        
    def run_phases_old(self, phases: List[int]):
        
        next_input = 0
        for phase in phases:
            
            #print(f'Running phase {phase} with input {next_input}')
            
            amplifier = IntcodeRunner(self.program.copy(),
                                      [phase,
                                       next_input])
            
            next_input = amplifier.run()[-1]
            
        return next_input
    
    def run_phases(self, phases: List[int]):
        
        next_input = 0
        amplifiers = [IntcodeRunner(self.program.copy(), [phase])
                      for phase in phases]
        
        iterators = [a.iter_run() for a in amplifiers]
        
        step = 0
        total = len(phases)
        while True:
            
            idx = step % total
            step += 1
            
            amplifier = amplifiers[idx]
            iterator = iterators[idx]

            #print(f'Running step {step}, index {idx} with input {next_input}')
            
            amplifier.inputs.append(next_input)
            
            try:
                next_input = next(iterator)
            except StopIteration:
                return next_input

            
        return next_input


with open("2019/inputs/day7.txt", "r") as f:
    inputs = f.read()

raw_program = [int(stritem) for stritem in inputs.split(",")]
a = AmplifierSet(raw_program)

max_output = 0
for perm in permutations(range(0, 5)):
    
    output = a.run_phases(perm)
    #print(f"Phases {perm} got output {output}")
    if output > max_output:
        max_output = output

answer_1 = max_output

max_output = 0
for perm in permutations(range(5, 10)):
    
    output = a.run_phases(perm)
    #print(f"Phases {perm} got output {output}")
    if output > max_output:
        max_output = output

answer_2 = max_output
print(answer_1, answer_2)
#70597 30872528



if __name__ == "__main__":
    
    import unittest
    
    class TestAll(unittest.TestCase):
        
        def test_1(self):
            a = AmplifierSet([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
            result = a.run_phases([4,3,2,1,0])
            
            self.assertEqual(result, 43210)

        def test_2(self):
            a = AmplifierSet([3,23,3,24,1002,24,10,24,1002,23,-1,23,
                              101,5,23,23,1,24,23,23,4,23,99,0,0])
            result = a.run_phases([0,1,2,3,4])
            
            self.assertEqual(result, 54321)

        def test_3(self):
            a = AmplifierSet([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                              1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
            result = a.run_phases([1,0,4,3,2])
            
            self.assertEqual(result, 65210)
            
        def test_4(self):
            a = AmplifierSet([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                              27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
            result = a.run_phases([9,8,7,6,5])
            
            self.assertEqual(result, 139629729)

        def test_5(self):
            a = AmplifierSet([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                              -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                              53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
            result = a.run_phases([9,7,8,5,6])
            
            self.assertEqual(result, 18216)

    unittest.main()
