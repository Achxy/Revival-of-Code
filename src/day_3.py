from itertools import accumulate

from benchmark import advent_problem
from data import day_3 as DATA


def _conv(i):
    return set(accumulate(({"^": 1j, "v": -1j, "<": 1, ">": -1}[k] for k in i), initial=0))


@advent_problem
def part_1(data=DATA):
    return len(_conv(data))


@advent_problem
def part_2(data=DATA):
    return len(_conv(data[::2]) | _conv(data[1::2]))


if __name__ == "__main__":
    part_1()
    part_2()
