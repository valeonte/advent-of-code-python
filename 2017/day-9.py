# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 17:22:52 2019

@author: Eftychios
"""

import os
import re

os.chdir("C:/Repos/advent-of-code-python")

with open("2017/inputs/day9.txt", "r") as f:
    inputs = f.read()

inputs = inputs.strip()

class StreamParser:
    
    def __init__(self):
        self.group_counter = 0
        self.in_garbage = False
        self.negator = False
        self.total_group_score = 0
        self.garbage_counter = 0
        
    def ParseStream(self, stream: str) -> None:
        for ch in stream:
            self.Parse(ch)
        
    def Parse(self, ch: str) -> None:
        if self.in_garbage:
            if self.negator:
                self.negator = False
                return # negating anything, resetting negator
            
            if ch == '!':
                self.negator = True
                return
            
            if ch == '>':
                self.in_garbage = False
                return
            
            # any other character is garbage
            self.garbage_counter += 1
            return
        
        if ch == "<":
            self.in_garbage = True
            return
        
        if ch == "{":
            self.group_counter += 1
            return
        
        if ch == "}":
            self.total_group_score += self.group_counter
            self.group_counter -= 1
            return
        
        if ch != ",":
            raise Exception(f"Unexpected out of garbage character --{ch}-- !!!")
            
        return
            
if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):
        
        def assert_stream_total(self, stream: str, total: int) -> int:
            sp = StreamParser()
            sp.ParseStream(stream)
            self.assertEqual(sp.total_group_score, total)
        
        def test_example_1(self):
            self.assert_stream_total("{}", 1)
        
        def test_example_2(self):
            self.assert_stream_total("{{{}}}", 6)
        
        def test_example_3(self):
            self.assert_stream_total("{{},{}}", 5)
        
        def test_example_4(self):
            self.assert_stream_total("{{{},{},{{}}}}", 16)
            
        def test_example_5(self):
            self.assert_stream_total("{<a>,<a>,<a>,<a>}", 1)
        
        def test_example_6(self):
            self.assert_stream_total("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9)
            
        def test_example_7(self):
            self.assert_stream_total("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9)
            
        def test_example_8(self):
            self.assert_stream_total("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3)
    
    unittest.main()
