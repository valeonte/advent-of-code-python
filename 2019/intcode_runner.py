# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 09:07:13 2019

@author: Eftychios
"""

from typing import List, Tuple, Iterator
from enum import Enum

class ParameterMode(Enum):
    Position = 0
    Value = 1
    Relative = 2


class IntcodeRunner:
    def __init__(self, program: List[int],
                 inputs: List[int] = None,
                 extend: int = 0,
                 print_output: bool = False,
                 input_iterator: Iterator[int] = None,
                 name: str = "default"):
        self.program = program + [0]*extend
        self.outputs = []
        self.relative_base = 0
        self.print_output = print_output
        self.name = name

        if input_iterator is not None:
            self.input_iterator = input_iterator
        elif inputs is not None:
            self.input_iterator = iter(inputs)
        else:
            self.input_iterator = None

    def add(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 1:
            raise Exception("Not addition!!")

        x = self.get_parameter(op_address, opcode, 1)
        y = self.get_parameter(op_address, opcode, 2)

        parameter_mode = self.get_parameter_mode(opcode, 3)
        if parameter_mode == ParameterMode.Value:
            raise Exception("Addition output in immediate mode!")

        if parameter_mode == ParameterMode.Position:
            self.program[self.program[op_address + 3]] = x + y

        if parameter_mode == ParameterMode.Relative:
            self.program[self.program[op_address + 3] + self.relative_base] = x + y

        return op_address + 4

    def get_parameter_mode(self, opcode: int, pnum: int) -> ParameterMode:
        return ParameterMode(opcode // 10**(pnum + 1) % 10)

    def get_parameter(self, op_address: int, opcode: int, pnum: int) -> int:

        addr = op_address + pnum
        parameter_mode = self.get_parameter_mode(opcode, pnum)

        if parameter_mode == ParameterMode.Position:
            return self.program[self.program[addr]]

        if parameter_mode == ParameterMode.Value:
            return self.program[addr]

        if parameter_mode == ParameterMode.Relative:
            return self.program[self.relative_base + self.program[addr]]

        raise Exception(f'Unexpected parameter mode {parameter_mode}!')


    def multiply(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 2:
            raise Exception("Not multiplication!!")

        x = self.get_parameter(op_address, opcode, 1)
        y = self.get_parameter(op_address, opcode, 2)

        parameter_mode = self.get_parameter_mode(opcode, 3)
        if parameter_mode == ParameterMode.Value:
            raise Exception("Multiplication output in immediate mode!")

        if parameter_mode == ParameterMode.Position:
            self.program[self.program[op_address + 3]] = x * y

        if parameter_mode == ParameterMode.Relative:
            self.program[self.program[op_address + 3] + self.relative_base] = x * y

        return op_address + 4

    def jump_if_true(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 5:
            raise Exception("Not jump-if-true!!")

        x = self.get_parameter(op_address, opcode, 1)

        if x != 0:
            return self.get_parameter(op_address, opcode, 2)

        return op_address + 3

    def jump_if_false(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 6:
            raise Exception("Not jump-if-false!!")

        x = self.get_parameter(op_address, opcode, 1)

        if x == 0:
            return self.get_parameter(op_address, opcode, 2)

        return op_address + 3

    def less_than(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 7:
            raise Exception("Not less-than!!")

        x = self.get_parameter(op_address, opcode, 1)
        y = self.get_parameter(op_address, opcode, 2)

        result = 1 if x < y else 0

        parameter_mode = self.get_parameter_mode(opcode, 3)
        if parameter_mode == ParameterMode.Value:
            raise Exception("Not less-than output in immediate mode!")

        if parameter_mode == ParameterMode.Position:
            self.program[self.program[op_address + 3]] = result

        if parameter_mode == ParameterMode.Relative:
            self.program[self.program[op_address + 3] + self.relative_base] = result

        return op_address + 4

    def equals(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 8:
            raise Exception("Not equals!!")

        x = self.get_parameter(op_address, opcode, 1)
        y = self.get_parameter(op_address, opcode, 2)

        result = 1 if x == y else 0

        parameter_mode = self.get_parameter_mode(opcode, 3)
        if parameter_mode == ParameterMode.Value:
            raise Exception("Equals output in immediate mode!")

        if parameter_mode == ParameterMode.Position:
            self.program[self.program[op_address + 3]] = result

        if parameter_mode == ParameterMode.Relative:
            self.program[self.program[op_address + 3] + self.relative_base] = result

        return op_address + 4


    def key_input(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 3:
            raise Exception("Not input operation!!")

        if self.input_iterator is not None:
            inp = next(self.input_iterator)
        else:
            inp = input(f"Please enter program input {op_address}: ")
            if inp == "quit":
                raise Exception("Quit requested!")

        parameter_mode = self.get_parameter_mode(opcode, 1)
        if parameter_mode == ParameterMode.Value:
            raise Exception("Input operation with output in immediate mode!")

        if parameter_mode == ParameterMode.Position:
            self.program[self.program[op_address + 1]] = int(inp)

        if parameter_mode == ParameterMode.Relative:
            self.program[self.program[op_address + 1] + self.relative_base] = int(inp)

        return op_address + 2


    def get_output(self, op_address: int) -> Tuple[int, int]:
        opcode = self.program[op_address]
        if opcode % 100 != 4:
            raise Exception("Not output operation!!")

        output = self.get_parameter(op_address, opcode, 1)
        self.outputs.append(output)

        if self.print_output:
            print(f"Output {op_address}: {output}")

        return (op_address + 2, output)

    def adjust_relative_base(self, op_address: int) -> int:
        opcode = self.program[op_address]
        if opcode % 100 != 9:
            raise Exception("Not adjust relative base!!")

        x = self.get_parameter(op_address, opcode, 1)

        self.relative_base += x

        return op_address + 2

    def run(self) -> List[int]:
        return list(self.iter_run())

    def iter_run(self) -> Iterator[int]:

        i = 0
        while True:
            op = self.program[i]

            #print(f"Operation {op} at {i}")

            opcode = op % 100
            # exit
            if opcode == 99:
                return

            # addition
            if opcode == 1:
                i = self.add(i)
            elif opcode == 2:
                i = self.multiply(i)
            elif opcode == 3:
                i = self.key_input(i)
            elif opcode == 4:
                (i, output) = self.get_output(i)
                yield output
            elif opcode == 5:
                i = self.jump_if_true(i)
            elif opcode == 6:
                i = self.jump_if_false(i)
            elif opcode == 7:
                i = self.less_than(i)
            elif opcode == 8:
                i = self.equals(i)
            elif opcode == 9:
                i = self.adjust_relative_base(i)
            else:
                raise Exception(f'Unrecognized operation {op} at {i}!')

runner = IntcodeRunner([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], extend=10000)
ret = runner.run()


if __name__ == "__main__":

    import unittest

    class TestAll(unittest.TestCase):

        def test_day_9_1(self):
            runner = IntcodeRunner([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], extend=10000)
            ret = runner.run()

            self.assertListEqual(ret, [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])

        def test_day_9_2(self):
            runner = IntcodeRunner([1102,34915192,34915192,7,4,7,99,0])
            runner.run()

            self.assertEqual(runner.outputs[0], 1219070632396864)

        def test_day_9_3(self):
            runner = IntcodeRunner([104,1125899906842624,99])
            runner.run()

            self.assertEqual(runner.outputs[0], 1125899906842624)

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
                                    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], input_iterator=iter([10]))
            ret = runner.run()

            self.assertListEqual(ret, [1001])

    unittest.main()
