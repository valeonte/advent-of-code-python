"""
Advent of Code 2023 day 7.

Created on Thu Dec 07 2023

@author: Eftychios
"""

import os
import math

from typing import List
from dataclasses import dataclass
from collections import namedtuple

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


with open("inputs/day-7.txt", "r") as f:
    inp_string = f.read()

inp = inp_string.split('\n')

card_value = {'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
for i in range(8):
    card_value[str(i + 2)] = i


@dataclass
class Hand:
    hand: str
    bid: int

    calc_value: int = -1

    def value(self) -> int:
        """Evaluate the hand."""
        if self.calc_value > 0:
            return self.calc_value

        self.calc_value = self.do_calc_value(self.hand)
        return self.calc_value

    def do_calc_value(self, raw_hand: str):
        base_value = 0
        for i, card in enumerate(reversed(self.hand)):
            base_value += card_value[card] * 13**i
        
        i += 1
        hand_power = self.get_hand_power(raw_hand)

        return hand_power * 13**i + base_value

    def value_joker(self) -> int:
        """Evaluate the hand."""
        if self.calc_value > 0:
            return self.calc_value

        if 'J' not in self.hand:
            self.calc_value = self.do_calc_value(self.hand)
            return self.calc_value

        max_calc_value = 0
        for card in card_value.keys():
            if card == 'J':
                continue
            try_hand = self.hand.replace('J', card)
            val = self.do_calc_value(try_hand)
            if val > max_calc_value:
                max_calc_value = val

        self.calc_value = max_calc_value

        return self.calc_value

    def get_hand_power(self, raw_hand: str):
        """Evaluate the hand type, and return the appropriate power."""
        freq = dict()
        for card in raw_hand:
            if card in freq:
                freq[card] += 1
            else:
                freq[card] = 1
        if len(freq) == 1:
            return 6  # 5 of a kind, a single type of card
        max_freq = max(freq.values())
        if max_freq == 4:
            return 5  # 4 of a kind
        if len(freq) == 2:
            return 4  # Full house, two distinct types of card, and not 4 of a kind
        if max_freq == 3:
            return 3  # 3 of a kind, for 3 the same without full house
        if len(freq) == 3:
            return 2  # Two pair, for 3 types of cards, with no 3 of a kind
        if max_freq == 2:
            return 1  # One pair

        return 0


# We will evaluate the hands on a 13-base system
hands = []
for line in inp:
    raw_hand = line[:5]
    bid = int(line[6:])
    
    hands.append(Hand(raw_hand, bid))

winnings = 0
for rank, hand in enumerate(sorted(hands, key=lambda x: x.value())):
    winnings += (rank + 1) * hand.bid

print('Answer 1:', winnings)


for key in card_value.keys():
    if card_value[key] < 9:
        card_value[key] += 1

card_value['J'] = 0

hands = []
for line in inp:
    raw_hand = line[:5]
    bid = int(line[6:])
    
    hands.append(Hand(raw_hand, bid))

winnings = 0
for rank, hand in enumerate(sorted(hands, key=lambda x: x.value_joker())):
    winnings += (rank + 1) * hand.bid

print('Answer 2:', winnings)
