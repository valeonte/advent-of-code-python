"""
Advent of Code 2023 day 4.

Created on Mon Dec 04 2023

@author: Eftychios
"""

import os
import re

from typing import List

os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


with open("inputs/day-4.txt", "r") as f:
    inp_string = f.read()


class Card:
    def __init__(self,
                 no: int,
                 winners: List[int],
                 drawn: List[int]):
        self.no = no
        self.winners = winners
        self.drawn = drawn

        self.won = sum([d in winners for d in drawn])

    def __repr__(self):
        return f'Card {self.no}, won {self.won}'


inp = inp_string.split("\n")

total_score = 0
cards = dict()
for line in inp:
    m = re.match(r'^Card\s+(?P<no>\d+):(?P<winners>(\s*\d+\s+)+)\|(?P<drawn>(\s*\d+\s*?)+)$', line)
    card_no = int(m.group('no'))
    winners = set([int(num) for num in m.group('winners').split(' ') if len(num) > 0])
    drawn = [int(num) for num in m.group('drawn').split(' ') if len(num) > 0]

    card = Card(card_no, winners, drawn)
    cards[card_no] = card
    if card.won > 0:
        total_score += 2 ** (card.won - 1)

print('Answer 1:', total_score)

cnt = 0
cards_occurences = {no: 1 for no in cards.keys()}
for no in range(len(cards)):
    card = cards[no + 1]
    occurs = cards_occurences[no + 1]
    cnt += occurs
    for add_no in range(card.won):
        cards_occurences[card.no + add_no + 1] += occurs

print('Answer 2:', cnt)
