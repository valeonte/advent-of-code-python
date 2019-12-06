# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 20:19:10 2019

@author: Eftychios
"""

import math
from typing import Iterator


class PasswordTester:
    
    def GetDigits(self, passcode: int) -> Iterator[int]:
        for i in str(passcode):
            yield int(i)


    def Passes(self, passcode: int) -> bool:
        
        cnt = 0
        last_digit = -1
        got_same = False
        for digit in self.GetDigits(passcode):
            cnt += 1
            
            # got descending
            if digit < last_digit:
                return False
            
            # check for same
            if last_digit == digit:
                got_same = True
        
            last_digit = digit
            
        if cnt != 6:
            return False
        
        return got_same

    def Passes2(self, passcode: int) -> bool:
        if not self.Passes(passcode):
            return False
        
        same_seq = 0
        last_digit = -1
        got_exactly_2 = False
        for digit in self.GetDigits(passcode):
            
            if last_digit == digit:
                same_seq += 1
            else:
                # group stopped, did it stop at 2?
                if same_seq == 2:
                    got_exactly_2 = True
                    
                same_seq = 1
            
            last_digit = digit
        
        return got_exactly_2 or same_seq == 2

pt = PasswordTester()

pt.Passes(111111)
pt.Passes2(111122)

passed1 = 0
passed2 = 0
for passcode in range(235741, 706949):
    if pt.Passes(passcode):
        passed += 1
        
        if pt.Passes2(passcode):
            passed2 += 1
        
answer_1 = passed
answer_2 = passed2

print(answer_1, answer_2)
