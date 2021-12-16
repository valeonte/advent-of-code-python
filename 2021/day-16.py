# -*- coding: utf-8 -*-
"""
Advent of Code 2021 day 16.

Created on Thu Dec 16 10:31:01 2021

@author: Eftychios
"""

import os

from typing import Iterator

os.chdir("C:/Repos/advent-of-code-python/2021")

inp_string = "D2FE28"  # literal
inp_string = "38006F45291200"  # type 0 subpackets
inp_string = "EE00D40C823060"  # type 1 subpackets
inp_string = "8A004A801A8002F478"
inp_string = "620080001611562C8802118E34"
inp_string = "C0015000016115A2E0802F182340"
inp_string = "A0016C880162017C3686B18A3D4780"

inp_string = "C200B40A82"
inp_string = "04005AC33890"
inp_string = "880086C3E88112"
inp_string = "CE00C43D881120"
inp_string = "D8005AC2A8F0"
inp_string = "F600BC2D8F"
inp_string = "9C005AC2F8F0"
inp_string = "9C0141080250320F1802104A08"

with open("inputs/day-16.txt", "r") as f:
    inp_string = f.read()


class Packet:
    """Packet representation."""

    def __init__(self, hex_def: str = None, bin_def: str = None):
        if bin_def is None:
            self.bits = bin(int(hex_def, 16))[2:]
            while len(self.bits) % 4 != 0:
                self.bits = '0' + self.bits

            if hex_def[0] == '0':
                self.bits = '0000' + self.bits
        else:
            self.bits = bin_def

        self.version = int(self.bits[0:3], 2)
        self.type_id = int(self.bits[3:6], 2)
        self.value = None

        self.bits_used = 6

        self.is_literal = self.type_id == 4
        if self.is_literal:
            print('Packet version', self.version, 'of type', self.type_id,
                  'and literal', self.get_literal())
        else:
            print('Packet version', self.version, 'of type', self.type_id)

    def get_value(self) -> int:
        """Get the value of the Packet."""
        if self.value is not None:
            return self.value
        if self.is_literal:
            return self.get_literal()

        vals = []
        for p in self.get_subpackets():
            val = p.get_value()
            vals.append(val)

        p = self
        if p.type_id == 0:  # sum
            return sum(vals)
        if p.type_id == 1:  # product
            ret = 1
            for v in vals:
                ret = ret * v
            return ret
        if p.type_id == 2:  # minimum
            return min(vals)
        if p.type_id == 3:  # maximum
            return max(vals)
        if p.type_id == 5:  # greater than
            return int(vals[0] > vals[1])
        if p.type_id == 6:  # less than
            return int(vals[0] < vals[1])
        if p.type_id == 7:  # equals
            return int(vals[0] == vals[1])

    def get_literal(self) -> int:
        """Extract packet's literal."""
        if not self.is_literal:
            raise Exception('Not literal!')
        if self.value is not None:
            return self.value

        num_str = ''
        inp = self.bits[6:]
        while inp[0] == '1':
            num_str = num_str + inp[1:5]
            inp = inp[5:]
            self.bits_used = self.bits_used + 5

        num_str = num_str + inp[1:5]
        self.bits_used = self.bits_used + 5

        self.value = int(num_str, 2)
        return self.value

    def round_up_bits_used(self):
        """Round up bits used taking into account hex representation."""
        mod = self.bits_used % 4
        if mod > 0:
            self.bits_used = self.bits_used + 4 - mod

    def get_subpackets0(self, total_length: int) -> Iterator:
        """Enumerate subpackets of type 0 packet."""
        self.bits_used = 22
        start_bits_used = self.bits_used
        while total_length > self.bits_used - start_bits_used:
            bin_def = self.bits[self.bits_used:]
            p = Packet(bin_def=bin_def)
            yield p

            if not p.is_literal:
                for _ in p.get_subpackets():
                    pass

            self.bits_used = self.bits_used + p.bits_used

    def get_subpackets1(self, total_subpackets: int) -> Iterator:
        """Enumerate subpackets of type 1 packet."""
        self.bits_used = 18
        subpackets_returned = 0
        while subpackets_returned < total_subpackets:
            bin_def = self.bits[self.bits_used:]
            p = Packet(bin_def=bin_def)
            yield p

            if not p.is_literal:
                for _ in p.get_subpackets():
                    pass

            self.bits_used = self.bits_used + p.bits_used
            subpackets_returned = subpackets_returned + 1

    def get_subpackets(self) -> Iterator:
        """Enumerate all sub packets in packet."""
        if self.is_literal:
            # Literal, no subpackets
            return

        self.length_type_id = int(self.bits[6])
        self.bits_used = 7

        if self.length_type_id == 0:
            total_length = self.bits[7: 22]
            self.bits_used = 22

            total_length = int(total_length, 2)
            for p in self.get_subpackets0(total_length):
                yield p
        else:
            total_subpackets = self.bits[7: 18]
            self.bits_used = 18

            total_subpackets = int(total_subpackets, 2)
            for p in self.get_subpackets1(total_subpackets):
                yield p


packets = [Packet(inp_string)]
version_sum = 0
while len(packets) > 0:
    p = packets.pop(0)
    version_sum = version_sum + p.version
    for pp in p.get_subpackets():
        packets.append(pp)

print('Answer 1:', version_sum)


p = Packet(inp_string)
print('Answer 2:', p.get_value())
