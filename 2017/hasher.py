# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 20:26:38 2019

@author: Eftychios
"""

from typing import Iterator

class Hasher:
    
    def __init__(self, max_length: int):
        self.hash = list(range(0, max_length))
        self.skip = 0
        self.position = 0
        self.max_length = max_length
        
    def do_reverse(self, idx_from: int, idx_to: int) -> None:
        #a=list(range(0,10))
        #idx_from=8
        #idx_to=1
        a = self.hash
        max_length = self.max_length
        
        if idx_from == idx_to:
            return
        
        if idx_from < idx_to:
            a[idx_from:idx_to+1] = list(reversed(a[idx_from:idx_to+1]))
            return
        
        
        rev_list = list(reversed(a[idx_from: max_length] + a[0:idx_to+1]))
        a[idx_from: max_length] = rev_list[0:max_length - idx_from]
        a[0:idx_to+1] = rev_list[max_length - idx_from:len(rev_list)]
    
    def move_position_by(self, steps) -> None:
        self.position = (self.position + steps) % self.max_length
    
    def process_length(self, length: int) -> None:
        
        if length > 0:
            idx_from = self.position
            # we move by length-1 to get the end of the range
            self.move_position_by(length - 1)
            idx_to = self.position
            #and then move by another 1
            self.move_position_by(1)        
            self.do_reverse(idx_from, idx_to)

        self.move_position_by(self.skip)
        self.skip += 1
        
    def process_series(self, lengths: Iterator[int], iterations: int = 1):
        for i in range(0, iterations):
            for l in lengths:
                self.process_length(l)

    def process_string(self, inputs: str):
        self.process_series([ord(ch) for ch in inputs] + [17, 31, 73, 47, 23],
                             64)
                
    def dense_hash_digits(self) -> Iterator[str]:
        if self.max_length != 256:
            raise Exception()
        
        for i in range(0, 16):
            offset = i * 16
            digit = self.hash[offset]
            
            for j in range(1, 16):
                digit = digit ^ self.hash[offset + j]
            
            hex_rep = hex(digit)[2:]
            if len(hex_rep) < 2:
                hex_rep = "0" + hex_rep
            yield hex_rep
        
    def dense_hash_string(self) -> str:
        
        return "".join([d for d in self.dense_hash_digits()])
    
    def hash_bits(self) -> Iterator[bool]:
        for hex_digit in self.dense_hash_digits():
            num = int(hex_digit, 16)
            binary = bin(num)[2:].zfill(8)
            for ch in binary:
                yield ch == '1'



if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_series_1(self):
            h = Hasher(256)
            h.process_string("")
            self.assertEqual(h.dense_hash_string(), "a2582a3a0e66e6e86e3812dcb672a272")
            
        def test_series_2(self):
            h = Hasher(256)
            h.process_string("AoC 2017")
            self.assertEqual(h.dense_hash_string(), "33efeb34ea91902bb2f59c9920caa6cd")
            
        def test_series_3(self):
            h = Hasher(256)
            h.process_string("1,2,3")
            self.assertEqual(h.dense_hash_string(), "3efbe78a8d82f29979031a4aa0b16a9d")
        
        def test_series_4(self):
            h = Hasher(256)
            h.process_string("1,2,4")
            self.assertEqual(h.dense_hash_string(), "63960835bcdc130f0b66d7ff4f6a5a8e")
            
        def test_process_length_0(self):
            h = Hasher(5)
            h.process_length(0)
            self.assertListEqual(h.hash, [0,1,2,3,4])
            self.assertEqual(h.skip, 1)
            self.assertEqual(h.position, 0)
            
        def test_process_length_1(self):
            h = Hasher(5)
            h.process_length(3)
            self.assertListEqual(h.hash, [2,1,0,3,4])
            self.assertEqual(h.skip, 1)
            self.assertEqual(h.position, 3)
            
        def test_process_length_2(self):
            h = Hasher(5)
            h.process_length(3)
            h.process_length(4)
            self.assertListEqual(h.hash, [4,3,0,1,2])
            self.assertEqual(h.skip, 2)
            self.assertEqual(h.position, 3)
            
        def test_process_length_3(self):
            h = Hasher(5)
            h.process_length(3)
            h.process_length(4)
            h.process_length(1)
            self.assertListEqual(h.hash, [4,3,0,1,2])
            self.assertEqual(h.skip, 3)
            self.assertEqual(h.position, 1)
            
        def test_process_length_4(self):
            h = Hasher(5)
            h.process_length(3)
            h.process_length(4)
            h.process_length(1)
            h.process_length(5)
            self.assertListEqual(h.hash, [3,4,2,1,0])
            self.assertEqual(h.skip, 4)
            self.assertEqual(h.position, 4)
        
        def test_do_reverse_easy_1(self):
            h = Hasher(10)
            h.do_reverse(0, 4)
            self.assertListEqual(h.hash, [4,3,2,1,0,5,6,7,8,9])
        
        def test_do_reverse_easy_2(self):
            h = Hasher(10)
            h.do_reverse(2, 4)
            self.assertListEqual(h.hash, [0,1,4,3,2,5,6,7,8,9])
            
        def test_do_reverse_circ_1(self):
            h = Hasher(10)
            h.do_reverse(8, 1)
            self.assertListEqual(h.hash, [9,8,2,3,4,5,6,7,1,0])
            
        def test_do_reverse_circ_2(self):
            h = Hasher(10)
            h.do_reverse(9, 0)
            self.assertListEqual(h.hash, [9,1,2,3,4,5,6,7,8,0])

        def test_move_position_1(self):
            h = Hasher(10)
            h.move_position_by(5)
            self.assertEqual(h.position, 5)
            
        def test_move_position_2(self):
            h = Hasher(10)
            h.move_position_by(10)
            self.assertEqual(h.position, 0)
            
        def test_move_position_3(self):
            h = Hasher(10)
            h.move_position_by(5)
            h.move_position_by(5)
            self.assertEqual(h.position, 0)
    
    unittest.main()
