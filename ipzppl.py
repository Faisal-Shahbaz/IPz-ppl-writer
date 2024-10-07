import math
import sympy


class pump:

    def __init__(
        self,
        file,
        dia,
        time=0,
    ):
        self.file = file
        self.dia = dia
        self.time = time
        self.loop = []

    def init(*args):
        for self in args:
            self.file.write(f"dia {self.dia}\nal 1\nbp 1\nPF 0\n")

    def rat(self, rate: int, vol: int, dir: str):
        self.file.write(f"\nphase\nfun rat\nrat {rate} mm\nvol {vol}\ndir {dir}\n")
        self.time += vol / rate * 60 * self.getloop()

    def pas(self, length: int):
        if length <= 99:
            self.file.write(f"\nphase\nfun pas {length}\n")
            self.time += length * self.getloop()

        elif length <= 99 * 3:
            self.pas(99)
            self.pas(length - 99)
        else:
            multiples = factor_check(decompose_dict(sympy.factorint(length)))
            if multiples != (0, 0) and len(multiples) <= 3:
                for i in range(len(multiples) - 1):
                    self.loopstart(multiples[1 + i])
                self.pas(multiples[0])
                for i in range(len(multiples) - 1):
                    self.loopend()
            else:
                self.pas(length % 50, self.getloop())
                length -= length % 50
                self.pas(length, self.getloop())

    def loopstart(self, count):
        self.loop.append(count)
        if len(self.loop) > 3:
            raise Exception("Up to three nested loops, you have too many")
        self.file.write(f"\nphase\nfun lps\n")

    def loopend(self):
        self.file.write(f"\nphase\nfun lop {self.loop.pop()}\n")

    def getloop(self):
        if len(self.loop) >= 1:
            return self.loop[-1]
        else:
            return sympy.prod(self.loop)

    def stop(*args):
        for self in args:
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


class masterppl:
    """
    Based on maseter ppl file made by Tim Burgess,
    SyringePumpPro https://SyringePumpPro.com
    timb@syringepumppro.com
    Find example file by Tim on SyringPumpPro manual
    All code is original, by me
    """
    def __init__(self, file, adrs=[]):
        self.file = file
        self.adrs = adrs

    def add(self, adr: int, ppl: pump):
        self.adrs.append(adr)
        self.file.write(f"Set adr={adr}\n")
        self.file.write(f"call {ppl.file.name}\n")

    def clearall(self):
        for adr in self.adrs:
            self.file.write(f"{adr}cldinf\n{adr}cldwdr\n{adr}dis\n")

    def beepall(self):
        for adr in self.adrs:
            self.file.write(f"{adr}buz13\n")
    
    def quickset(self, all: dict):
        for tuples in all.items():
            self.add(*tuples)
        self.clearall()
        self.beepall()


def decompose_dict(dict: dict) -> list:
    r = []
    for key in dict:
        for i in range(dict[key]):
            r.append(key)
    return r


def factor_check(initial_factor, attempt=0) -> tuple:

    if isinstance(initial_factor, int):
        initial_factor = decompose_dict(sympy.factorint(initial_factor))

    if not isinstance(initial_factor, list):
        raise Exception("initial_factor should be int or list")

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
