from itertools import pairwise

from benchmark import advent_problem
from data import day_5 as DATA

VOWELS = tuple("aeiou")
PROHIBITED_SUBSTRINGS = ("ab", "cd", "pq", "xy")


def _is_nice_p1(s: str):
    return (
        sum(s.count(v) for v in VOWELS) >= 3
        and any(p == q for p, q in zip(s, s[1:]))
        and not any(ps in s for ps in PROHIBITED_SUBSTRINGS)
    )


def _is_nice_p2(s: str):
    return any(
        s.find(substr, index + 2) > 0 for index, substr in enumerate(map("".join, pairwise(s)))
    ) and any(s[i] == s[i + 2] for i in range(len(s) - 2))


@advent_problem
def part_1(data=DATA):
    return sum(_is_nice_p1(string) for string in data.splitlines())


@advent_problem
def part_2(data=DATA):
    return sum(_is_nice_p2(string) for string in data.splitlines())


if __name__ == "__main__":
    part_1()
    part_2()
