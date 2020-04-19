# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 09:26:38 2020

@author: Eftychios
"""

import os
import time

os.chdir("C:/Repos/advent-of-code-python/2017")

with open("inputs/day19.txt", "r") as f:
    inp = f.read()


class Router:
    def __init__(self, diagram: str):
        self.routing_diagram = diagram.split('\n')
        self.width = max([len(row) for row in self.routing_diagram])
        self.height = len(self.routing_diagram)
        self.cur_row = 0
        self.cur_char = self.routing_diagram[0].find('|')
        self.direction = 'S'
        self.step_counter = 1

    def try_move_south(self) -> bool:
        if (self.height > self.cur_row + 1 and
                len(self.routing_diagram[self.cur_row + 1]) > self.cur_char and
                self.routing_diagram[self.cur_row + 1][self.cur_char] != ' '):
            self.cur_row += 1
            return True

        return False

    def try_move_north(self) -> bool:
        if (self.cur_row > 0 and
                len(self.routing_diagram[self.cur_row - 1]) > self.cur_char and
                self.routing_diagram[self.cur_row - 1][self.cur_char] != ' '):
            self.cur_row -= 1
            return True

        return False

    def try_move_east(self) -> bool:
        if (len(self.routing_diagram[self.cur_row]) > self.cur_char + 1 and
                self.routing_diagram[self.cur_row][self.cur_char + 1] != ' '):
            self.cur_char += 1
            return True

        return False

    def try_move_west(self) -> bool:
        if (self.cur_char > 0 and
                self.routing_diagram[self.cur_row][self.cur_char - 1] != ' '):
            self.cur_char -= 1
            return True

        return False

    def print_map(self):
        for (idx, row) in enumerate(self.routing_diagram):
            if idx == self.cur_row:
                print(row[0:self.cur_char] + '#' + row[self.cur_char + 1:])
            else:
                print(row)

    def try_move(self) -> bool:
        if self.direction == 'S':
            if self.try_move_south():
                return True
            if self.try_move_east():
                self.direction = 'E'
                return True
            self.direction = 'W'
            return self.try_move_west()

        if self.direction == 'N':
            if self.try_move_north():
                return True
            if self.try_move_east():
                self.direction = 'E'
                return True
            self.direction = 'W'
            return self.try_move_west()

        if self.direction == 'W':
            if self.try_move_west():
                return True
            if self.try_move_north():
                self.direction = 'N'
                return True
            self.direction = 'S'
            return self.try_move_south()

        if self.direction == 'E':
            if self.try_move_east():
                return True
            if self.try_move_north():
                self.direction = 'N'
                return True
            self.direction = 'S'
            return self.try_move_south()

    def run(self, debug_delay: int = 0) -> str:
        ret = ''
        paths = '|-+'
        while self.try_move():
            self.step_counter += 1
            ch = self.routing_diagram[self.cur_row][self.cur_char]
            if ch not in paths:
                ret += ch

            if debug_delay > 0:
                self.print_map()
                time.sleep(debug_delay)

        return ret


r = Router(inp)
print(r.run())


if __name__ == '__main__':

    import unittest

    class TestAll(unittest.TestCase):

        def test_init(self):
            r = Router("""    |
   |""")

            self.assertEqual(r.width, 5)
            self.assertEqual(r.height, 2)
            self.assertEqual(r.cur_row, 0)
            self.assertEqual(r.cur_char, 4)

        def test_try_move_south_1(self):
            r = Router("""    |
    |""")

            self.assertTrue(r.try_move_south())
            self.assertEqual(r.cur_row, 1)

        def test_try_move_south_2(self):
            r = Router("""    |
   |""")

            self.assertFalse(r.try_move_south())

        def test_try_move_north(self):
            r = Router("""    |
    |""")

            r.try_move_south()
            self.assertTrue(r.try_move_north())
            self.assertEqual(r.cur_row, 0)

        def test_try_move_east_1(self):
            r = Router("""    |
    +-""")

            r.try_move_south()
            self.assertTrue(r.try_move_east())
            self.assertEqual(r.cur_row, 1)
            self.assertEqual(r.cur_char, 5)

        def test_try_move_east_2(self):
            r = Router("""    |
    +""")

            r.try_move_south()
            self.assertFalse(r.try_move_east())

        def test_try_move_west_1(self):
            r = Router("""    |
   -+""")

            r.try_move_south()
            self.assertTrue(r.try_move_west())
            self.assertEqual(r.cur_row, 1)
            self.assertEqual(r.cur_char, 3)

        def test_try_move_west_2(self):
            r = Router("""    |
    +""")

            r.try_move_south()
            self.assertFalse(r.try_move_west())

        def test_run(self):
            inp = """     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+ """

            r = Router(inp)
            self.assertEqual(r.run(), 'ABCDEF')
            self.assertEqual(r.step_counter, 38)


    unittest.main()
