# -*- coding: utf-8 -*-
"""
Day 8 Advent of Code 2020 file.

Created on Fri Dec 11 13:18:45 2020

@author: Eftychios
"""

import os
import re


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

with open("inputs/day-8.txt", "r") as f:
    inp_string = f.read()


class Console:
    """A console running a program."""

    def __init__(self, program_string: str):
        self.program = program_string.split("\n")
        self.accumulator = 0
        self.run_pointer = 0
        self.execution_counter = 0
        self.executed_commands = set()
        self.command_re = re.compile(r'^(?P<command>\w+) (?P<arg>[\+\-\d]+)$')

    def run_command(self) -> bool:
        """Execute next command. Return True on termination."""
        command = self.program[self.run_pointer]

        self.executed_commands.add(self.run_pointer)
        self.execution_counter += 1

        m = self.command_re.match(command)
        arg = int(m.group('arg'))

        command = m.group('command')
        if command == 'acc':
            self.acc(arg)
        elif command == 'jmp':
            self.jmp(arg)
        elif command == 'nop':
            self.nop()
        else:
            raise Exception(f'Unknown command {command}!')

        return self.run_pointer == len(self.program)

    def acc(self, arg: int):
        """Run acc command."""
        self.accumulator += arg
        self.run_pointer += 1

    def jmp(self, arg: int):
        """Run jmp command."""
        self.run_pointer += arg

    def nop(self):
        """Run nop command."""
        self.run_pointer += 1

    def flip_command(self, idx: int) -> bool:
        """Flips a command from nop to jmp and back."""
        command = self.program[idx]
        if command.startswith('acc'):
            return False

        if command.startswith('nop'):
            self.program[idx] = command.replace('nop', 'jmp')
        else:
            self.program[idx] = command.replace('jmp', 'nop')

        return True

    def run_to_infinite_loop(self) -> bool:
        """Run until right before you execute the same command twice."""
        while self.run_pointer not in self.executed_commands:
            if self.run_command():
                return True

        return False


console = Console(inp_string)
console.run_to_infinite_loop()

print('Answer 1:', console.accumulator)


for i in range(0, len(console.program)):
    console = Console(inp_string)
    if not console.flip_command(i):
        continue

    if console.run_to_infinite_loop():
        break

print('Answer 2:', console.accumulator)
