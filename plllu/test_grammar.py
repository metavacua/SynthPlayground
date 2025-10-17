import unittest
from lfi_ill.parser import parse
from lfi_ill.interpreter import Interpreter, ParaconsistentTruth
from lfi_ill.ast import *

class TestGrammar(unittest.TestCase):
    def test_tensor_parsing(self):
        result = parse("A ⊗ B")
        self.assertIsInstance(result, Tensor)

    def test_par_parsing(self):
        result = parse("A ⅋ B")
        self.assertIsInstance(result, Par)

    def test_plus_parsing(self):
        result = parse("A ⊕ B")
        self.assertIsInstance(result, Plus)

    def test_with_parsing(self):
        result = parse("A & B")
        self.assertIsInstance(result, With)

    def test_negation_parsing(self):
        result = parse("¬A")
        self.assertIsInstance(result, Negation)

    def test_consistency_parsing(self):
        result = parse("∘A")
        self.assertIsInstance(result, Consistency)

    def test_paracomplete_parsing(self):
        result = parse("~A")
        self.assertIsInstance(result, Paracomplete)

    def test_of_course_parsing(self):
        result = parse("!A")
        self.assertIsInstance(result, OfCourse)

    def test_whynot_parsing(self):
        result = parse("?A")
        self.assertIsInstance(result, WhyNot)

    def test_section_parsing(self):
        result = parse("§A")
        self.assertIsInstance(result, Section)

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_negation_operator(self):
        # ¬(TRUE) = FALSE
        ast = Negation(Atom("A"))
        env = {"A": ParaconsistentTruth.TRUE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.FALSE)

        # ¬(FALSE) = TRUE
        env = {"A": ParaconsistentTruth.FALSE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

        # ¬(BOTH) = BOTH
        env = {"A": ParaconsistentTruth.BOTH}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.BOTH)

        # ¬(NEITHER) = NEITHER
        env = {"A": ParaconsistentTruth.NEITHER}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.NEITHER)

    def test_consistency_operator(self):
        # ∘(TRUE) = TRUE
        ast = Consistency(Atom("A"))
        env = {"A": ParaconsistentTruth.TRUE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

        # ∘(FALSE) = TRUE
        env = {"A": ParaconsistentTruth.FALSE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

        # ∘(BOTH) = FALSE
        env = {"A": ParaconsistentTruth.BOTH}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.FALSE)

        # ∘(NEITHER) = NEITHER
        env = {"A": ParaconsistentTruth.NEITHER}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.NEITHER)

    def test_paracomplete_operator(self):
        # ~(TRUE) = TRUE
        ast = Paracomplete(Atom("A"))
        env = {"A": ParaconsistentTruth.TRUE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

        # ~(FALSE) = TRUE
        env = {"A": ParaconsistentTruth.FALSE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

        # ~(BOTH) = BOTH
        env = {"A": ParaconsistentTruth.BOTH}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.BOTH)

        # ~(NEITHER) = FALSE
        env = {"A": ParaconsistentTruth.NEITHER}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.FALSE)

    def test_of_course_operator(self):
        # !A should evaluate A in an empty environment
        ast = OfCourse(Atom("A"))
        env = {"A": ParaconsistentTruth.FALSE} # This should be ignored
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE) # Because A is TRUE in an empty env

    def test_plus_operator(self):
        # A + B should evaluate to A
        ast = Plus(Atom("A"), Atom("B"))
        env = {"A": ParaconsistentTruth.FALSE, "B": ParaconsistentTruth.TRUE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.FALSE)

    def test_with_operator(self):
        # A & B should evaluate to the same if both are same
        ast = With(Atom("A"), Atom("B"))
        env = {"A": ParaconsistentTruth.TRUE, "B": ParaconsistentTruth.TRUE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

        env = {"A": ParaconsistentTruth.TRUE, "B": ParaconsistentTruth.FALSE}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.NEITHER)

    def test_nested_operators(self):
        # ¬(∘(BOTH)) = ¬(FALSE) = TRUE
        ast = Negation(Consistency(Atom("A")))
        env = {"A": ParaconsistentTruth.BOTH}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

        # ~(∘(BOTH)) = ~(FALSE) = TRUE
        ast = Paracomplete(Consistency(Atom("A")))
        env = {"A": ParaconsistentTruth.BOTH}
        result = self.interpreter.eval(ast, env)
        self.assertEqual(result, ParaconsistentTruth.TRUE)

if __name__ == '__main__':
    unittest.main()