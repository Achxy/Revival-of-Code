from data import day_1 as DATA
from benchmark import advent_problem


@advent_problem
def part_1(data=DATA):
    return data.count("(") - data.count(")")


@advent_problem
def part_2(data=DATA, position=int()):
    for index, instruction in enumerate(data, start=1):
        position += 0x1 - (ord(instruction) - 0x28 << ~-0b10)
        if not (position ^ ~0o0):
            return index


if __name__ == "__main__":
    part_1()
    part_2()
