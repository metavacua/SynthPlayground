import unittest
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plllu.parser import parse
from plllu.interpreter import Interpreter, Truth

class TestPllluInterpreter(unittest.TestCase):

    def setUp(self):
        self.interpreter = Interpreter()

    def _run_test(self, formula, expected_truth, env=None):
        if env:
            self.interpreter.environment = env
        ast = parse(formula)
        result = self.interpreter.eval(ast)
        self.assertEqual(result, expected_truth, f"Failed on formula: {formula}")
        self.interpreter.environment = {} # Reset env

    def test_atoms(self):
        self._run_test("a", Truth.TRUE, env={'a': Truth.TRUE})
        self._run_test("a", Truth.FALSE, env={'a': Truth.FALSE})
        self._run_test("a", Truth.BOTH, env={'a': Truth.BOTH})
        self._run_test("a", Truth.NEITHER, env={'a': Truth.NEITHER})
        self._run_test("b", Truth.NEITHER) # Not in env

    def test_negation(self):
        self._run_test("¬a", Truth.FALSE, env={'a': Truth.TRUE})
        self._run_test("¬a", Truth.TRUE, env={'a': Truth.FALSE})
        self._run_test("¬a", Truth.BOTH, env={'a': Truth.BOTH})
        self._run_test("¬a", Truth.NEITHER, env={'a': Truth.NEITHER})

    def test_consistency_operator(self):
        self._run_test("∘a", Truth.TRUE, env={'a': Truth.TRUE})
        self._run_test("∘a", Truth.TRUE, env={'a': Truth.FALSE})
        self._run_test("∘a", Truth.FALSE, env={'a': Truth.BOTH})
        self._run_test("∘a", Truth.TRUE, env={'a': Truth.NEITHER})

    def test_paracomplete_operator(self):
        self._run_test("~a", Truth.TRUE, env={'a': Truth.TRUE})
        self._run_test("~a", Truth.TRUE, env={'a': Truth.FALSE})
        self._run_test("~a", Truth.TRUE, env={'a': Truth.BOTH})
        self._run_test("~a", Truth.FALSE, env={'a': Truth.NEITHER})

    def test_tensor_connective(self):
        # TRUE ⊗ TRUE -> TRUE
        self._run_test("a ⊗ b", Truth.TRUE, env={'a': Truth.TRUE, 'b': Truth.TRUE})
        # FALSE ⊗ x -> FALSE
        self._run_test("a ⊗ b", Truth.FALSE, env={'a': Truth.FALSE, 'b': Truth.TRUE})
        self._run_test("a ⊗ b", Truth.FALSE, env={'a': Truth.TRUE, 'b': Truth.FALSE})
        # BOTH ⊗ TRUE -> BOTH
        self._run_test("a ⊗ b", Truth.BOTH, env={'a': Truth.BOTH, 'b': Truth.TRUE})
        # NEITHER ⊗ x -> NEITHER
        self._run_test("a ⊗ b", Truth.NEITHER, env={'a': Truth.NEITHER, 'b': Truth.TRUE})

    def test_par_connective(self):
        # FALSE ⅋ FALSE -> FALSE
        self._run_test("a ⅋ b", Truth.FALSE, env={'a': Truth.FALSE, 'b': Truth.FALSE})
        # TRUE ⅋ x -> TRUE
        self._run_test("a ⅋ b", Truth.TRUE, env={'a': Truth.TRUE, 'b': Truth.FALSE})
        # BOTH ⅋ FALSE -> BOTH
        self._run_test("a ⅋ b", Truth.BOTH, env={'a': Truth.BOTH, 'b': Truth.FALSE})
        # NEITHER ⅋ FALSE -> NEITHER
        self._run_test("a ⅋ b", Truth.NEITHER, env={'a': Truth.NEITHER, 'b': Truth.FALSE})

    def test_complex_formulas(self):
        # ¬(a ⊗ ¬a) -> ¬(T ⊗ F) -> ¬F -> T
        self._run_test("¬(a ⊗ ¬a)", Truth.TRUE, env={'a': Truth.TRUE})
        # ∘(a ⊗ b) -> ∘(T ⊗ B) -> ∘B -> F
        self._run_test("∘(a ⊗ b)", Truth.FALSE, env={'a': Truth.TRUE, 'b': Truth.BOTH})
        # ~(a ⅋ b) -> ~(T ⅋ N) -> ~T -> T
        self._run_test("~(a ⅋ b)", Truth.TRUE, env={'a': Truth.TRUE, 'b': Truth.NEITHER})
        # Inconsistent but not explosive without ∘
        self._run_test("a ⊗ ¬a", Truth.BOTH, env={'a': Truth.BOTH})


if __name__ == '__main__':
    unittest.main()