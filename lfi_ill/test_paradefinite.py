import unittest
from lfi_ill.lexer import lexer
from lfi_ill.parser import parser
from lfi_ill.interpreter import Interpreter, ParaconsistentTruth, ParaconsistentState
from lfi_ill.ast import Atom, CoNegation, Undeterminedness


class TestParadefiniteGrammar(unittest.TestCase):
    def test_co_negation_parsing(self):
        data = "-p"
        result = parser.parse(data, lexer=lexer)
        expected = CoNegation(Atom("p"))
        self.assertEqual(repr(result), repr(expected))

    def test_undeterminedness_parsing(self):
        data = "*p"
        result = parser.parse(data, lexer=lexer)
        expected = Undeterminedness(Atom("p"))
        self.assertEqual(repr(result), repr(expected))


class TestParadefiniteInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter(parser)

    def _run_interp(self, node, env=None):
        if env:
            self.interpreter.environment = env
        return self.interpreter.visit(node)

    def test_co_negation_operator(self):
        # -A should behave like ~A
        p_true = Atom("p_true")
        p_false = Atom("p_false")
        p_both = Atom("p_both")
        p_neither = Atom("p_neither")

        env = {
            "p_true": ParaconsistentState(ParaconsistentTruth.TRUE),
            "p_false": ParaconsistentState(ParaconsistentTruth.FALSE),
            "p_both": ParaconsistentState(ParaconsistentTruth.BOTH),
            "p_neither": ParaconsistentState(ParaconsistentTruth.NEITHER),
        }

        self.assertEqual(
            self._run_interp(CoNegation(p_true), env).value, ParaconsistentTruth.FALSE
        )
        self.assertEqual(
            self._run_interp(CoNegation(p_false), env).value, ParaconsistentTruth.TRUE
        )
        self.assertEqual(
            self._run_interp(CoNegation(p_both), env).value, ParaconsistentTruth.BOTH
        )
        self.assertEqual(
            self._run_interp(CoNegation(p_neither), env).value,
            ParaconsistentTruth.NEITHER,
        )

    def test_undeterminedness_operator(self):
        # *A is TRUE if A is not BOTH
        p_true = Atom("p_true")
        p_false = Atom("p_false")
        p_both = Atom("p_both")
        p_neither = Atom("p_neither")

        env = {
            "p_true": ParaconsistentState(ParaconsistentTruth.TRUE),
            "p_false": ParaconsistentState(ParaconsistentTruth.FALSE),
            "p_both": ParaconsistentState(ParaconsistentTruth.BOTH),
            "p_neither": ParaconsistentState(ParaconsistentTruth.NEITHER),
        }

        self.assertEqual(
            self._run_interp(Undeterminedness(p_true), env).value,
            ParaconsistentTruth.TRUE,
        )
        self.assertEqual(
            self._run_interp(Undeterminedness(p_false), env).value,
            ParaconsistentTruth.TRUE,
        )
        self.assertEqual(
            self._run_interp(Undeterminedness(p_both), env).value,
            ParaconsistentTruth.FALSE,
        )
        self.assertEqual(
            self._run_interp(Undeterminedness(p_neither), env).value,
            ParaconsistentTruth.TRUE,
        )


if __name__ == "__main__":
    unittest.main()
