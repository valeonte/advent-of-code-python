"""
Advent of Code 2024 day 2.

Created on Mon Dec 02 2024 5:52:51 PM

@author: Eftychios
"""

import os

os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
inp_string = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

with open("inputs/day-3.txt", "r") as f:
    inp_string = f.read()


class Command:
    def __init__(self):
        self.base_command = 'mul('
        self.next_idx = 0
        self.in_first_number = False
        self.in_second_number = False

        self.first_number = ''
        self.second_number = ''

    def get_result_and_reset(self) -> int:
        res = int(self.first_number) * int(self.second_number)
        self.__init__()
        return res

    def add_char(self, char: str):
        if self.in_second_number:
            if char.isnumeric():
                self.second_number += char
                return
            if char == ')' and len(self.second_number) > 0:
                return self.get_result_and_reset()
        elif self.in_first_number:
            if char.isnumeric():
                self.first_number += char
                return
            if char == ',' and len(self.first_number) > 0:
                self.in_first_number = False
                self.in_second_number = True
                return
        elif char == self.base_command[self.next_idx]:
            if char == '(':
                self.in_first_number = True
            else:
                self.next_idx += 1
            return

        # reset, invalid char
        self.__init__()


sum_ret = 0
cmd = Command()
for ch in inp_string:
    part_res = cmd.add_char(ch)
    if part_res is not None:
        sum_ret += part_res

print('Answer 1:', sum_ret)


sum_ret = 0
cmd = Command()
muls_enabled = True
enable_string = "do()"
disable_string = "don't()"
for i, ch in enumerate(inp_string):
    part_res = cmd.add_char(ch)
    if muls_enabled:
        if i < len(inp_string) - len(disable_string):
            if inp_string[i:i+len(disable_string)] == disable_string:
                muls_enabled = False
                continue
        if part_res is not None:
            sum_ret += part_res
    elif i < len(inp_string) - len(enable_string):
        if inp_string[i:i+len(enable_string)] == enable_string:
            muls_enabled = True


print('Answer 2:', sum_ret)
