# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 10.

Created on Fri Dec 10 08:15:43 2021

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

with open("inputs/day-10.txt", "r") as f:
    inp_string = f.read()


inp = inp_string.split("\n")

illegal_chars = []

bracket_map = {'[': ']',
               '(': ')',
               '<': '>',
               '{': '}'}

score = {')': 1, ']': 2, '}': 3, '>': 4}
completion_scores = []
for row in inp:
    open_brackets = []
    is_illegal = False
    for ch in row:
        if ch in bracket_map:
            open_brackets.append(ch)
        else:
            last_opener = open_brackets.pop()
            is_illegal = bracket_map[last_opener] != ch
            if is_illegal:
                illegal_chars.append(ch)
                break

    if is_illegal or len(open_brackets) == 0:
        continue

    completion_score = 0
    open_brackets.reverse()
    for o in open_brackets:
        c = bracket_map[o]
        completion_score = completion_score * 5 + score[c]

    completion_scores.append(completion_score)

#    break


score = {')': 3, ']': 57, '}': 1197, '>': 25137}

print('Answer 1:', sum([score[ch] for ch in illegal_chars]))

print('Answer 2:', sorted(completion_scores)[len(completion_scores) // 2])
