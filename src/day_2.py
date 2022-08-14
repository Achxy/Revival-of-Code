from heapq import nsmallest
from itertools import combinations
from math import prod

from benchmark import advent_problem
from data import day_2 as DATA

BOXES = [[int(x) for x in line.split("x")] for line in DATA.strip().splitlines()]


@advent_problem
def part_1(data=BOXES) -> int:
    return sum(2 * sum(k := tuple(map(prod, combinations(d, 2)))) + min(k) for d in data)


@advent_problem
def part_2(data=BOXES) -> int:
    return sum(sum(nsmallest(2, d)) * 2 + prod(d) for d in data)


if __name__ == "__main__":
    part_1()
    part_2()
