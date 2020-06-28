# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 21:09:20 2020

@author: valeo
"""

import os
import time
import math

from typing import Dict


os.chdir("C:/Repos/advent-of-code-python/2017")


with open("inputs/day23.txt", "r") as f:
    inp = f.read()


def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


class CoProcessor:

    def __init__(self,
                 program: str,
                 register_a: int = 0):

        self.registers: Dict[str, int] = {'a': register_a,
                                          'h': 0}
        self.mul_counter = 0
        self.program = program
        self.idx = 0
        self.last_run = [0] * 50

    def prog(self, register_a):
        b = 67
        c = b
        h = 0
        g = 0
        a = register_a
        if a != 0:
            b = 100 * b + 100000
            c = b + 17000
        while True:
            f = 1
            d = 2
            while d != b:
                e = 2
                while b != e:
                    if d * e == b:
                        f = 0
                    e = e + 1
                d = d + 1
                print(f'{a}'.rjust(12),
                      f'{b}'.rjust(12),
                      f'{c}'.rjust(12),
                      f'{d}'.rjust(12),
                      f'{e}'.rjust(12),
                      f'{f}'.rjust(12),
                      f'{g}'.rjust(12),
                      f'{h}'.rjust(12))
                if e == b:
                    if is_prime(b):
                        print('Prime number', b)
                    else:
                        f = 0
                    d = b
            if f == 0:
                h = h + 1
            if b == c:
                print(f'{a}'.rjust(12),
                      f'{b}'.rjust(12),
                      f'{c}'.rjust(12),
                      f'{d}'.rjust(12),
                      f'{e}'.rjust(12),
                      f'{f}'.rjust(12),
                      f'{g}'.rjust(12),
                      f'{h}'.rjust(12))

                return (a,b,c,d,e,f,g,h)
            b = b + 17

    def run_program(self) -> int:
        commands = [c
                    for c in self.program.split("\n")
                    if len(c) > 0]

        cnt = 0
        phase = 0
        skip_iterations = 0

        while True:
            if self.idx >= len(commands):
                print('Ran out of commands!')
                break

            self.last_run[cnt % 50] = self.idx

            cnt += 1
            command = commands[self.idx]

            if skip_iterations > 0:
                skip_iterations -= 1
            else:
                self.print_program()
                iterations = input()
                if iterations == 'q':
                    print('Quitting')
                    return
                try:
                    skip_iterations = int(iterations)
                    print('Running for', skip_iterations, 'iterations')
                except Exception:
                    pass

            # if phase == 0 and command == 'jnz g -8':
            #     phase = 1
            #     print('Switching phases')
            #     self.print_registers()
            #     self.registers['e'] = 106690
            #     self.registers['g'] = -10
            #     self.registers['f'] = 0
            #     time.sleep(2)

            # if phase == 1 and (command == 'jnz g -8'
            #                    or command == 'jnz g 2'):
            #     self.print_registers()
            #     time.sleep(2)

            ret = self.run_command(command)
            self.idx += 1 if ret is None else ret

    def run_command(self, command: str) -> int:

        parts = command.split(" ")
        func = parts[0]
        args = parts[1:]

        return eval(f'self.{func}(*args)')

    def resolve_value(self, value: str):
        try:
            return int(value)
        except Exception:
            pass
        try:
            return self.registers[value]
        except Exception:
            self.registers[value] = 0
            return 0

    def set(self, register: str, value: str):
        value = self.resolve_value(value)
        self.registers[register] = value

    def sub(self, register: str, value: str):
        value = self.resolve_value(value)
        self.registers[register] = self.resolve_value(register) - value

    def mul(self, register: str, value: str):
        value = self.resolve_value(value)
        self.registers[register] = self.resolve_value(register) * value
        self.mul_counter += 1

    def jnz(self, mask: str, value: str):
        mask = self.resolve_value(mask)
        if mask != 0:
            return self.resolve_value(value)

    def print_program(self):

        print('-' * 100)
        regs = sorted(list(self.registers.items()))

        for i, c in enumerate(self.program.split("\n")):
            if len(c) == 0:
                continue

            if i == self.idx:
                line = c.ljust(15) + '| <==='
            elif i in self.last_run:
                line = c.ljust(15) + '|'
            else:
                line = c

            if i < len(regs):
                reg = regs[i]
                line = line.ljust(30) + reg[0] + str(reg[1]).rjust(10)

            print(line)


# a = CoProcessor(0)
# a.run_program(inp)
# answer_1 = a.mul_counter
# print(answer_1)
# a.print_registers()

b = CoProcessor(inp, 1)
#b.run_program()
# b.print_registers()

b.prog(1)
