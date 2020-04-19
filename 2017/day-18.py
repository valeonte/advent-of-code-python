# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 21:09:20 2020

@author: valeo
"""

import os
from typing import Dict


os.chdir("C:/Repos/advent-of-code-python/2017")


with open("inputs/day18.txt", "r") as f:
    inp = f.read()


class MusicProcessor:

    def __init__(self, program_id: int):
        self.registers: Dict[str, int] = {'p': program_id}
        self.last_sound_played = -1
        self.__mate = None
        self.__queue = []
        self.program_id = program_id
        self.send_counter = 0

    def set_mate(self, mate):
        self.__mate = mate

    def enqueue(self, num: int):
        self.__queue.append(num)

    def run_program(self, program: str) -> int:
        commands = [c
                    for c in program.split("\n")
                    if len(c) > 0]

        idx = 0

        while True:
            command = commands[idx]

            ret = self.run_command(command)
            if ret is None:
                idx += 1
                if idx == len(commands):
                    return
                continue
            if ret == 0:
                print('Returning normally')
                return self.last_sound_played

            idx += ret

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

    def snd(self, frequency: str):
        frequency = self.resolve_value(frequency)
        self.send_counter += 1
        print(f'{self.program_id} sending {frequency} to '
              f'{self.__mate.program_id}')
        self.last_sound_played = frequency
        self.__mate.enqueue(frequency)

    def add(self, register: str, value: str):
        value = self.resolve_value(value)
        self.registers[register] = self.resolve_value(register) + value

    def mul(self, register: str, value: str):
        value = self.resolve_value(value)
        self.registers[register] = self.resolve_value(register) * value

    def mod(self, register: str, value: str):
        value = self.resolve_value(value)
        self.registers[register] = self.resolve_value(register) % value

    def jgz(self, mask: str, value: str):
        mask = self.resolve_value(mask)
        if mask > 0:
            return self.resolve_value(value)

    def rcv(self, register: str):
        if (len(self.__queue) == 0):
            print('Empty queue, receiving nothing')
            return 0

        self.registers[register] = self.__queue.pop(0)


a = MusicProcessor(0)
b = MusicProcessor(1)
a.set_mate(b)
b.set_mate(a)

# inp = """snd 1
# snd 2
# snd p
# rcv a
# rcv b
# rcv c
# rcv d"""

a_idx = 0
b_idx = 0
commands = inp.split('\n')
max_idx = len(commands)
deadlock = False

while (a_idx < max_idx or b_idx < max_idx) and not deadlock:

    deadlock = True
    if a_idx < max_idx:
        ret = a.run_command(commands[a_idx])
        if ret is None:
            a_idx += 1
        else:
            a_idx += ret

        deadlock = ret == 0

    if b_idx < max_idx:
        ret = b.run_command(commands[b_idx])
        if ret is None:
            b_idx += 1
        else:
            b_idx += ret

        deadlock = deadlock and ret == 0


#ret = p.run_program(inp)


if __name__ == '__main__':

    import unittest

    class TestAll(unittest.TestCase):

        def test_init(self):
            p = MusicProcessor(1)

            self.assertIsNotNone(p)

        def test_set(self):
            p = MusicProcessor(1)
            p.run_program("set a 11")

            self.assertEqual(p.registers['a'], 11)

        def test_add(self):
            p = MusicProcessor(1)
            p.run_program("""
set a 11
set b 22
add a b""")

            self.assertEqual(p.registers['a'], 33)

        def test_mul(self):
            p = MusicProcessor(1)
            p.run_program("""
set a 11
mul a 10""")

            self.assertEqual(p.registers['a'], 110)

        def test_mod(self):
            p = MusicProcessor(1)
            p.run_program("""
set a 11
mod a 5""")

            self.assertEqual(p.registers['a'], 1)

        def test_rcv_1(self):
            p = MusicProcessor(1)
            ret = p.run_program("""
set a 11
snd 12
rcv a""")

            self.assertEqual(ret, 12)

        def test_rcv_2(self):
            p = MusicProcessor(1)
            ret = p.run_program("""
set a 0
snd 12
rcv a""")

            self.assertIsNone(ret)

        def test_jgz(self):
            p = MusicProcessor(1)
            ret = p.run_program("""
set a 0
snd 12
jgz 1 2
set a 1
rcv a""")

            self.assertIsNone(ret)

    # unittest.main()
