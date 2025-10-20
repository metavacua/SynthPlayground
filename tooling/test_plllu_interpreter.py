import unittest
import sys
import os
from collections import Counter

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.plllu_interpreter import (
    FourValuedInterpreter,
    LogicValue,
    InterpretationError,
)


class TestPlllUInterpreter(unittest.TestCase):

    def setUp(self):
        self.interpreter = FourValuedInterpreter()

    def test_atom_consumption(self):
        context = Counter({("A", 1): 1})
        ast = ("atom", (LogicValue.TRUE, ("A", 1)))
        val, rem = self.interpreter._evaluate(ast, context)
        self.assertEqual(val, LogicValue.TRUE)
        self.assertEqual(len(rem), 0)

    def test_unary_operators(self):
        context = Counter({("A", 1): 1})
        ast = ("unary_op", "∘", ("atom", (LogicValue.BOTH, ("A", 1))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.FALSE)

        context = Counter({("A", 1): 1})
        ast = ("unary_op", "~", ("atom", (LogicValue.TRUE, ("A", 1))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.FALSE)

    def test_additive_conjunction_shared_resource(self):
        # A & A with a single shared resource A:T
        context = Counter({("A", 1): 1})
        ast = (
            "binary_op",
            "&",
            ("atom", (LogicValue.TRUE, ("A", 1))),
            ("atom", (LogicValue.TRUE, ("A", 1))),
        )
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.TRUE)

    def test_additive_conjunction_different_resources(self):
        # A & B with context A:T, B:T -> Fails linearity
        context = Counter({("A", 1): 1, ("B", 1): 1})
        ast = (
            "binary_op",
            "&",
            ("atom", (LogicValue.TRUE, ("A", 1))),
            ("atom", (LogicValue.TRUE, ("B", 1))),
        )
        with self.assertRaisesRegex(
            InterpretationError, "branches consume different resources"
        ):
            self.interpreter.interpret(ast, context)

    def test_paraconsistency_with_shared_resource(self):
        # A & ~A with a single shared resource A:B
        context = Counter({("A", 1): 1})
        ast = (
            "binary_op",
            "&",
            ("atom", (LogicValue.BOTH, ("A", 1))),
            ("unary_op", "~", ("atom", (LogicValue.BOTH, ("A", 1)))),
        )
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.BOTH)

    def test_implication_precondition(self):
        # Test A:B, C:T |- A -o C => Fails because ∘A is FALSE, and C is unconsumed.
        context = Counter({("A", 1): 1, ("C", 1): 1})
        ast = (
            "binary_op",
            "-o",
            ("atom", (LogicValue.BOTH, ("A", 1))),
            ("atom", (LogicValue.TRUE, ("C", 1))),
        )
        with self.assertRaisesRegex(InterpretationError, "resources were not consumed"):
            self.interpreter.interpret(ast, context)

        # Test A:T, C:T |- A -o C => TRUE
        context = Counter({("A", 1): 1, ("C", 1): 1})
        ast = (
            "binary_op",
            "-o",
            ("atom", (LogicValue.TRUE, ("A", 1))),
            ("atom", (LogicValue.TRUE, ("C", 1))),
        )
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.TRUE)

    def test_modalities_are_transparent_and_linear(self):
        # Test ?A -> A
        context = Counter({("A", 1): 1})
        ast = ("unary_op", "?", ("atom", (LogicValue.TRUE, ("A", 1))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.TRUE)

        # Test §A -> A
        context = Counter({("A", 1): 1})
        ast = ("unary_op", "§", ("atom", (LogicValue.FALSE, ("A", 1))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.FALSE)

        # Test that they fail linearity if a resource is left over
        context = Counter({("A", 1): 1, ("B", 1): 1})
        ast = ("unary_op", "§", ("atom", (LogicValue.TRUE, ("A", 1))))
        with self.assertRaisesRegex(InterpretationError, "resources were not consumed"):
            self.interpreter.interpret(ast, context)


if __name__ == "__main__":
    unittest.main()
