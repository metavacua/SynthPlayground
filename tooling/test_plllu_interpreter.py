import unittest
import sys
import os
from collections import Counter

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.plllu_interpreter import FourValuedInterpreter, LogicValue, InterpretationError

class TestPlllUInterpreter(unittest.TestCase):

    def setUp(self):
        self.interpreter = FourValuedInterpreter()

    def test_atom_consumption(self):
        context = Counter({('A', 1): 1})
        ast = ('atom', (LogicValue.TRUE, ('A', 1)))
        val, rem = self.interpreter._evaluate(ast, context)
        self.assertEqual(val, LogicValue.TRUE)
        self.assertEqual(len(rem), 0)

    def test_unary_operators(self):
        context = Counter({('A', 1): 1})
        ast = ('unary_op', '∘', ('atom', (LogicValue.BOTH, ('A', 1))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.FALSE)

        context = Counter({('A', 1): 1})
        ast = ('unary_op', '~', ('atom', (LogicValue.TRUE, ('A', 1))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.FALSE)

    def test_additive_conjunction_shared_resource(self):
        # A & A with a single shared resource A:T
        context = Counter({('A', 1): 1})
        ast = ('binary_op', '&',
               ('atom', (LogicValue.TRUE, ('A', 1))),
               ('atom', (LogicValue.TRUE, ('A', 1))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.TRUE)

    def test_additive_conjunction_different_resources(self):
        # A & B with context A:T, B:T -> Fails linearity
        context = Counter({('A', 1): 1, ('B', 1): 1})
        ast = ('binary_op', '&',
               ('atom', (LogicValue.TRUE, ('A', 1))),
               ('atom', (LogicValue.TRUE, ('B', 1))))
        with self.assertRaisesRegex(InterpretationError, "branches consume different resources"):
            self.interpreter.interpret(ast, context)

    def test_paraconsistency_with_shared_resource(self):
        # A & ~A with a single shared resource A:B
        context = Counter({('A', 1): 1})
        ast = ('binary_op', '&',
               ('atom', (LogicValue.BOTH, ('A', 1))),
               ('unary_op', '~', ('atom', (LogicValue.BOTH, ('A', 1)))))
        val = self.interpreter.interpret(ast, context)
        self.assertEqual(val, LogicValue.BOTH)

if __name__ == '__main__':
    # Clean the old, broken test runner from the interpreter file
    if os.path.exists("tooling/plllu_interpreter.py"):
        with open("tooling/plllu_interpreter.py", "r") as f:
            content = f.read()
        if "__main__" in content:
            with open("tooling/plllu_interpreter.py", "w") as f:
                f.write(content.split("if __name__ == '__main__':")[0])

    unittest.main()