# TODO: This can be refactored, making part 2 work first...
from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import cache as memoize
from operator import and_ as bin_and, lshift, or_ as bin_or, rshift
from typing import TypeAlias, Union
from ast import AST
from typing_extensions import reveal_type

from benchmark import advent_problem
from data import day_7 as DATA

Scalar = int
Wire = Instruction = Expression = str
Node: TypeAlias = Union["Scalar", "Wire", "BinOp", "InvertOp"]
INSTRUCTION_MAP = {
    "AND": bin_and,
    "OR": bin_or,
    "LSHIFT": lshift,
    "RSHIFT": rshift,
    "NOT": lambda x: ~x & 0xFFFF,
}


def _evaluate(obj):
    if isinstance(obj, str):
        return Scalar(obj) if obj.isnumeric() else obj
    return obj


class BinOp(AST):
    __slots__ = ("left", "op", "right")

    def __init__(self, left: Node, op: str, right: Node) -> None:
        self.left = _evaluate(left)
        self.op: Callable = INSTRUCTION_MAP[op]
        self.right = _evaluate(right)


class InvertOp(AST):
    __slots__ = ("operand",)

    def __init__(self, operand: Node) -> None:
        self.operand = _evaluate(operand)


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
        self._connections[target] = self._form_node(expression)

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
        return self._unparse(tree)

    def get_node(self, name: str) -> Node:
        """
        Takes an name and returns the node associated with the name stored in the internal connections
        pool, chained names are cleared before returning, as such it can be ensured that returned name is not
        a wire itself

        Args:
            name (str): The name to search

        Returns:
            Node: The node associated with the name
        """
        node = self._connections[name]
        if isinstance(node, str):
            return Scalar(node) if node.isnumeric() else self.get_node(node)
        return node

    @classmethod
    def from_instructions(cls, instructions: Iterable[Instruction]) -> Circuit:
        self = cls()
        for instruction in instructions:
            self.take_instruction(instruction)
        return self

    @memoize
    def _unparse(self, tree: Node) -> Scalar:
        if isinstance(tree, Scalar):
            return tree
        if isinstance(tree, Wire):
            node = self.get_node(tree)
            return self._unparse(node)
        if isinstance(tree, BinOp):
            left, right = map(self._unparse, [tree.left, tree.right])
            return tree.op(left, right)
        if isinstance(tree, InvertOp):
            operand = self._unparse(tree.operand)
            return INSTRUCTION_MAP["NOT"](operand)
        raise ValueError(f"Expected node, found {tree!r}")

    def _form_node(self, expression: Expression) -> Node:
        expr = expression.split()
        if len(expr) > 2:
            return BinOp(*expr)
        if len(expr) > 1:
            _, operand = expr
            return InvertOp(operand=operand)
        lone = expr.pop()
        return _evaluate(lone)


@advent_problem
def part_1(data=DATA):
    return Circuit.from_instructions(data.splitlines()).get_wire("a")


@advent_problem
def part_2(data=DATA):
    circuit = Circuit.from_instructions(data.splitlines())
    circuit.set_wire("b", str(circuit.get_wire("a")))
    circuit._unparse.cache_clear()
    return circuit.get_wire("a")


if __name__ == "__main__":
    part_1()
    part_2()
