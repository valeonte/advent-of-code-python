"""
Advent of Code 2021 day 24.

Created on Sat Dec 16 2023 8:43:25 PM

@author: Eftychios
"""

import os
import re

from typing import List
from logging import getLogger

log = getLogger(__name__)

os.chdir("C:/Repos/advent-of-code-python/2021")


inp_string = """inp x
mul x -1"""

inp_string = """inp z
inp x
mul z 3
eql z x"""

inp_string = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""

with open("inputs/day-24-orig.txt", "r") as f:
    inp_string = f.read()


class ALU:
    def __init__(self, inputs: List[int]):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

        self.inputs = inputs
        self.pat = re.compile(r'^(?P<command>inp|add|mul|div|mod|eql) (?P<a>[wxyz]){1}( (?P<b>-?\d+|[wxyz]))?$')
        self.inpcnt = 0

    def __repr__(self) -> str:
        return f'ALU(w={self.w}, x={self.x}, y={self.y}, z={self.z})'

    def inp(self, a: str):
        self.inpcnt += 1
        print('Pre digit', self.inpcnt, ':', self.z)
        setattr(self, a, self.inputs.pop(0))

    def add(self, a: str, b: int):
        setattr(self, a, getattr(self, a) + b)

    def mul(self, a: str, b: int):
        setattr(self, a, getattr(self, a) * b)

    def div(self, a: str, b: int):
        setattr(self, a, int(getattr(self, a) / b))

    def mod(self, a: str, b: int):
        setattr(self, a, getattr(self, a) % b)
    
    def eql(self, a: str, b: int):
        setattr(self, a, 1 if getattr(self, a) == b else 0)

    def run_command(self, command: str):
        """Run the command."""
        m = self.pat.match(command)
        command = m.group('command')
        a = m.group('a')
        b = m.group('b')

        if b is None:
            self.inp(a)
            return
        try:
            bb = int(b)
        except Exception:
            bb = getattr(self, b)
        func = getattr(self, command)
        func(a, bb)


def monad_block(w: int, z: int, z_div: int, x_add: int, y_add: int) -> int:
    x = z % 26 + x_add
    if x < 10 and x != w:
        print('potential savings!!')
    z = int(z / z_div)
    if x == w:
        return z

    z = 26 * z + w + y_add

    return z

def monad(inputs: List[int]) -> int:
    """Runs the monad code and returns z."""
    it = iter(inputs)

    w = next(it)
    z = monad_block(w, 0, 1, 12, 7)

    print('Pre digit 2:', z)
    w = next(it)
    z = monad_block(w, z, 1, 11, 15)

    print('Pre digit 3:', z)
    w = next(it)
    z = monad_block(w, z, 1, 12, 2)

    print('Pre digit 4:', z)
    w = next(it)
    z = monad_block(w, z, 26, -3, 15)

    print('Pre digit 5:', z)
    w = next(it)
    z = monad_block(w, z, 1, 10, 14)

    print('Pre digit 6:', z)
    w = next(it)
    z = monad_block(w, z, 26, -9, 2)

    print('Pre digit 7:', z)
    w = next(it)
    z = monad_block(w, z, 1, 10, 15)

    print('Pre digit 8:', z)
    w = next(it)
    z = monad_block(w, z, 26, -7, 1)

    print('Pre digit 9:', z)
    w = next(it)
    z = monad_block(w, z, 26, -11, 15)

    print('Pre digit 10:', z)
    w = next(it)
    z = monad_block(w, z, 26, -4, 15)

    print('Pre digit 11:', z)
    w = next(it)
    z = monad_block(w, z, 1, 14, 12)

    print('Pre digit 12:', z)
    w = next(it)
    z = monad_block(w, z, 1, 11, 2)

    print('Pre digit 13:', z)
    w = next(it)
    z = monad_block(w, z, 26, -8, 13)

    print('Pre digit 14:', z)
    w = next(it)
    z = monad_block(w, z, 26, -10, 13)

    return z

inputs = [6, 5, 9, 8, 4,
          9, 1, 9, 9, 9,
          7, 9, 3, 9]
print(monad(inputs))

# alu = ALU(inputs)
# for command in inp_string.split('\n'):
#     alu.run_command(command)


print('Answer 1:', ''.join([str(n) for n in inputs]))

inputs = [1, 1, 2, 1, 1,
          6, 1, 9, 5, 4,
          1, 7, 1, 3]
print(monad(inputs))

print('Answer 2:', ''.join([str(n) for n in inputs]))
