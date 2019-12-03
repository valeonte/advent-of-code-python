# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:29:11 2019

@author: Eftychios
"""
import os
from typing import List, Callable

os.chdir("C:/Repos/advent-of-code-python")


class IntcodeRunner:
    def __init__(self, program: List[int]):
        self.program = program
        
    def operation(self, op_address: int, op: Callable[[int, int], int]) -> None:
        address1 = self.program[op_address + 1]
        address2 = self.program[op_address + 2]
        target_address = self.program[op_address + 3]
        
        self.program[target_address] = op(self.program[address1],
                    self.program[address2])
        
    def run(self):
        
        i = 0
        while True:
            op = self.program[i]
            
            # exit
            if op == 99:
                return
            
            # addition
            if op == 1:
                self.operation(i, lambda x, y: x + y)
            elif op == 2:
                self.operation(i, lambda x, y: x * y)
            else:
                raise Exception(f'Unrecognized operation {op}!')
            
            i += 4

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


if __name__ == "__main__":
    
    import unittest
    
    class TestAll(unittest.TestCase):
        
        def test_example_1(self):
            runner = IntcodeRunner([1,9,10,3,2,3,11,0,99,30,40,50])
            runner.run()
            
            self.assertListEqual(runner.program, [3500,9,10,70,2,3,11,0,99,30,40,50])
            
        def test_example_2(self):
            runner = IntcodeRunner([1,0,0,0,99])
            runner.run()
            
            self.assertListEqual(runner.program, [2,0,0,0,99])

        def test_example_3(self):
            runner = IntcodeRunner([2,3,0,3,99])
            runner.run()
            
            self.assertListEqual(runner.program, [2,3,0,6,99])

        def test_example_4(self):
            runner = IntcodeRunner([2,4,4,5,99,0])
            runner.run()
            
            self.assertListEqual(runner.program, [2,4,4,5,99,9801])

        def test_example_5(self):
            runner = IntcodeRunner([1,1,1,4,99,5,6,0,99])
            runner.run()
            
            self.assertListEqual(runner.program, [30,1,1,4,2,5,6,0,99])

    unittest.main()