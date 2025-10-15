import unittest
from logic_system.src.formulas import Prop, Implies, And, Or, Not, OfCourse, LinImplies, With, Plus
from logic_system.src.sequents import Sequent
from logic_system.src.lj import axiom as lj_axiom, implies_right as lj_implies_right
from logic_system.src.translations import lj_to_lk, translate_formula_lj_to_ill

class TestTranslations(unittest.TestCase):

    def test_lj_to_lk_translation(self):
        """
        Tests the direct embedding translation from LJ to LK.
        """
        # 1. Construct a simple LJ proof for ⊢ A → A
        A = Prop("A")
        axiom_proof = lj_axiom(A) # A ⊢ A
        lj_proof = lj_implies_right(axiom_proof, Implies(A, A)) # ⊢ A → A

        # 2. Translate the LJ proof to LK
        lk_proof = lj_to_lk(lj_proof)

        # 3. Assert correctness
        self.assertIsInstance(lk_proof.conclusion, Sequent)
        self.assertEqual(lk_proof.conclusion.antecedent, frozenset())
        self.assertEqual(lk_proof.conclusion.succedent, {Implies(A, A)})
        self.assertEqual(lk_proof.rule.name, "→-R")
        self.assertEqual(len(lk_proof.premises), 1)
        self.assertEqual(lk_proof.premises[0].conclusion.antecedent, {A})
        self.assertEqual(lk_proof.premises[0].conclusion.succedent, {A})
        self.assertEqual(lk_proof.premises[0].rule.name, "Axiom")

    def test_lj_to_ill_formula_translation(self):
        """
        Tests the formula translation from LJ to ILL.
        """
        A = Prop("A")
        B = Prop("B")
        bottom = Prop("⊥")

        # Test atoms
        self.assertEqual(translate_formula_lj_to_ill(A), A)

        # Test conjunction
        formula_and = And(A, B)
        translated_and = translate_formula_lj_to_ill(formula_and)
        self.assertEqual(translated_and, With(A, B))

        # Test disjunction
        formula_or = Or(A, B)
        translated_or = translate_formula_lj_to_ill(formula_or)
        self.assertEqual(translated_or, Plus(OfCourse(A), OfCourse(B)))

        # Test implication
        formula_imp = Implies(A, B)
        translated_imp = translate_formula_lj_to_ill(formula_imp)
        self.assertEqual(translated_imp, OfCourse(LinImplies(A, B)))

        # Test negation
        formula_not = Not(A)
        translated_not = translate_formula_lj_to_ill(formula_not)
        self.assertEqual(translated_not, OfCourse(LinImplies(A, bottom)))

if __name__ == '__main__':
    unittest.main()