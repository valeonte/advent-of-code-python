# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 22:44:46 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List
import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2019")

class FFT:
    def __init__(self,
                 pattern: List[int]):
        self._pattern = pattern
        
    def get_pattern_for_digit(self,
                              digit_order: int) -> Iterator[int]:
        
        #print('Getting pattern for digit', digit_order)
        first = True
        while True:
            for i in self._pattern:
                for j in range(0, digit_order):
                    #print("i j", i, j)
                    if first:
                        first = False
                        continue
                    
                    yield i

            #print('Pattern sequence exhausted')
    
    def get_pattern_matrix(self,
                           input_size: int):
        
        print('Getting pattern matrix for input size', input_size)
        ret = np.zeros((input_size, input_size), int)
        for i in range(0, input_size):
            gen = self.get_pattern_for_digit(i+1)
            row = []
            for k in range(0, input_size):
                row.append(next(gen))
                
            ret[i,:] = row
        
        return ret
        
    
    def get_output_digit(self,
                         input_sequence: List[int],
                         digit_order: int) -> int:
        
        gen = self.get_pattern_for_digit(digit_order)
        total = 0
        for v in input_sequence:
            total += v * next(gen)
        
        return abs(total) % 10

    def get_output_sequence(self,
                            input_sequence: List[int]) -> Iterator[int]:
        
        for (i, v) in enumerate(input_sequence):
            yield self.get_output_digit(input_sequence, i+1)

    def get_output_after_phases(self,
                                phases: int,
                                input_sequence: List[int]) -> List[int]:
        
        previous_phase = input_sequence
        for p in range(0, phases):
            previous_phase = list(self.get_output_sequence(previous_phase))
        
        return previous_phase

    def sequence_str(self,
                     input_sequence: Iterator[int],
                     offset: int = 0,
                     count: int = 100) -> str:
        
        return ''.join([str(d) for (i, d) in enumerate(input_sequence) 
                        if i >= offset and i < offset+count])

    def get_characters_at_offset(self,
                                 offset: int,
                                 phases: int) -> Iterator[str]:
        pass


with open("inputs/day16.txt", "r") as f:
    inp = f.read()

f = FFT([0,1,0,-1])

if not 'answer_1' in locals():
    print('Getting answer_1')
    inp_sec = [int(ch) for ch in inp]
    v = f.get_output_after_phases(100, inp_sec)
    answer_1 = f.sequence_str(v, 0, 8)
    print('answer_1 ->', answer_1)


inp = [int(ch) for ch in "80871224585914546619083218645595"]

last_seq = inp
for i in range(0, 20):
    print(f.sequence_str(last_seq))
    last_seq = list(f.get_output_sequence(last_seq))
    

#
#mat = f.get_pattern_matrix(32)
#mat2 = np.dot(mat,mat)
#mat4 = np.dot(mat2, mat2)
#mat16 = np.dot(mat4, mat4)
#mat5 = np.dot(mat4, mat)
#
#np.dot(np.identity(3),np.array([[1, -3, 3],
#                        [3, -5, 3],
#                        [6, -6, 4]]))
#np.linalg.eig()
#
#a=np.array([[1,2,3],
#            [2,3,4],
#            [3,4,5]])
#
#b = np.array([1,0,-1])
#np.dot(a,a)
#np.square(b)
#np.linalg.matrix_power(a,5)

    
if __name__ == "__main__":
    
    import unittest
    
    class TestAll(unittest.TestCase):

        def test_pattern_1(self):
            pattern = [1,2,3,4]
            f = FFT(pattern)
            
            gen = f.get_pattern_for_digit(1)
            for i in range(1, 4):
                self.assertEqual(pattern[i], next(gen))
        
        def test_pattern_2(self):
            pattern = [1,2]
            f = FFT(pattern)
            
            gen = f.get_pattern_for_digit(3)
            for i in range(0, 8):
                if i in [0, 1,5,6,7]:
                    self.assertEqual(1, next(gen))
                elif i in [2,3,4]:
                    self.assertEqual(2, next(gen))

        def test_output_digit_1(self):
            f = FFT([0,1,0,-1])
            
            v = f.get_output_digit([1,2,3,4,5,6,7,8], 1)
            self.assertEqual(v, 4)
        
        def test_output_digit_4(self):
            f = FFT([0,1,0,-1])
            
            v = f.get_output_digit([1,2,3,4,5,6,7,8], 4)
            self.assertEqual(v, 2)
            
        def test_output_digit_8(self):
            f = FFT([0,1,0,-1])
            
            v = f.get_output_digit([1,2,3,4,5,6,7,8], 8)
            self.assertEqual(v, 8)
        
        def test_output_sequence_1(self):
            f = FFT([0,1,0,-1])
            
            v = f.get_output_sequence([1,2,3,4,5,6,7,8])
            self.assertListEqual(list(v), [4,8,2,2,6,1,5,8])

        def test_output_sequence_2(self):
            f = FFT([0,1,0,-1])
            
            v = f.get_output_sequence([4,8,2,2,6,1,5,8])
            self.assertListEqual(list(v), [3,4,0,4,0,4,3,8])

        def test_phases_1(self):
            f = FFT([0,1,0,-1])
            
            inp = [int(ch) for ch in "80871224585914546619083218645595"]
            v = f.get_output_after_phases(100, list(inp))
            
            self.assertListEqual(list(v)[0:8], [2,4,1,7,6,1,7,6])

        def test_phases_2(self):
            f = FFT([0,1,0,-1])
            
            inp = [int(ch) for ch in "19617804207202209144916044189917"]
            v = f.get_output_after_phases(100, list(inp))
            
            self.assertListEqual(list(v)[0:8], [7,3,7,4,5,4,1,8])

        def test_phases_3(self):
            f = FFT([0,1,0,-1])
            
            inp = [int(ch) for ch in "69317163492948606335995924319873"]
            v = f.get_output_after_phases(100, list(inp))
            
            self.assertListEqual(list(v)[0:8], [5,2,4,3,2,1,3,3])


    unittest.main()
