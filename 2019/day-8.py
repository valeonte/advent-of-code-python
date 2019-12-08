# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 07:21:33 2019

@author: Eftychios
"""

import os
from typing import Iterator, Tuple, Dict

os.chdir("C:/Repos/advent-of-code-python")

class Image:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.layers = []
        
    def build(self, sequence: str):
        
        x = -1
        y = -1
        layer = None
        row = None
        for ch in sequence:
            pixel = int(ch)
            
            x += 1
            if x % self.width == 0:
                if row is not None and layer is not None:
                    layer.append(row)
                
                row = []
                y += 1
                x = 0
                
                if y % self.height == 0:
                    if layer is not None:
                        self.layers.append(layer)
                    layer = []
            
            row.append(pixel)
        
        layer.append(row)
        self.layers.append(layer)
    
    def get_visible_layer(self):
        
        ret = []
        row = []
        max_layer = len(self.layers)
        
        for row_idx in range(0, self.height):
            for pixel_idx in range(0, self.width):
                layer_idx = 0
                last_pixel = 2
                while last_pixel == 2 and layer_idx < max_layer:
                    last_pixel = self.layers[layer_idx][row_idx][pixel_idx]
                    layer_idx += 1
                
                row.append(last_pixel)

            ret.append(row)
            row = []
            
        
        return ret

    def print_layer(self, layer):
        for row in layer:
            print(''.join([str(pixel) for pixel in row]).replace('0', ' ').replace('1', '$').replace('2', ' '))



with open("2019/inputs/day8.txt", "r") as f:
    inp = f.read().strip()

img = Image(25, 6)
img.build(inp)

fewest_zeros = 1000000000
fewest_zero_layer = None
for layer in img.layers:
    zeros = 0
    zeros = sum([sum([1 for pixel in row if pixel == 0]) for row in layer])
    if zeros < fewest_zeros:
        fewest_zeros = zeros
        fewest_zero_layer = layer
        
ones = sum([sum([1 for pixel in row if pixel == 1]) for row in fewest_zero_layer])
twos = sum([sum([1 for pixel in row if pixel == 2]) for row in fewest_zero_layer])

answer_1 = ones * twos

print(answer_1)

visible_layer = img.get_visible_layer()
img.print_layer(visible_layer)


if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_1(self):
            img = Image(3, 2)
            img.build('123456789012')
            
            self.assertEqual(img.layers, [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]])

        def test_2(self):
            img = Image(2,2)
            img.build('0222112222120000')
            
            self.assertEqual(img.get_visible_layer(), [[0, 1], [1, 0]])

    unittest.main()
