# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 22:06:57 2019

@author: Eftychios
"""

import os
import time
from typing import Iterator, Tuple, Dict, List, NamedTuple
import numpy as np
import threading

os.chdir("C:/Repos/advent-of-code-python/2019")


from intcode_runner import IntcodeRunner


class Packet(NamedTuple):
    destination: int
    X: int
    Y: int

lock = threading.Lock()
nat = Packet(-1, -1, -1)
stop_threads = False

class NetworkBus:

    def __init__(self,
                 program: List[int]):
        self.queue: List[Packet] = []
        self.nics: List[IntcodeRunner] = []
        self.program = program

    def transmitter(self,
                    address: int) -> Iterator[int]:

        # always first send the address
        #print(f'Sent address to {address}')
        yield address

        while True:
            # for all subsequent inputs, check if there is anything to send
            if any(p.destination == address for p in self.queue):
                lock.acquire()
                try:
                    for i, p in enumerate(self.queue):
                        if p.destination == address:
                            #print(f'Sending packet {p.X}/{p.Y} to {address}')
                            yield p.X
                            yield p.Y

                            break

                    del self.queue[i]
                finally:
                    lock.release()

            else:
                yield -1

    def runner(self,
               address: int,
               nic: IntcodeRunner):

        nic_iter = nic.iter_run()
        while True:
            global stop_threads
            if stop_threads:
                break

            global nat
            p = Packet(
                    destination = next(nic_iter),
                    X = next(nic_iter),
                    Y = next(nic_iter)
                    )
            if p.destination == 255:
                print(f'Received NAT packet from {address}, {p}')
                nat = p
                continue

            self.queue.append(p)

            print(f'Received packet from {address}, {p}')


    def start_nic(self):

        address = len(self.nics)
        nic = IntcodeRunner(self.program,
                            extend=1000,
                            input_iterator=self.transmitter(address),
                            name=f'NIC {address}')
        self.nics.append(nic)

        print(f'Kicking off NIC {address}')
        thread = threading.Thread(target=self.runner, args=(address, nic))
        thread.start()

        return thread


with open("inputs/day23.txt", "r") as f:
    inp = [int(i) for i in f.read().split(',')]

bus = NetworkBus(inp)

threads = []
for i in range(50):
    #time.sleep(1)
    threads.append(bus.start_nic())
    print(f'Thread active count {threading.active_count()}')

last_nat_sent = Packet(1,1,1)
while True:
    print('Spinning...lock: ', lock.locked(), 'queue:', len(bus.queue))
    if nat.destination == 255 and len(bus.queue) == 0:
        to_send = Packet(0, nat.X, nat.Y)
        print('-----------------Empty queue, kicking things off:', to_send)
        if last_nat_sent.Y == to_send.Y:
            print('------------!!!!!!!!!!!!----------- got answer_2', to_send, last_nat_sent)
            break

        last_nat_sent = to_send
        bus.queue.append(Packet(0, nat.X, nat.Y))

    time.sleep(1)

stop_threads = True
