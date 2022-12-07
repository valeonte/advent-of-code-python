# -*- coding: utf-8 -*-
"""
Advent of Code 2022 day 7.

Created on Wed Dec  7 21:28:13 2022

@author: Eftychios
"""

import os


os.chdir("C:/Repos/advent-of-code-python/2022")

inp_string = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

with open("inputs/day-7.txt", "r") as f:
    inp_string = f.read()


class File:
    def __init__(self, ls_row: str):
        parts = ls_row.split(' ')
        self.name = parts[1]
        self.size = int(parts[0])

    def __repr__(self) -> str:
        return f'{self.name} (file, size={self.size})'


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.parent_dir = None

        self.subdirs = []
        self.files = []

    def __repr__(self) -> str:
        return f'{self.name} (dir, {len(self.subdirs)} subdirs, {len(self.files)} files)'  # noqa

    def get_size(self) -> int:
        """Calculate directory size."""
        size = 0
        for f in self.files:
            size += f.size
        for d in self.subdirs:
            size += d.get_size()

        return size


root = None
cur_dir = None
all_dirs = []

for row in inp_string.split('\n'):
    if row == '$ ls':
        continue

    if row == '$ cd ..':
        cur_dir = cur_dir.parent_dir
        continue

    if row.startswith('$ cd '):
        dir_name = row[5:]
        if cur_dir is None:
            cur_dir = Directory(dir_name)
            root = cur_dir
            all_dirs.append(cur_dir)
            continue

        cur_dir = [d for d in cur_dir.subdirs
                   if d.name == dir_name][0]
        continue

    if row.startswith('dir'):
        dir_name = row.split(' ')[-1]
        new_dir = Directory(dir_name)
        new_dir.parent_dir = cur_dir
        cur_dir.subdirs.append(new_dir)
        all_dirs.append(new_dir)
        continue

    if row[0].isnumeric():
        cur_dir.files.append(File(row))
        continue

    raise Exception(f'Unexpected line: {row}')


sum_of_sizes = 0
for d in all_dirs:
    d_size = d.get_size()
    if d_size <= 100000:
        sum_of_sizes += d_size

print('Answer 1:', sum_of_sizes)


unused_space = 70000000 - root.get_size()
missing_space = 30000000 - unused_space

min_diff = 100000000
best_dir = None
for d in all_dirs:
    d_size = d.get_size()
    excess = d_size - missing_space
    if excess < 0:
        continue
    if excess < min_diff:
        best_dir = d
        min_diff = excess

print('Best delete dir', best_dir, 'with size', best_dir.get_size())
