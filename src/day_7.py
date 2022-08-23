from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import cache as memoize
from operator import and_ as AND, lshift as LSHIFT, or_ as OR, rshift as RSHIFT
from typing import Union, NamedTuple

from benchmark import advent_problem
from data import day_7 as DATA

Scalar = int
Wire = Instruction = Expression = str
BinOp = NamedTuple("BinOp", left="Node", op=Callable, right="Node")
InvertOp = NamedTuple("InvertOp", operand="Node")
Node = Union["Scalar", "Wire", "BinOp", "InvertOp"]
INSTRUCTION_MAP = {"AND": AND, "OR": OR, "LSHIFT": LSHIFT, "RSHIFT": RSHIFT, "NOT": lambda x: ~x & 0xFFFF}


def _evaluate(obj):
    if isinstance(obj, str):
        return Scalar(obj) if obj.isnumeric() else obj
    return obj


class Circuit:
    __slots__ = ("_connections",)

    def __init__(self) -> None:
        self._connections: dict[Wire, Node] = {}

    def take_instruction(self, instruction: Instruction) -> None:
        """
        Takes an instruction and report it to the circuit frame for evaluation
        updating existing wires may not take effect as they are cached and requires
        artifacts to be invalidated

        Args:
            instruction (Instruction): the instruction string conforming to an assignment
        """
        expr, target = map(str.strip, instruction.split("->"))
        self.set_wire(target, expr)

    def set_wire(self, target: Wire, expression: Expression) -> None:
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

    def clear_cache(self) -> None:
        """
        Clears the internal cache for unparsing nodes
        """
        self._unparse.cache_clear()

    @classmethod
    def from_instructions(cls, instructions: Iterable[Instruction]) -> Circuit:
        """
        An convenience method for instantiating the class from a given iterable
        of instruction strings

        Args:
            instructions (Iterable[Instruction]): Instructions which should be taken

        Returns:
            Circuit: New Circuit instance
        """
        self = cls()
        for instruction in instructions:
            self.take_instruction(instruction)
        return self

    @memoize
    def _unparse(self, tree: Node) -> Scalar:
        """
        An internal helper method for recursively parsing the connections tree

        Args:
            tree (Node): The root of the tree from which parsing should be done

        Raises:
            ValueError: Not a valid node

        Returns:
            Scalar: The Scalar result which was produced from parsing
        """
        if isinstance(tree, Scalar):
            return tree
        if isinstance(tree, Wire):
            return self._unparse(self.get_node(tree))
        if isinstance(tree, BinOp):
            left, right = map(self._unparse, [tree.left, tree.right])
            return tree.op(left, right)
        if isinstance(tree, InvertOp):
            operand = self._unparse(tree.operand)
            return INSTRUCTION_MAP["NOT"](operand)
        raise ValueError(f"Expected node, found {tree!r}")

    def _form_node(self, expression: Expression) -> Node:
        """
        An internal helper method for forming a node from a given expression

        Args:
            expression (Expression): Left hand side of the assignment

        Returns:
            Node: Node formed from parsing LHS of the assignment
        """
        expr = expression.split()
        if len(expr) > 2:
            left, op, right = expr
            return BinOp(_evaluate(left), INSTRUCTION_MAP[op], _evaluate(right))
        if len(expr) > 1:
            _, operand = expr
            return InvertOp(_evaluate(operand))
        lone = expr.pop()
        return _evaluate(_evaluate(lone))


@advent_problem
def part_1(data=DATA):
    return Circuit.from_instructions(data.splitlines()).get_wire("a")


@advent_problem
def part_2(data=DATA):
    circuit = Circuit.from_instructions(data.splitlines())
    circuit.set_wire("b", str(circuit.get_wire("a")))
    circuit.clear_cache()
    return circuit.get_wire("a")


if __name__ == "__main__":
    part_1()
    part_2()
