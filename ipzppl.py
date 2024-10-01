import math
import sympy

class pump:

    def __init__(self, file, dia, time=0):
        self.file = file
        self.dia = dia
        self.time = time

    def init(self):
        self.file.write(f"dia {self.dia}\nal 1\nbp 1\nPF 0\n")

    def rat(self, rate: int, vol: int, dir: str, loops=1):
        self.file.write(f"\nphase\nfun rat\nrat {rate} mm\nvol {vol}\ndir {dir}\n")
        self.time += vol / rate * 60 * loops

    def pas(self, length: int, loops=1):
        if length <= 99:
            self.file.write(f"\nphase\nfun pas {length}\n")
            self.time += length * loops

        elif length <= 99 * 3:
            self.pas(99, loops)
            self.pas(length - 99, loops)
        else:
            multiples = factor_check(
                decompose_dict(sympy.factorint(length))
            )
            if multiples != (0, 0):
                for i in range(len(multiples) - 1):
                    self.lps()
                self.pas(multiples[0], sympy.prod(multiples[1:]) * loops)
                for i in range(len(multiples) - 1):
                    self.lop(multiples[1 + i])
            else:
                self.pas(length % 50, loops)
                length -= length % 50
                self.pas(length, loops)

    def lps(self):
        self.file.write(f"\nphase\nfun lps\n")

    def lop(self, count):
        self.file.write(f"\nphase\nfun lop {count}\n")

    def stop(self):
        self.file.write(f"\nphase\nfun stp\n")

    def sync(*args):
        max_time = 0
        for arg in args:
            if arg.time > max_time:
                max_time = arg.time
        for arg in args:
            time_diff = max_time - arg.time
            if time_diff > 0:
                arg.pas(math.ceil(time_diff))


def decompose_dict(dict: dict) -> list:
    r = []
    for key in dict:
        for i in range(dict[key]):
            r.append(key)
    return r

def factor_check(initial_factor, attempt=0) -> tuple:

    if isinstance(initial_factor, int):
        initial_factor=decompose_dict(sympy.factorint(initial_factor))

    if not isinstance(initial_factor,list):
        raise Exception('initial_factor should be int or list')

    if any(x > 99 for x in initial_factor):
        return (0, 0)
    factor = initial_factor.copy()
    a = 0
    b = 0
    i = 0
    if len(factor) == 1:
        return (0, 0)
    while i < len(factor):
        if factor[i] * factor[i + 1] < 99:
            factor[i + 1] = factor[i] * factor[i + 1]
            factor[i] = 1
            i += 1
        else:
            a = factor[i]
            factor[i] = 1
            i = len(factor)
    b = sympy.prod(factor)
    if b <= 99:
        return (a, b)
    else:
        return (a, factor_check(decompose_dict(sympy.factorint(b))))

