from itertools import accumulate

from benchmark import advent_problem
from data import day_3 as DATA


def _conv(i):
    c, b, m = complex, bool, map
    gen = (c(m < 0x3F and (-b(m & 0x2) or 0x1), m > 0x5D and (-b(m & 0x21) or 0x1)) for m in m(ord, i))
    return set(accumulate(gen, initial=0))


@advent_problem
def part_1(data=DATA):
    return len(_conv(data))


@advent_problem
def part_2(data=DATA):
    return len(_conv(data[::2]) | _conv(data[1::2]))


if __name__ == "__main__":
    part_1()
    part_2()
