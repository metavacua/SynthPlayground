import unittest
import sys
import os

# Add the root directory to the Python path to allow importing witness_d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from witness_d import godel_number, diagonalization_function, decide, register_formula

class TestDecidableDiagonalizationTheory(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment. This involves clearing the GODEL_LOOKUP
        table before each test to ensure test isolation.
        """
        # Since witness_d.GODEL_LOOKUP is a global, we need to manage it
        import witness_d
        witness_d.GODEL_LOOKUP = {}

    def test_diagonalization_function(self):
        """
        Tests the core logic of the diagonalization function.
        """
        formula_A = "x + 1 = 1 + x"
        godel_A = register_formula(formula_A)

        # The result should be the Gödel number of the substituted formula.
        d_godel_A = diagonalization_function(godel_A)

        substituted_formula = formula_A.replace('x', str(godel_A))
        expected_godel = godel_number(substituted_formula)

        self.assertEqual(d_godel_A, expected_godel)

    def test_decider_true_statement(self):
        """
        Tests that the decider correctly identifies a true statement.
        """
        formula_B = "d(x) = d(x)"
        godel_B = register_formula(formula_B)
        d_godel_B = diagonalization_function(godel_B)

        true_statement = f"d({godel_B}) = {d_godel_B}"
        decision = decide(true_statement)

        self.assertTrue(decision["decided"])
        self.assertTrue(decision["value"])
        self.assertEqual(decision["LHS_eval"], d_godel_B)

    def test_decider_false_statement(self):
        """
        Tests that the decider correctly identifies a false statement.
        """
        formula_C = "x = 1"
        godel_C = register_formula(formula_C)

        # A statement that is definitionally false.
        false_statement = f"d({godel_C}) = {godel_C}" # d(n) is rarely equal to n
        decision = decide(false_statement)

        self.assertTrue(decision["decided"])
        self.assertFalse(decision["value"])

    def test_decider_invalid_formula(self):
        """
        Tests that the decider handles malformed formulas gracefully.
        """
        decision = decide("this is not a valid formula")
        self.assertFalse(decision["decided"])
        self.assertIn("reason", decision)

if __name__ == '__main__':
    unittest.main()
