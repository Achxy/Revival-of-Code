from itertools import accumulate

from benchmark import advent_problem
from data import day_3 as DATA


SANTA_PATH = slice(None, None, 2)
ROBO_SANTA_PATH = slice(1, None, 2)


def _conv(i):
    gen = (complex(m < 0x3F and (-bool(m & 0x2) or 0x1), m > 0x5D and (-bool(m & 0x21) or 0x1)) for m in map(ord, i))
    return set(accumulate(gen, initial=0))


@advent_problem
def part_1(data=DATA):
    return len(_conv(data))


@advent_problem
def part_2(data=DATA):
    santa, robot = data[SANTA_PATH], data[ROBO_SANTA_PATH]
    return len(_conv(santa) | _conv(robot))


if __name__ == "__main__":
    part_1()
    part_2()
