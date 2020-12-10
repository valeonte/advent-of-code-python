# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 22.

Created on Sat Dec 28 12:17:29 2019

@author: Eftychios
"""

import os
import time
import re
from typing import Iterator, Tuple, Dict, List


class DeckShuffler:
    """The shuffler class."""

    def deal_into_new_stack(self,
                            deck: List[int]) -> Iterator[Tuple[int, int]]:
        """Deal into a new stack."""
        # print(f'Dealing into new stack')

        size = len(deck)

        for pos, card in enumerate(deck):

            new_pos = size - pos - 1
            yield (new_pos, card)

    def cut_n_cards(self,
                    deck: List[int],
                    n: int) -> Iterator[Tuple[int, int]]:
        """Cut n cards."""
        # print(f'Cutting {n}')

        if n > 0:
            cut_off = n
        else:
            cut_off = len(deck) + n

        for i in range(cut_off, len(deck)):
            yield (i - cut_off, deck[i])

        for i in range(0, cut_off):
            yield (i + len(deck) - cut_off, deck[i])

    def deal_with_increment(self,
                            deck: List[int],
                            inc: int) -> Iterator[Tuple[int, int]]:
        """Deal with increment inc."""
        # print(f'Dealing with increment {inc}')

        last_index = -inc
        for card in deck:
            last_index = (last_index + inc) % len(deck)

            yield (last_index, card)

    def do_shuffle_command(self,
                           deck: List[int],
                           command: str) -> List[int]:
        """Run shuffle command."""
        iterator = None
        if command == "deal into new stack":
            iterator = self.deal_into_new_stack(deck)
        else:
            cutex = r'^cut ([\d-]+)$'
            m = re.search(cutex, command)
            if m:
                n = int(m.group(1))
                iterator = self.cut_n_cards(deck, n)
            else:
                incex = r'^deal with increment (\d+)$'
                m = re.search(incex, command)
                inc = int(m.group(1))
                iterator = self.deal_with_increment(deck, inc)

        if iterator is None:
            raise Exception(f"failed to parse command: {command}")

        shuffled = [-1] * len(deck)
        for pos, card in iterator:
            shuffled[pos] = card

        return shuffled

    def get_new_index_new_stack(self,
                                deck_size: int,
                                card_index: int) -> int:

        return deck_size - card_index - 1

    def get_prev_index_new_stack(self,
                                deck_size: int,
                                card_index: int) -> int:
        return self.get_new_index_new_stack(deck_size, card_index)

    def get_new_index_cut_n_cards(self,
                                  deck_size: int,
                                  card_index: int,
                                  n: int) -> int:

        if n > 0:
            cut_off = n
        else:
            cut_off = deck_size + n

        if card_index < cut_off:
            return deck_size - cut_off + card_index

        return card_index - cut_off

    def get_prev_index_cut_n_cards(self,
                                  deck_size: int,
                                  card_index: int,
                                  n: int) -> int:

        return (card_index + n) % deck_size

    def get_new_index_deal_with_increment(self,
                                          deck_size: int,
                                          card_index: int,
                                          inc: int) -> int:

        return card_index * inc % deck_size

    def get_prev_index_deal_with_increment(self,
                                           deck_size: int,
                                           card_index: int,
                                           inc: int) -> int:

        while card_index % inc != 0:
            card_index += deck_size

        return card_index // inc

    def get_new_index_command(self,
                              deck_size: int,
                              card_index: int,
                              command: str) -> List[int]:
        iterator = None
        if command == "deal into new stack":
            return self.get_new_index_new_stack(deck_size, card_index)

        cutex = "^cut ([\d-]+)$"
        m = re.search(cutex, command)
        if m:
            n = int(m.group(1))
            return self.get_new_index_cut_n_cards(deck_size, card_index, n)

        incex = "^deal with increment (\d+)$"
        m = re.search(incex, command)
        inc = int(m.group(1))
        return self.get_new_index_deal_with_increment(deck_size, card_index, inc)

    def get_prev_index_command(self,
                               deck_size: int,
                               card_index: int,
                               command: str) -> List[int]:
        iterator = None
        if command == "deal into new stack":
            return self.get_prev_index_new_stack(deck_size, card_index)

        cutex = "^cut ([\d-]+)$"
        m = re.search(cutex, command)
        if m:
            n = int(m.group(1))
            return self.get_prev_index_cut_n_cards(deck_size, card_index, n)

        incex = "^deal with increment (\d+)$"
        m = re.search(incex, command)
        inc = int(m.group(1))
        return self.get_prev_index_deal_with_increment(deck_size, card_index, inc)

    def get_prev_index_full_shuffle(self,
                                    deck_size: int,
                                    card_index: int) -> int:
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 12)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 62)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -9633)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 66)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -2776)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 7)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 8053)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 4283)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 56)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 33)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -8783)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 57)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -7349)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 46)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -412)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 14)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 5612)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 62)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -7555)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 13)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -1983)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 19)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -8998)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 50)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 8131)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 29)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -5300)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 75)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -3297)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 21)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 6945)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 32)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 23)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 9409)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 30)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 2910)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 20)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -9537)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 13)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 7294)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 23)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 4222)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 23)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 3754)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 3867)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 73)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -7026)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 10)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 4009)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 48)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -1754)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 63)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 5774)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 60)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -8349)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 42)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -2316)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 21)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -6859)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 59)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 6080)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 56)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 2873)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 3)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -1038)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 61)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -5330)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 5)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 9150)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 44)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -8095)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 40)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -2391)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 25)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 4074)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 32)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -9939)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 59)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 5290)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 50)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -337)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 27)
        card_index = self.get_prev_index_new_stack(deck_size, card_index)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, -4435)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 23)
        card_index = self.get_prev_index_cut_n_cards(deck_size, card_index, 6859)
        card_index = self.get_prev_index_deal_with_increment(deck_size, card_index, 41)

        return card_index



with open("inputs/day22.txt", "r") as f:
    inp = f.read()


ds = DeckShuffler()

deck = list(range(10007))

for command in inp.splitlines():
    deck = ds.do_shuffle_command(deck, command)

answer_1 = deck.index(2019)
print('answer_1', answer_1)

commands = inp.splitlines()
commands.reverse()
index = answer_1

for target in range(10007):
    index = ds.get_prev_index_full_shuffle(10007, target)

    if index != deck[target]:
        print('Failed!')
        break



# confirmed with original example

cnt = 0
index = 2020
start = time.process_time()
deck_size = 119315717514047
for rep in range(101741582076661):
    index = ds.get_prev_index_full_shuffle(deck_size, index)

    if cnt % 100000 == 0:
        dt = time.process_time() - start
        est = dt*(101741582076661 - rep)/100000/3600
        print(cnt, 'dt:', dt, 'sec, est: ', est, 'hours')
        start = time.process_time()


    cnt +=1

    if index == 2020:
            print(cnt, index)
            break



if __name__ == "__main__":

    import unittest

    class TestAll(unittest.TestCase):

        def test_1(self):
            ds = DeckShuffler()

            deck = list(range(0, 10))
            shuffled = ds.do_shuffle_command(deck, "deal into new stack")

            self.assertListEqual(shuffled, [9,8,7,6,5,4,3,2,1,0])

            for card in deck:
                self.assertEqual(ds.get_new_index_command(len(deck),
                                                          card,
                                                          "deal into new stack"),
                                 shuffled.index(card))

            for i, card in enumerate(shuffled):
                self.assertEqual(ds.get_prev_index_command(len(deck),
                                                           i,
                                                           "deal into new stack"), card)

        def test_2(self):
            ds = DeckShuffler()

            deck = list(range(0, 10))
            shuffled = ds.do_shuffle_command(deck, "cut 3")

            self.assertListEqual(shuffled, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

            for card in deck:
                self.assertEqual(ds.get_new_index_command(len(deck),
                                                          card,
                                                          "cut 3"),
                                 shuffled.index(card))

            for i, card in enumerate(shuffled):
                self.assertEqual(ds.get_prev_index_command(len(deck),
                                                           i,
                                                           "cut 3"), card)

        def test_3(self):
            ds = DeckShuffler()

            deck = list(range(0, 10))
            shuffled = ds.do_shuffle_command(deck, "cut -4")

            self.assertListEqual(shuffled, [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

            for card in deck:
                self.assertEqual(ds.get_new_index_command(len(deck),
                                                          card,
                                                          "cut -4"),
                                 shuffled.index(card))

            for i, card in enumerate(shuffled):
                self.assertEqual(ds.get_prev_index_command(len(deck),
                                                           i,
                                                           "cut -4"), card)

        def test_4(self):
            ds = DeckShuffler()

            deck = list(range(0, 10))
            shuffled = ds.do_shuffle_command(deck, "deal with increment 3")

            self.assertListEqual(shuffled, [0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

            for card in deck:
                self.assertEqual(ds.get_new_index_command(len(deck),
                                                          card,
                                                          "deal with increment 3"),
                                 shuffled.index(card))

            for i, card in enumerate(shuffled):
                self.assertEqual(ds.get_prev_index_command(len(deck),
                                                           i,
                                                           "deal with increment 3"), card)

    unittest.main()
