# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 06:54:36 2019

@author: Eftychios
"""
from math import floor
import os

os.chdir("C:/Repos/advent-of-code-python")

def calc_fuel_required(mass: int, recursive: bool = False) -> int:
    fuel = floor(mass/3) - 2
    
    if fuel <= 0:
        fuel = 0
    
    if recursive:
        if fuel == 0:
            return fuel
        else:
            return fuel + calc_fuel_required(fuel, True)
    else:
        return fuel


with open("2019/inputs/day1.txt", "r") as f:
    contents = f.read()

all_numbers = [int(stritem)for stritem in contents.split("\n")]
all_fuels = [calc_fuel_required(mass) for mass in all_numbers]

answer_1 = sum(all_fuels)

all_fuels_rec = [calc_fuel_required(mass, True) for mass in all_numbers]

answer_2 = sum(all_fuels_rec)

print(answer_1, answer_2)

