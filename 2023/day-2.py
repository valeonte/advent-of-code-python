"""
Advent of Code 2023 day 2.

Created on Sat Dec 02 2023

@author: Eftychios
"""

import os
import re


os.chdir("C:/Repos/advent-of-code-python/2023")

inp_string = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


with open("inputs/day-2.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")

games = []

p = re.compile(r'^(\d+) (blue|red|green)$')

for line in inp:
    sets_line = line[line.index(':') + 2:]
    game = []
    for ss in sets_line.split('; '):
        d = dict(red=0, green=0, blue=0)
        for s in ss.split(', '):
            m = p.match(s)
            num = int(m.group(1))
            colour = m.group(2)
            d[colour] = num
        game.append(d)

    games.append(game)

max_red = 12
max_green = 13
max_blue = 14
possible_sum = 0
for i, g in enumerate(games):
    impossible = False
    for draw in g:
        impossible = draw['red'] > max_red or draw['green'] > max_green or draw['blue'] > max_blue
        if impossible:
            break
    if not impossible:
        possible_sum += i + 1

print('Answer 1:', possible_sum)

power_sum = 0
for g in games:
    max_red = 0
    max_green = 0
    max_blue = 0
    for draw in g:
        if draw['red'] > max_red:
            max_red = draw['red']
        if draw['green'] > max_green:
            max_green = draw['green']
        if draw['blue'] > max_blue:
            max_blue = draw['blue']

    power_sum += max_red * max_green * max_blue

print('Answer 2:', power_sum)
