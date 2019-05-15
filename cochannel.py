# LabunskyA wrote this file
# Distributed under the Simplified BSD License

import string, time
from baudot import Baudot


class CoverChannelStateAPI:
    def send_bit(self, bit: bool, dest): raise NotImplementedError
    def receive_bit(self, src) -> bool: raise NotImplementedError
    def get_state(self, dest) -> bool: raise NotImplementedError


class CoverChannelEncoder:
    bit_lim = 0
    @staticmethod
    def encode(data: string) -> [int]: raise NotImplementedError
    @staticmethod
    def decode(data: [int]) -> string: raise NotImplementedError
    @staticmethod
    def get_sym(code: int): raise NotImplementedError


class CovertChannel:
    def __init__(self, api: CoverChannelStateAPI, endpoint, clock_len: int = 1, tail_nulls: int = 10,
                 verbose: bool = False, encoder: CoverChannelEncoder = Baudot):
        self.__api = api
        self.__api_clock = clock_len
        self.__tail_nuls = tail_nulls
        self.__endpoint = endpoint
        self.__state = False
        self.__verbose = verbose
        self.__encoder = encoder

    @staticmethod
    def __clock():
        return time.perf_counter()

    def __sync_on(self, clock):
        total_skipped = 0

        spent = self.__clock() - clock
        while spent >= self.__api_clock:
            skipped = int(spent / self.__api_clock)

            clock += skipped * self.__api_clock
            total_skipped += skipped

            spent = self.__clock() - clock + spent % self.__api_clock

        time.sleep(clock + self.__api_clock - self.__clock())
        return total_skipped

    def __send_bit(self, bit):
        if self.__state != bit:
            self.__api.send_bit(bit, self.__endpoint)
            self.__state = bit

    def __receive_bit(self) -> bool:
        return self.__api.receive_bit(self.__endpoint)

    def send(self, message):
        codes = self.__encoder.encode(message)
        self.send_raw(codes)

    def receive(self):
        return self.__encoder.decode(self.receive_raw())

    def receive_raw(self) -> [int]:
        clock = self.__clock()

        # Wait for the transmission to start
        self.__state = self.__receive_bit()
        while True:
            skipped = self.__sync_on(clock)
            clock += (skipped + 1) * self.__api_clock
            if self.__state != self.__receive_bit():
                break

        codes = []
        code = 0
        code_bit = 1

        nulls = 0
        while nulls <= self.__tail_nuls:
            skipped = self.__sync_on(clock)
            clock += (skipped + 1) * self.__api_clock

            while skipped > 0:
                skipped -= 1
                code_bit <<= 1
                if self.__verbose:
                    print("X", end="")
                if code_bit == self.__encoder.bit_lim:
                    codes.append(code)
                    if self.__verbose:
                        print("", self.__encoder.get_sym(code))
                    code = 0
                    code_bit = 1

            bit = self.__receive_bit()
            if bit:
                nulls = 0
                code |= code_bit
                if self.__verbose:
                    print("+", end="")
            else:
                nulls += 1
                if self.__verbose:
                    print("-", end="")

            code_bit <<= 1
            if code_bit == self.__encoder.bit_lim:
                codes.append(code)
                if self.__verbose:
                    print("", self.__encoder.get_sym(code))
                code = 0
                code_bit = 1

        return codes

    def send_raw(self, codes: [int]):
        self.__state = self.__api.get_state(self.__endpoint)
        clock = self.__clock()

        pos = 0
        code_bit = 1

        self.__send_bit(not self.__state)
        while True:
            skipped = self.__sync_on(clock)
            clock += (skipped + 1) * self.__api_clock
            while skipped > 0:
                skipped -= 1
                if self.__verbose:
                    print("X", end="")
                code_bit <<= 1
                if code_bit == self.__encoder.bit_lim:
                    if self.__verbose:
                        print("", self.__encoder.get_sym(codes[pos]))
                    pos += 1
                    code_bit = 1

            if pos >= len(codes):
                break

            bit = (codes[pos] & code_bit) != 0
            self.__send_bit(bit)

            if self.__verbose:
                if bit:
                    print("+", end="")
                else:
                    print("-", end="")

            code_bit <<= 1
            if code_bit == self.__encoder.bit_lim:
                if self.__verbose:
                    print("", self.__encoder.get_sym(codes[pos]))
                pos += 1
                code_bit = 1
        self.__send_bit(False)
