# LabunskyA wrote this file
# Distributed under the Simplified BSD License

import string


class Baudot:
    # ITA-2 code table
    __ITA_2 = (
        ('', ''),
        ('E', '3'),
        ('\n', '\n'),
        ('A', '-'),
        (' ', ' '),
        ('S', '\7'),
        ('I', '8'),
        ('U', '7'),
        ('\r', '\r'),
        ('D', '$'),
        ('R', '\''),
        ('J', '4'),
        ('N', ','),
        ('F', '!'),
        ('C', ':'),
        ('K', '('),
        ('T', '5'),
        ('Z', '"'),
        ('L', ')'),
        ('W', '2'),
        ('H', '#'),
        ('Y', '6'),
        ('P', '0'),
        ('Q', '1'),
        ('O', '9'),
        ('B', '?'),
        ('G', '&'),
        (0, 0), # LTRS
        ('M', '.'),
        ('X', '/'),
        ('V', ';'),
        (1, 1)  # FIGS
    )

    __ITA_2_rev = {
        'A': 3, '-': 3,
        'B': 25, '?': 25,
        'C': 14, ':': 14,
        'D': 9, '$': 9,
        'E': 1, '3': 1,
        'F': 13, '!': 13,
        'G': 26, '&': 26,
        'H': 20, '#': 20,
        'I': 6, '8': 6,
        'J': 11, '4': 11,
        'K': 15, '(': 15,
        'L': 18, ')': 18,
        'M': 28, '.': 28,
        'N': 12, ',': 12,
        'O': 24, '9': 24,
        'P': 22, '0': 22,
        'Q': 23, '1': 23,
        'R': 10, '\'': 10,
        'S': 5, '\7': 5,
        'T': 16, '5': 16,
        'U': 7, '7': 7,
        'V': 30, ';': 30,
        'W': 19, '2': 19,
        'X': 29, '/': 29,
        'Y': 21, '6': 21,
        'Z': 17, '"': 17,
        '\n': 2, '\r': 8,
        ' ': 4, '': 0,
        # States switch codes
        0: 27, 1: 31
    }

    __STATES = (
        0,  # LTRS
        1   # FIGS
    )

    bit_lim = 32 # 5 bit-code

    @staticmethod
    def get_sym(code: int):
        return Baudot.__ITA_2[code][0], Baudot.__ITA_2[code][1]

    @staticmethod
    def decode(codes: [int]):
        state = 0
        decoded = []
        for code in codes:
            if code < 0 or code > 31:
                raise
            symbol = Baudot.__ITA_2[code][state]
            if symbol not in Baudot.__STATES:
                decoded.append(symbol)
            else:
                state = symbol
        return ''.join(decoded)

    @staticmethod
    def encode(message: string):
        state = 0
        encoded = []
        for symbol in message:
            symbol = symbol.upper()
            if symbol in Baudot.__ITA_2_rev:
                code = Baudot.__ITA_2_rev[symbol]
                if Baudot.__ITA_2[code][state] != symbol:
                    state ^= 1
                    encoded.append(Baudot.__ITA_2_rev[state])
                encoded.append(code)
        return encoded
