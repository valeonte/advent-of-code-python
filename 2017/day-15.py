# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 22:02:36 2019

@author: Eftychios
"""

import os
os.chdir("C:/Repos/advent-of-code-python/2017")

class Generator:
    def __init__(self,
                 seed: int,
                 factor: int,
                 divisor: int = 1):
        
        self._seed = seed
        self._factor = factor
        self._divisor = divisor
    
    def values(self) -> Iterator[int]:
        previous = self._seed

        while True:
            value = previous * self._factor
            previous = value % 2147483647
            if previous % self._divisor == 0:
                yield previous


gen_a = Generator(722, 16807)
gen_b = Generator(354, 48271)

#gen_a = Generator(65, 16807)
#gen_b = Generator(8921, 48271)


iterations = 40000000
#iterations = 5
judge_count = 0
judge_mask = int('ffff', 16)
cnt = 0
for (num_a, num_b) in zip(gen_a.values(), gen_b.values()):
    cnt += 1

    if cnt % 1000000 == 0:
        print(cnt, num_a, num_b)

    if num_a & judge_mask == num_b & judge_mask:
        judge_count += 1


    if cnt >= iterations:
        break

answer_1 = judge_count

gen_a = Generator(722, 16807, 4)
gen_b = Generator(354, 48271, 8)

#gen_a = Generator(65, 16807, 4)
#gen_b = Generator(8921, 48271, 8)


iterations = 5000000
#iterations = 5
judge_count = 0
judge_mask = int('ffff', 16)
cnt = 0
for (num_a, num_b) in zip(gen_a.values(), gen_b.values()):
    cnt += 1

    if cnt % 200000 == 0:
        print(cnt, num_a, num_b)

    if num_a & judge_mask == num_b & judge_mask:
        judge_count += 1


    if cnt >= iterations:
        break

answer_2 = judge_count

print(answer_1, answer_2)
#612 285
