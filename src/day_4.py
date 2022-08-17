from hashlib import md5
from itertools import count

from benchmark import advent_problem
from data import day_4 as DATA


def _from_zero_count(data, zero_count):
    zero_prefix = "".zfill(zero_count)
    for num in count(start=1):
        if md5(f"{data}{num}".encode()).hexdigest().startswith(zero_prefix):
            return num


@advent_problem
def part_1(data=DATA):
    return _from_zero_count(data, 5)


@advent_problem
def part_2(data=DATA):
    return _from_zero_count(data, 6)


if __name__ == "__main__":
    part_1("a")
    part_2()
