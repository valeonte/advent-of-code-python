# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 20:17:58 2019

@author: Eftychios
"""

import numpy as np
import os
os.chdir("C:/Repos/advent-of-code-python/2017")

from hasher import Hasher

disk = np.zeros((128,128), np.int32)

for i in range(0, 128):
    h = Hasher(256)
    h.process_string(f"hxtvlmkl-{i}")
    #h.process_string(f"flqrgnkx-{i}")

    j = 0
    for one in h.hash_bits():
        if one:
            disk[i][j] = 1
        
        j += 1

answer_1 = sum([sum(row) for row in disk])

def tag_group(x, y, group):
    if x < 0 or x > 127 or y < 0 or y > 127:
        return
    
    if disk[x][y] != 1:
        return
    
    disk[x][y] = group
    tag_group(x-1, y, group)
    tag_group(x, y-1, group)
    tag_group(x+1, y, group)
    tag_group(x, y+1, group)


group_cnt = 0

for x in range(0, 128):
    for y in range(0, 128):
        
        if disk[x][y] <= 0:
            continue
        
        group_cnt += 1
        group = -group_cnt
        tag_group(x, y, group)
        
answer_2 = group_cnt

print(answer_1, answer_2)


if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_1(self):
            
            used = 0
            for i in range(0, 128):
                h = Hasher(256)
                h.process_string(f"flqrgnkx-{i}")
            
                for one in h.hash_bits():
                    if one:
                        used += 1

            self.assertEqual(used, 8108)

    unittest.main()
