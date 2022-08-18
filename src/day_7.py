from __future__ import annotations
from collections.abc import Callable
from benchmark import advent_problem
from data import day_7 as DATA
from functools import cache
from typing import NamedTuple, TypeAlias
from operator import and_, or_, lshift, rshift

Scalar = int
Wire = str
Node: TypeAlias = "BinOp | UnaryOp | Scalar | Wire"
Operator = Callable[[Scalar, Scalar], Scalar]
INSTRUCTION_MAP = {"AND": and_, "OR": or_, "LSHIFT": lshift, "RSHIFT": rshift, "NOT": lambda x: ~x & 0xFFFF}


class BinOp(NamedTuple):
    left: Node
    op: Operator
    right: Node


class UnaryOp(NamedTuple):
    operand: Node


class Circuit:
    def __init__(self) -> None:
        self._connections: dict = {}

    def take_instruction(self, instruction: str):
        expr, target = map(str.strip, instruction.split("->"))
        self.set_wire(target, expr)

    def set_wire(self, target: str, value: str):
        self._connections[target] = self._form_connection(value)

    def get_wire(self, wire: Wire):
        found = self._connections[wire]
        return self._unparse_tree(found)

    def clear_cache(self):
        self._unparse_tree.cache_clear()

    @classmethod
    def from_instructions(cls, instructions: list[str]) -> Circuit:
        self = cls()
        for instruction in instructions:
            self.take_instruction(instruction)
        return self

    @cache
    def _unparse_tree(self, tree: Node):
        if isinstance(tree, Scalar):
            return tree
        if isinstance(tree, Wire):
            ptr = self._connections[tree]
            return self._unparse_tree(ptr)
        if isinstance(tree, UnaryOp):
            op = INSTRUCTION_MAP["NOT"]
            value = self._unparse_tree(tree.operand)
            return op(value)
        if isinstance(tree, BinOp):
            _left, op, _right = tree.left, tree.op, tree.right
            left, right = map(self._unparse_tree, [_left, _right])
            return op(left, right)

    def _form_connection(self, expression: str):
        expr = expression.split()
        if len(expr) > 2:
            _left, _op, _right = expr
            left, right = map(self._evaluate, [_left, _right])
            op = INSTRUCTION_MAP[_op]
            return BinOp(left=left, op=op, right=right)
        if len(expr) > 1:
            _, _operand = expr
            operand = self._evaluate(_operand)
            return UnaryOp(operand=operand)
        lone = expr.pop()
        return Scalar(lone) if lone.isnumeric() else lone

    def _evaluate(self, value: str):
        if value.isnumeric():
            return Scalar(value)
        return self._connections.get(value, value)

    @property
    def connections(self):
        return self._connections.items()


@advent_problem
def part_1(data=DATA):
    return Circuit.from_instructions(data.splitlines()).get_wire("a")


if __name__ == "__main__":
    part_1()
