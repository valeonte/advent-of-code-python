# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 20:17:58 2019

@author: Eftychios
"""

import os
from typing import Iterator
os.chdir("C:/Repos/advent-of-code-python/2017")

from hasher import Hasher

with open("inputs/day10.txt", "r") as f:
    inputs = f.read()

h = Hasher(256)
h.process_series([int(l) for l in inputs.split(',')])

answer_1 = h.hash[0] * h.hash[1]

h = Hasher(256)
h.process_string(inputs)

answer_2 = h.dense_hash_string()

print(answer_1, answer_2)
