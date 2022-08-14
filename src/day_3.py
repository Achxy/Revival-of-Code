from itertools import accumulate

from benchmark import advent_problem
from data import day_3 as DATA

ORIGIN = {0}
MOVE_INSTRUCTION = {"^": 1j, "v": -1j, "<": 1, ">": -1}


def _conv(instructions):
    return set(accumulate(MOVE_INSTRUCTION[move] for move in instructions))


@advent_problem
def part_1(data=DATA):
    return len(ORIGIN | _conv(data))


@advent_problem
def part_2(data=DATA):
    return len(ORIGIN | _conv(data[::2]) | _conv(data[1::2]))


if __name__ == "__main__":
    part_1()
    part_2()
