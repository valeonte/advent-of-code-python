# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 20.

Created on Mon Dec 20 21:19:03 2021

@author: Eftychios
"""

import os

import numpy as np


os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""  # noqa


with open("inputs/day-20.txt", "r") as f:
    inp_string = f.read()


def print_image(image: np.array):
    """Visual representation of the image."""
    for row in range(image.shape[0]):
        s = ''
        for col in range(image.shape[1]):
            s = s + ('#' if image[row, col] else '.')
        print(s)


algo = None
image = []
for inp in inp_string.split("\n"):
    if algo is None:
        algo = [ch == '#' for ch in inp]
        continue

    if len(inp) == 0:
        continue

    image.append([ch == '#' for ch in inp])

image = np.array(image)
new_image = np.zeros((image.shape[0] + 6, image.shape[1] + 6),
                     dtype=bool)
new_image[3:3 + image.shape[0], 3: 3 + image.shape[1]] = image
image = new_image

mult = [256, 128, 64, 32, 16, 8, 4, 2, 1]
for enh in range(2):
    print_image(image)
    print('---------------------------------------------')
    new_image = np.zeros((image.shape[0] - 2, image.shape[1] - 2), dtype=bool)
    for row in range(image.shape[0] - 2):
        for col in range(image.shape[1] - 2):
            square = image[row:row + 3, col: col + 3]
            idx = sum(np.reshape(square, 9) * mult)
            new_image[row, col] = algo[idx]

    image = new_image
    new_image = np.zeros((image.shape[0] + 6, image.shape[1] + 6),
                         dtype=bool)
    new_image[:] = image[0, 0]
    new_image[3:3 + image.shape[0], 3: 3 + image.shape[1]] = image
    image = new_image


print_image(new_image)
print('Answer 1:', new_image.sum())


for enh in range(2, 50):
    print('Enhancement', enh, 'of 50')
    new_image = np.zeros((image.shape[0] - 2, image.shape[1] - 2), dtype=bool)
    for row in range(image.shape[0] - 2):
        for col in range(image.shape[1] - 2):
            square = image[row:row + 3, col: col + 3]
            idx = sum(np.reshape(square, 9) * mult)
            new_image[row, col] = algo[idx]

    image = new_image
    new_image = np.zeros((image.shape[0] + 6, image.shape[1] + 6),
                         dtype=bool)
    new_image[:] = image[0, 0]
    new_image[3:3 + image.shape[0], 3: 3 + image.shape[1]] = image
    image = new_image

print('Answer 2:', new_image.sum())
