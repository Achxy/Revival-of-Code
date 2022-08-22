# TODO: This can be refactored, making part 2 work first...
from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import cache
from operator import and_ as bin_and, lshift, or_ as bin_or, rshift
from typing import TypeAlias, Union
from ast import BinOp, UnaryOp

from benchmark import advent_problem
from data import day_7 as DATA

Scalar = int
Wire = Instruction = Expression = str
Node: TypeAlias = Union["Scalar", "Wire", "BinOp", "UnaryOp"]
INSTRUCTION_MAP = {
    "AND": bin_and,
    "OR": bin_or,
    "LSHIFT": lshift,
    "RSHIFT": rshift,
    "NOT": lambda x: ~x & 0xFFFF,
}


class Circuit:
    def __init__(self) -> None:
        self._connections: dict[Wire, Node] = {}

    def take_instruction(self, instruction: Instruction):
        """
        Takes an instruction and report it to the circuit frame for evaluation
        updating existing wires may not take effect as they are cached and requires
        artifacts to be invalidated

        Args:
            instruction (Instruction): the instruction string conforming to an assignment
        """
        expr, target = map(str.strip, instruction.split("->"))
        self.set_wire(target, expr)

    def set_wire(self, target: Wire, expression: Expression):
        """
        Takes an target wire and an expression which evaluates to a bounded scalar product
        The wire is mapped or overwritten to the expression contents thereafter

        Args:
            target (Wire): Wire to which the the expression should be binded.
            expression (Expression): Expression which produces an scalar result
        """
        self._connections[target] = self._form_connection(expression)

    def get_wire(self, wire: Wire) -> Scalar:
        """
        Takes an wire and attempt to parse the associated tree in an attempt to find scalar product
        A NameError exception may be raised by an dict lookup if an non-existent wire is referenced

        Args:
            wire (Wire): The wire which should be looked up

        Returns:
            Scalar: The scalar product which was an evaluated result of the tree parsing
        """
        tree = self.get_node(wire)
        return self._unparse_tree(tree)

    def get_node(self, name: str) -> Node:
        return self._connections[name]

    def clear_cache(self):
        self._unparse_tree.cache_clear()

    @classmethod
    def from_instructions(cls, instructions: Iterable[Instruction]) -> Circuit:
        self = cls()
        for instruction in instructions:
            self.take_instruction(instruction)
        return self

    @cache
    def _unparse_tree(self, tree: Node) -> Scalar:
        if isinstance(tree, Scalar):
            return tree
        if isinstance(tree, Wire):
            ptr = self.get_node(tree)
            return self._unparse_tree(ptr)
        if isinstance(tree, InvertOp):
            op = INSTRUCTION_MAP["NOT"]
            value = self._unparse_tree(tree.operand)
            return op(value)
        if isinstance(tree, BinOp):
            _left, op, _right = tree.left, tree.op, tree.right
            left, right = map(self._unparse_tree, [_left, _right])
            return op(left, right)

    def _form_connection(self, expression: Expression) -> Node:
        expr = expression.split()
        if len(expr) > 2:
            _left, _op, _right = expr
            left, right = map(self._evaluate, [_left, _right])
            op = INSTRUCTION_MAP[_op]
            return BinOp(left=left, op=op, right=right)
        if len(expr) > 1:
            _, _operand = expr
            operand = self._evaluate(_operand)
            return InvertOp(operand=operand)
        lone = expr.pop()
        return Scalar(lone) if lone.isnumeric() else lone

    def _evaluate(self, value: Expression) -> Node:
        if value.isnumeric():
            return Scalar(value)
        return self._connections.get(value, value)


@advent_problem
def part_1(data=DATA):
    return Circuit.from_instructions(data.splitlines()).get_wire("a")


@advent_problem
def part_2(data=DATA):
    # FIXME: ???
    # Cache seems to get invalidated properly but we are getting the same values
    # for both parts
    circuit = Circuit.from_instructions(data.splitlines())
    # circuit.clear_cache()
    circuit.set_wire("b", "3176")
    circuit.clear_cache()
    return circuit.get_wire("a")


if __name__ == "__main__":
    part_1()
    part_2()
