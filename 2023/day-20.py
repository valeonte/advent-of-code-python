"""
Advent of Code 2023 day 20.

Created on Wed Dec 20 2023 11:04:42 PM

@author: Eftychios
"""

import os
import json
import re
import math

import numpy as np

from typing import Tuple, Set, Iterator, Dict, List
from dataclasses import dataclass, replace
from enum import Enum

os.chdir("C:/Repos/advent-of-code-python/2023")

part1 = False

inp_string = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

inp_string = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

with open("inputs/day-20.txt", "r") as f:
    inp_string = f.read()

debug = False

class Pulse(Enum):
    Low: int = 0
    High: int = 1


class Module:
    def __init__(self, name: str):
        self.name = name

        self.inputs = dict()
        self.outputs = dict()
    
    def add_input(self, module: 'Module'):
        self.inputs[module.name] = module
    
    def add_output(self, module: 'Module'):
        self.outputs[module.name] = module
    
    def process_pulse(self, pulse: Pulse, source_module: 'Module') -> Pulse:
        if debug:
            print(source_module.name, pulse, '->', self.name)
    
    def __repr__(self) -> str:
        return self.__class__.__name__ + ' ' + self.name


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)

        self.state_on = False
    
    def process_pulse(self, pulse: Pulse, source_module: Module) -> Pulse:
        super().process_pulse(pulse, source_module)

        if pulse == Pulse.Low:
            if self.state_on:
                self.state_on = False
                return Pulse.Low

            self.state_on = True
            return Pulse.High

        return None


class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name)

        self.pulse_received = dict()
    
    def add_input(self, module: Module):
        super().add_input(module)

        self.pulse_received[module.name] = Pulse.Low
    
    def process_pulse(self, pulse: Pulse, source_module: Module) -> Pulse:
        super().process_pulse(pulse, source_module)

        self.pulse_received[source_module.name] = pulse
        all_high = True
        for p in self.pulse_received.values():
            if p == Pulse.Low:
                all_high = False
                break
        if all_high:
            return Pulse.Low
        return Pulse.High


class Broadcaster(Module):
    def __init__(self, name: str):
        super().__init__(name)
    
    def process_pulse(self, pulse: Pulse, source_module: Module) -> Pulse:
        super().process_pulse(pulse, source_module)

        return pulse


# Registering modules
modules = dict()
for inp in inp_string.split('\n'):
    ps = inp.split(' -> ')
    name = ps[0]
    outputs = ps[1]
    if name == 'broadcaster':
        modules['broadcaster'] = Broadcaster('broadcaster')
        continue
    if name[0] == '%':
        modules[name[1:]] = FlipFlop(name[1:])
        continue
    if name[0] == '&':
        modules[name[1:]] = Conjunction(name[1:])
        continue

# Adding inputs/outputs
for inp in inp_string.split('\n'):
    ps = inp.split(' -> ')
    name = ps[0]
    if name[0] in ['%', '&']:
        name = name[1:]
    
    module = modules[name]
    if ',' in ps[1]:
        outputs = ps[1].split(', ')
    else:
        outputs = [ps[1]]

    for output in outputs:
        if output not in modules:
            print('Adding dummy module', output)
            modules[output] = Module(output)

        module.add_output(modules[output])
        modules[output].add_input(module)


if part1:
    pulse_counter = {Pulse.Low: 0, Pulse.High: 0}
    for i in range(1000):
        if debug:
            print('------------------------------------- Button press', i + 1)
        queue = [(modules['broadcaster'], Pulse.Low)]
        pulse_counter[Pulse.Low] += 1
        while queue:
            module, pulse = queue.pop(0)
            for output in module.outputs.values():
                pulse_counter[pulse] += 1
                new_pulse = output.process_pulse(pulse, module)
                if new_pulse is not None:
                    queue.append((output, new_pulse))


    print('Answer 1:', pulse_counter[Pulse.Low] * pulse_counter[Pulse.High])

    raise SystemExit(0)

high_emit_rounds = dict(rd=[], bt=[], fv=[], pr=[])
pulse_counter = {Pulse.Low: 0, Pulse.High: 0}
button_press = 0
while True:
    all_done_ones = True
    for her in high_emit_rounds.values():
        if len(her) == 0:
            all_done_ones = False
            break
    if all_done_ones:
        break

    button_press += 1
    queue = [(modules['broadcaster'], Pulse.Low)]
    pulse_counter[Pulse.Low] += 1
    while queue:
        module, pulse = queue.pop(0)
        if pulse == Pulse.High and module.name in high_emit_rounds:
            print(module.name, 'emits high on press', button_press)
            high_emit_rounds[module.name].append(button_press)

        for output in module.outputs.values():
            if output == 'rx':
                print('checking')
            pulse_counter[pulse] += 1
            new_pulse = output.process_pulse(pulse, module)
            if new_pulse is not None:
                queue.append((output, new_pulse))


print('Answer 2:', math.lcm(*[v[0] for v in high_emit_rounds.values()]))
