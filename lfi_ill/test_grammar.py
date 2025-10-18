import unittest
from lfi_ill.lexer import lexer
from lfi_ill.parser import parser
from lfi_ill.interpreter import Interpreter, ParaconsistentTruth, ParaconsistentState
from lfi_ill.ast import (
    Tensor,
    Atom,
    Par,
    Negation,
    Consistency,
    Completeness,
    OfCourse,
)


class TestGrammar(unittest.TestCase):
    def test_tensor_parsing(self):
        data = 'p ⊗ q'
        result = parser.parse(data, lexer=lexer)
        expected = Tensor(Atom('p'), Atom('q'))
        self.assertEqual(repr(result), repr(expected))

    def test_par_parsing(self):
        data = 'p ⅋ q'
        result = parser.parse(data, lexer=lexer)
        expected = Par(Atom('p'), Atom('q'))
        self.assertEqual(repr(result), repr(expected))

    def test_negation_parsing(self):
        data = '¬p'
        result = parser.parse(data, lexer=lexer)
        expected = Negation(Atom('p'))
        self.assertEqual(repr(result), repr(expected))

    def test_consistency_parsing(self):
        data = '∘p'
        result = parser.parse(data, lexer=lexer)
        expected = Consistency(Atom('p'))
        self.assertEqual(repr(result), repr(expected))

    def test_completeness_parsing(self):
        data = '~p'
        result = parser.parse(data, lexer=lexer)
        expected = Completeness(Atom('p'))
        self.assertEqual(repr(result), repr(expected))

    def test_of_course_parsing(self):
        data = '!p'
        result = parser.parse(data, lexer=lexer)
        expected = OfCourse(Atom('p'))
        self.assertEqual(repr(result), repr(expected))


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter(parser)

    def _run_interp(self, node, env=None):
        # Helper to run interpreter on a given node
        if env:
            self.interpreter.environment = env
        # This is a bit of a hack, as the interpreter is stateful
        # and designed to parse from a string.
        # We are bypassing the parser and visiting the node directly.
        return self.interpreter.visit(node)

    def test_completeness_operator(self):
        # ~A is TRUE if A is not NEITHER
        p_true = Atom('p_true')
        p_false = Atom('p_false')
        p_both = Atom('p_both')
        p_neither = Atom('p_neither')

        env = {
            'p_true': ParaconsistentState(ParaconsistentTruth.TRUE),
            'p_false': ParaconsistentState(ParaconsistentTruth.FALSE),
            'p_both': ParaconsistentState(ParaconsistentTruth.BOTH),
            'p_neither': ParaconsistentState(ParaconsistentTruth.NEITHER)
        }

        self.assertEqual(self._run_interp(Completeness(p_true), env).value, ParaconsistentTruth.TRUE)
        self.assertEqual(self._run_interp(Completeness(p_false), env).value, ParaconsistentTruth.TRUE)
        self.assertEqual(self._run_interp(Completeness(p_both), env).value, ParaconsistentTruth.TRUE)
        self.assertEqual(self._run_interp(Completeness(p_neither), env).value, ParaconsistentTruth.FALSE)

    def test_consistency_operator(self):
        # oA is TRUE if A is not BOTH
        p_true = Atom('p_true')
        p_false = Atom('p_false')
        p_both = Atom('p_both')
        p_neither = Atom('p_neither')

        env = {
            'p_true': ParaconsistentState(ParaconsistentTruth.TRUE),
            'p_false': ParaconsistentState(ParaconsistentTruth.FALSE),
            'p_both': ParaconsistentState(ParaconsistentTruth.BOTH),
            'p_neither': ParaconsistentState(ParaconsistentTruth.NEITHER)
        }

        self.assertEqual(self._run_interp(Consistency(p_true), env).value, ParaconsistentTruth.TRUE)
        self.assertEqual(self._run_interp(Consistency(p_false), env).value, ParaconsistentTruth.TRUE)
        self.assertEqual(self._run_interp(Consistency(p_both), env).value, ParaconsistentTruth.FALSE)
        self.assertEqual(self._run_interp(Consistency(p_neither), env).value, ParaconsistentTruth.TRUE)

    def test_negation_operator(self):
        # not A swaps TRUE and FALSE
        p_true = Atom('p_true')
        p_false = Atom('p_false')
        p_both = Atom('p_both')
        p_neither = Atom('p_neither')

        env = {
            'p_true': ParaconsistentState(ParaconsistentTruth.TRUE),
            'p_false': ParaconsistentState(ParaconsistentTruth.FALSE),
            'p_both': ParaconsistentState(ParaconsistentTruth.BOTH),
            'p_neither': ParaconsistentState(ParaconsistentTruth.NEITHER)
        }

        self.assertEqual(self._run_interp(Negation(p_true), env).value, ParaconsistentTruth.FALSE)
        self.assertEqual(self._run_interp(Negation(p_false), env).value, ParaconsistentTruth.TRUE)
        self.assertEqual(self._run_interp(Negation(p_both), env).value, ParaconsistentTruth.BOTH)
        self.assertEqual(self._run_interp(Negation(p_neither), env).value, ParaconsistentTruth.NEITHER)


if __name__ == '__main__':
    unittest.main()
