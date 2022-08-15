from ast import literal_eval

from benchmark import advent_problem
from data import day_8 as DATA

BACK_SLASH = "\\"


@advent_problem
def part_1(data=DATA):
    diff = 0
    for s in data.splitlines():
        diff += len(s)
        diff -= len(literal_eval(s))
    return diff
