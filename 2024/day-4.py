"""
Advent of Code 2024 day 4.

Created on Wed Dec 04 2024 9:27:01 PM

@author: Eftychios
"""

import os

from common import Dir


os.chdir("C:/Repos/advent-of-code-python/2024")

inp_string = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

with open("inputs/day-4.txt", "r") as f:
    inp_string = f.read()


letters = inp_string.split("\n")

max_x = len(letters[0]) - 1
max_y = len(letters) - 1


def has_xmas_at_direction(x: int, y: int, dir: Dir, search_word: str, char_idx: int = 0) -> bool:
    """Check whether there is valid XMAS following direction."""
    if x < 0 or x > max_x or y < 0 or y > max_y or letters[y][x] != search_word[char_idx]:
        return False
    if char_idx == len(search_word) - 1:
        return True
    new_x = x
    new_y = y
    if dir == Dir.N or dir == Dir.NW or dir == Dir.NE:
        new_y -= 1
    if dir == Dir.S or dir == Dir.SW or dir == Dir.SE:
        new_y += 1
    if dir == Dir.E or dir == Dir.SE or dir == Dir.NE:
        new_x += 1
    if dir == Dir.W or dir == Dir.SW or dir == Dir.NW:
        new_x -= 1
    
    return has_xmas_at_direction(new_x, new_y, dir, search_word, char_idx+1)


ret = 0
for x in range(max_x+1):
    for y in range(max_y+1):
        for dir in Dir:
            ret += has_xmas_at_direction(x, y, dir, 'XMAS')

print('Answer 1:', ret)


ret = 0
for x in range(max_x-1):
    for y in range(max_y-1):
        ret += ((has_xmas_at_direction(x, y, Dir.SE, 'MAS') or has_xmas_at_direction(x, y, Dir.SE, 'SAM'))
                and (has_xmas_at_direction(x+2, y, Dir.SW, 'MAS') or has_xmas_at_direction(x+2, y, Dir.SW, 'SAM')))

print('Answer 2:', ret)
