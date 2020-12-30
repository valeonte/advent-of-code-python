# -*- coding: utf-8 -*-
"""
Day 18 Advent of Code 2020 file.

Created on Wed Dec 30 18:04:19 2020

@author: Eftychios
"""

import os

from typing import Iterator


os.chdir("C:/Repos/advent-of-code-python/2020")

inp_string = "1 + 2 * 3 + 4 * 5 + 6"
inp_string = "1 + (2 * 3) + (4 * (5 + 6))"
inp_string = "2 * 3 + (4 * 5)"
inp_string = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"

with open("inputs/day-18.txt", "r") as f:
    inp_string = f.read()


def amend_plain_formula(formula: str) -> Iterator[str]:
    """Amend the formula by adding all appropriate parenthesis."""
    chars = formula.split(' ')
    yield '(' * int((len(chars) - 1)/2)

    for i, ch in enumerate(chars):
        yield ch
        if i > 0 and i % 2 == 0:
            yield ')'


def calculate_formula(formula: str) -> int:
    """Calculate the formula."""
    last_open_bracket = -1
    for i, ch in enumerate(formula):
        if ch == '(':
            last_open_bracket = i
        elif ch == ')':
            if last_open_bracket < 0:
                raise Exception('Impossible!')
            bracket = formula[last_open_bracket:i + 1]
            bracket_result = calculate_formula(bracket[1:-1])

            new_formula = formula.replace(bracket, str(bracket_result))
            return calculate_formula(new_formula)

    return eval(''.join(amend_plain_formula(formula)))


answer_1 = 0
for formula in inp_string.split('\n'):
    answer_1 += calculate_formula(formula)

print('Answer 1:', answer_1)


def amend_plain_formula2(formula: str) -> Iterator[str]:
    """Amend the formula by adding all appropriate parenthesis."""
    elements = formula.split(' ')

    num1 = elements[0]
    for i in range(1, len(elements), 2):
        sign = elements[i]
        num2 = elements[i + 1]
        if sign == '*':
            yield num1
            yield sign
            num1 = num2
        else:
            num1 = str(int(num1) + int(num2))

    yield num1


def calculate_formula2(formula: str) -> int:
    """Calculate the formula."""
    last_open_bracket = -1
    for i, ch in enumerate(formula):
        if ch == '(':
            last_open_bracket = i
        elif ch == ')':
            if last_open_bracket < 0:
                raise Exception('Impossible!')
            bracket = formula[last_open_bracket:i + 1]
            bracket_result = calculate_formula2(bracket[1:-1])

            new_formula = formula.replace(bracket, str(bracket_result))
            return calculate_formula2(new_formula)

    return eval(''.join(amend_plain_formula2(formula)))


answer_2 = 0
for formula in inp_string.split('\n'):
    answer_2 += calculate_formula2(formula)

print('Answer 2:', answer_2)
