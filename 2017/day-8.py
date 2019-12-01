# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 16:06:06 2019

@author: Eftychios
"""
import os
import re

class Registry:
    
    def __init__(self):
        self.dict = dict()
        self.running_max = 0
        
    def get_reg(self, reg: str) -> int:
        if not reg in self.dict.keys():
            self.dict[reg] = 0
        
        return self.dict[reg]
    
    def set_reg(self, reg: str, val: int) -> None:
        if val > self.running_max:
            self.running_max = val
            
        self.dict[reg] = val
        

    def compare(self, comp_register: str, comp: str, comp_num: int) -> bool:
        left_arg = self.get_reg(comp_register)
        right_arg = comp_num
        switcher = {
                "<": left_arg < right_arg,
                "<=": left_arg <= right_arg,
                "==": left_arg == right_arg,
                "!=": left_arg != right_arg,
                ">": left_arg > right_arg,
                ">=": left_arg >= right_arg
                }
        
        ret = switcher.get(comp, "Invalid comarator!!")
        if type(ret) != bool:
            raise Exception(f"Invalid comarator {comp}!!")
        
        return ret

    def operate(self, register:str, op: str, arg: int) -> None:
        reg_val = self.get_reg(register)
        if op == "inc":
            reg_val += arg
        else:
            reg_val -= arg
        
        self.set_reg(register, reg_val)

    def full_operation(self, result_register: str, op: str, op_arg: int,
                        comp_register: str, comp: str, comp_num: int):
        
        if (self.compare(comp_register, comp, comp_num)):
            self.operate(result_register, op, op_arg)
        

regex = "^(\w+) (inc|dec) ([\d-]+) if (\w+) ([!<>=]+) ([\d-]+)$"

os.chdir("C:/Repos/advent-of-code-python")

with open("2017/inputs/day8.txt", "r") as f:
    inputs = f.read()

expr = [e for e in inputs.split('\n')]
regs = Registry()



for e in expr:

    print(e)
    
    m = re.search(regex, e)
    if not m:
        raise Exception(f'Line {e} did not match!!')

    result_register = m.group(1)
    op = m.group(2)
    op_arg = int(m.group(3))
    
    comp_register = m.group(4)
    comp = m.group(5)
    comp_num = int(m.group(6))

    regs.full_operation(result_register, op, op_arg, comp_register, comp, comp_num)

answer_1 = max(regs.dict.values())
answer_2 = regs.running_max

print(answer_1, answer_2)
