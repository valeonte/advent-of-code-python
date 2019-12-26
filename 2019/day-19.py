# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:42:28 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List, NamedTuple, Set
import numpy as np

os.chdir("C:/Repos/advent-of-code-python/2019")

from intcode_runner import IntcodeRunner

with open("inputs/day19.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]


class TractorBeam:
    def __init__(self,
                 dim_rows: int,
                 dim_cols: int):
        self.dim_rows = 50
        self.dim_cols = 50
        
        self.beam = np.zeros((dim_rows, dim_cols), int)
        self.dp = np.zeros((dim_rows, dim_cols), int)
        
        self.biggest_square = 0
        self.bottom_right = (0, 0)


    def calculate_beam_cell(self,
                            row: int,
                            col: int):
        runner = IntcodeRunner(inp, inputs=[col, row], extend=1000)
        a=runner.run()
        self.beam[row, col] = a[0]
        

    def populate_beam(self):
        for row in range(self.dim_rows):
            for col in range(self.dim_cols):
                self.calculate_beam_cell(row, col)

    def calculate_dp_cell(self,
                          row: int,
                          col: int) -> int:

        if self.beam[row, col] == 0:
            return 0
        
        # If elements is at top  
        # row or first column,  
        # it wont form a square 
        # matrix's bottom-right 
        if row == 0 or col == 0: 
            self.dp[row, col] = 1
            return 1
  
        # Check if adjacent  
        # elements are equal            
        if (self.beam[row-1, col] == 1 and 
            self.beam[row, col-1] == 1 and
            self.beam[row-1, col-1] == 1):
            square_size = min(self.dp[row-1][col],
                              self.dp[row][col-1],
                              self.dp[row-1][col-1]) + 1
  
        # If not equal, then   
        # it will form a 1x1 
        # submatrix 
        else: 
            square_size = 1
        
        self.dp[row, col] = square_size
        if square_size > self.biggest_square:
            self.biggest_square = square_size
            self.bottom_right = (row, col)
        
        return square_size
    
    def populate_dp(self):

        for row in range(self.dim_rows):
            for col in range(self.dim_cols):
                self.calculate_dp_cell(row, col)
        

    def extend_beam(self, new_rows = 0, new_cols = 0):
        
        for row in range(new_rows):
            zero_row = np.zeros((1, self.dim_cols))
            self.beam = np.append(self.beam, zero_row, axis = 0)
            self.dp = np.append(self.dp, zero_row, axis = 0)
            self.dim_rows += 1
            for col in range(self.dim_cols//2, self.dim_cols):
                self.calculate_beam_cell(self.dim_rows-1, col)
                self.calculate_dp_cell(self.dim_rows-1, col)
        
        for col in range(new_cols):
            zero_col = np.zeros((self.dim_rows, 1))
            self.beam = np.append(self.beam, zero_col, axis = 1)
            self.dp = np.append(self.dp, zero_col, axis = 1)
            self.dim_cols += 1
            for row in range(self.dim_rows//2, self.dim_rows):
                self.calculate_beam_cell(row, self.dim_cols-1)
                self.calculate_dp_cell(row, self.dim_cols-1)


tb = TractorBeam(50, 50)
tb.populate_beam()

answer_1 = sum(sum(tb.beam))
print('answer_1', answer_1)

tb.populate_dp()

last_biggest_square = 0
last_bottom_right = (0, 0)
while tb.biggest_square < 100:
    dist_rows = tb.dim_rows - tb.bottom_right[0]
    dist_cols = tb.dim_cols - tb.bottom_right[1]
    
    if dist_rows > dist_cols:
        tb.extend_beam(0, 10)
    else:
        tb.extend_beam(10, 0)
        
    if last_biggest_square < tb.biggest_square:
        last_biggest_square = tb.biggest_square
        print('Got new biggest square', last_biggest_square,
              'at', tb.bottom_right, 'diff', tb.bottom_right[0] - last_bottom_right[0],
              tb.bottom_right[1] - last_bottom_right[1])
        last_bottom_right = tb.bottom_right

answer_2 = (last_bottom_right[1]-99) * 10000 + last_bottom_right[0]-99
print('answer_2', answer_2)

#This while loop takes a while, but while watching the results I spotted a pattern
#in the coords which got me the result faster. The pattern starts from:
#square size: 19, X: 169, Y: 191, and from then for every 1 more square size you add
#the below to X and Y respectively, recycling:
#
#8	9
#9	10
#8	9
#9	10
#12	14
#9	10
#8	9
#9	10
#8	9
#9	10
#12	14
#8	9
#9	10
#8	9
#9	10
#8	9
#13	15
