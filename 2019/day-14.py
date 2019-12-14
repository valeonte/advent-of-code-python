# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:37:16 2019

@author: Eftychios
"""

import os
import time
import math
from typing import Iterator, Tuple, Dict, List

os.chdir("C:/Repos/advent-of-code-python/2019")

class Ingredient:
    def __init__(self,
                 ingredient: str):
        parts = ingredient.split(' ')
        
        self.quantity = int(parts[0])
        self.chemical = parts[1]
    
    def __repr__(self):
        return f'{self.quantity} {self.chemical}'


class Reaction:
    def __init__(self,
                 produces: Ingredient,
                 consumes: List[Ingredient]):
        self.produces = produces
        self.consumes = consumes

    def __repr__(self):
        return ', '.join([str(c) for c in self.consumes]) + f' => {self.produces}'

class NanoFactory:
    def __init__(self,
                 reactions: str):

        self.reactions: Dict[str, Reaction] = dict()
        self.stock: Dict[str, int] = dict()
        
        for row in reactions.split('\n'):
            parts = row.split(' => ')
            produces = Ingredient(parts[1])
            consumes = [Ingredient(c) for c in parts[0].split(', ')]
            
            reaction = Reaction(produces, consumes)
            self.reactions[produces.chemical] = reaction
            self.stock[produces.chemical] = 0

    
    def get_ore_needed_for(self,
                           quantity: int,
                           chemical: str) -> int:
        
        if chemical == "ORE":
            return quantity
        
        stock = self.stock[chemical]
        if stock >= quantity:
            self.stock[chemical] = stock - quantity
            return 0
        
        self.stock[chemical] = 0
        quantity = quantity - stock
        reaction = self.reactions[chemical]
        reactions_needed = math.ceil(quantity / reaction.produces.quantity)
        
        total_ore = 0
        for ingredient in reaction.consumes:
            total_ore += self.get_ore_needed_for(reactions_needed*ingredient.quantity,
                                                 ingredient.chemical)
        
        produced_quantity = reactions_needed * reaction.produces.quantity
        self.stock[chemical] = produced_quantity - quantity
        return total_ore
    
    def get_max_fuel_from_ore(self, ore_quantity: int) -> int:
        
        max_ore_for_one = self.get_ore_needed_for(1, 'FUEL')
        fuel_produced = 1
        remaining_ore = ore_quantity - max_ore_for_one
        
        while True:
            
            affordable = remaining_ore//max_ore_for_one
            if affordable == 0:
                affordable = 1
                
            ore_consumed = self.get_ore_needed_for(affordable, 'FUEL')
            remaining_ore -= ore_consumed
            if remaining_ore <= 0:
                return fuel_produced

            fuel_produced += affordable

with open("inputs/day14.txt", "r") as f:
    inp = f.read()

f = NanoFactory(inp)
answer_1 = f.get_ore_needed_for(1, 'FUEL')

f = NanoFactory(inp)
answer_2 = f.get_max_fuel_from_ore(1000000000000)

print(answer_1, answer_2)

if __name__ == '__main__':

    import unittest
    
    class TestAll(unittest.TestCase):

        def test_1(self):
            reactions = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_ore_needed_for(1, 'FUEL'), 31)
            
        def test_2(self):
            reactions = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_ore_needed_for(1, 'FUEL'), 165)

        def test_3(self):
            reactions = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_ore_needed_for(1, 'FUEL'), 13312)

        def test_3_b(self):
            reactions = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_max_fuel_from_ore(1000000000000), 82892753)

        def test_4(self):
            reactions = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_ore_needed_for(1, 'FUEL'), 180697)

        def test_4_b(self):
            reactions = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_max_fuel_from_ore(1000000000000), 5586022)

        def test_5(self):
            reactions = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_ore_needed_for(1, 'FUEL'), 2210736)

        def test_5_b(self):
            reactions = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
            
            f = NanoFactory(reactions)
            self.assertEqual(f.get_max_fuel_from_ore(1000000000000), 460664)

    unittest.main()
