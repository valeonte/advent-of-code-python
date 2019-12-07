# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 09:07:13 2019

@author: Eftychios
"""

from typing import List


class IntcodeRunner:
    def __init__(self, program: List[int], inputs: List[int] = None):
        self.program = program
        self.inputs = inputs
        self.input_counter = 0
        self.outputs = []
        
    def add(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 1:
            raise Exception("Not addition!!")
        
        x = self.get_parameter(op_address + 1, opcode % 1000 < 100)
        y = self.get_parameter(op_address + 2, opcode % 10000 < 1000)

        if opcode > 9999:
            raise Exception("Addition output in immediate mode!")
        
        self.program[self.program[op_address + 3]] = x + y
        
        return op_address + 4
        
    def get_parameter(self, addr: int, position_mode: bool) -> int:
        
        if position_mode:
            return self.program[self.program[addr]] # position mode
        
        return self.program[addr] # immediate mode
    

    def multiply(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 2:
            raise Exception("Not multiplication!!")
        
        x = self.get_parameter(op_address + 1, opcode % 1000 < 100)
        y = self.get_parameter(op_address + 2, opcode % 10000 < 1000)

        if opcode > 9999:
            raise Exception("Multiplication output in immediate mode!")
        
        self.program[self.program[op_address + 3]] = x * y

        return op_address + 4
    
    def jump_if_true(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 5:
            raise Exception("Not jump-if-true!!")
        
        x = self.get_parameter(op_address + 1, opcode % 1000 < 100)

        if x != 0:
            return self.get_parameter(op_address + 2, opcode % 10000 < 1000)
        
        return op_address + 3
    
    def jump_if_false(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 6:
            raise Exception("Not jump-if-false!!")
        
        x = self.get_parameter(op_address + 1, opcode % 1000 < 100)

        if x == 0:
            return self.get_parameter(op_address + 2, opcode % 10000 < 1000)
        
        return op_address + 3

    def less_than(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 7:
            raise Exception("Not less-than!!")
        
        x = self.get_parameter(op_address + 1, opcode % 1000 < 100)
        y = self.get_parameter(op_address + 2, opcode % 10000 < 1000)

        result = 1 if x < y else 0
        self.program[self.program[op_address + 3]] = result
        
        return op_address + 4
    
    def equals(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 8:
            raise Exception("Not equals!!")
        
        x = self.get_parameter(op_address + 1, opcode % 1000 < 100)
        y = self.get_parameter(op_address + 2, opcode % 10000 < 1000)

        result = 1 if x == y else 0
        self.program[self.program[op_address + 3]] = result
        
        return op_address + 4
    
    
    def key_input(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 3:
            raise Exception("Not input operation!!")
        
        if self.inputs is not None:
            inp = self.inputs[self.input_counter]
            #print(f'Key input at {op_address}: {inp}')
            self.input_counter += 1
        else:
            inp = input(f"Please enter program input {op_address}: ")
                
        if opcode > 99:
            raise Exception("Input operation with output in immediate mode!")
        
        self.program[self.program[op_address + 1]] = int(inp)

        return op_address + 2
    
        
    def print_output(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 4:
            raise Exception("Not output operation!!")

        output = self.get_parameter(op_address + 1, opcode % 1000 < 100)
        self.outputs.append(output)
        
        #print(f"Output {op_address}: {output}")

        return op_address + 2
    
    
    def run(self) -> List[int]:
        
        i = 0
        while True:
            op = self.program[i]
            
            #print(f"Operation {op} at {i}")
            
            opcode = op % 100
            # exit
            if opcode == 99:
                return self.outputs
            
            # addition
            if opcode == 1:
                i = self.add(i)
            elif opcode == 2:
                i = self.multiply(i)
            elif opcode == 3:
                i = self.key_input(i)
            elif opcode == 4:
                i = self.print_output(i)
            elif opcode == 5:
                i = self.jump_if_true(i)
            elif opcode == 6:
                i = self.jump_if_false(i)
            elif opcode == 7:
                i = self.less_than(i)
            elif opcode == 8:
                i = self.equals(i)
            else:
                raise Exception(f'Unrecognized operation {op} at {i}!')
                
                
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
            
        def test_example_6(self):
            runner = IntcodeRunner([3,9,8,9,10,9,4,9,99,-1,8], [8])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
            
        def test_example_7(self):
            runner = IntcodeRunner([3,9,8,9,10,9,4,9,99,-1,8], [10])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])

        def test_example_8(self):
            runner = IntcodeRunner([3,9,7,9,10,9,4,9,99,-1,8], [7])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
            
        def test_example_9(self):
            runner = IntcodeRunner([3,9,7,9,10,9,4,9,99,-1,8], [10])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])

        def test_example_10(self):
            runner = IntcodeRunner([3,9,7,9,10,9,4,9,99,-1,8], [8])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])



        def test_example_6i(self):
            runner = IntcodeRunner([3,3,1108,-1,8,3,4,3,99], [8])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
            
        def test_example_7i(self):
            runner = IntcodeRunner([3,3,1108,-1,8,3,4,3,99], [10])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])

        def test_example_8i(self):
            runner = IntcodeRunner([3,3,1107,-1,8,3,4,3,99], [7])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
            
        def test_example_9i(self):
            runner = IntcodeRunner([3,3,1107,-1,8,3,4,3,99], [10])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])

        def test_example_10i(self):
            runner = IntcodeRunner([3,3,1107,-1,8,3,4,3,99], [8])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])
            
        def test_example_11(self):
            runner = IntcodeRunner([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])
        
        def test_example_12(self):
            runner = IntcodeRunner([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [10])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
            
        def test_example_13(self):
            runner = IntcodeRunner([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [1])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
        
        def test_example_11i(self):
            runner = IntcodeRunner([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0])
            ret = runner.run()
            
            self.assertListEqual(ret, [0])
        
        def test_example_12i(self):
            runner = IntcodeRunner([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [10])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
            
        def test_example_13i(self):
            runner = IntcodeRunner([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [1])
            ret = runner.run()
            
            self.assertListEqual(ret, [1])
        
        def test_example_14(self):
            runner = IntcodeRunner([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                                    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                                    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [1])
            ret = runner.run()
            
            self.assertListEqual(ret, [999])
        
        def test_example_15(self):
            runner = IntcodeRunner([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                                    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                                    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [8])
            ret = runner.run()
            
            self.assertListEqual(ret, [1000])
            
        def test_example_16(self):
            runner = IntcodeRunner([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                                    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                                    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [10])
            ret = runner.run()
            
            self.assertListEqual(ret, [1001])
        
    unittest.main()
