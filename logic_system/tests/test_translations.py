import unittest
from collections import Counter
from logic_system.src.formulas import Prop, Implies, And, Or, Not, Bottom, OfCourse, LinImplies, With, Plus
from logic_system.src.sequents import Sequent
from logic_system.src import lj, ill
from logic_system.src.translations import lj_to_lk, translate_formula_lj_to_ill, lj_to_ill_proof
from logic_system.src.proof import ProofTree, Rule

class TestTranslations(unittest.TestCase):

    def test_lj_to_lk_translation(self):
        """
        Tests the direct embedding translation from LJ to LK.
        """
        A = Prop("A")
        axiom_proof = lj.axiom(A)
        lj_proof = lj.implies_right(axiom_proof, Implies(A, A))
        lk_proof = lj_to_lk(lj_proof)
        self.assertIsInstance(lk_proof.conclusion, Sequent)
        self.assertEqual(lk_proof.conclusion.antecedent, Counter())
        self.assertEqual(lk_proof.conclusion.succedent, Counter([Implies(A, A)]))

    def test_lj_to_ill_formula_translation(self):
        """
        Tests the formula translation from LJ to ILL.
        """
        A = Prop("A")
        B = Prop("B")

        # A* = A
        self.assertEqual(translate_formula_lj_to_ill(A), A)
        # (A & B)* = A* & B*
        self.assertEqual(translate_formula_lj_to_ill(And(A, B)), With(A, B))
        # (A v B)* = !A* + !B*
        self.assertEqual(translate_formula_lj_to_ill(Or(A, B)), Plus(OfCourse(A), OfCourse(B)))
        # (A -> B)* = !A* -o B*
        self.assertEqual(translate_formula_lj_to_ill(Implies(A, B)), LinImplies(OfCourse(A), B))
        # (~A)* = !A* -o 0
        self.assertEqual(translate_formula_lj_to_ill(Not(A)), LinImplies(OfCourse(A), Bottom()))
        # ⊥* = 0
        self.assertEqual(translate_formula_lj_to_ill(Bottom()), Bottom())

    def test_lj_axiom_to_ill_proof_translation(self):
        """
        Tests the translation of a simple LJ axiom proof to ILL.
        An LJ axiom A ⊢ A translates to an ILL proof of !A* ⊢ A*
        """
        A = Prop("A")
        lj_proof = lj.axiom(A)
        ill_proof = lj_to_ill_proof(lj_proof)

        A_star = translate_formula_lj_to_ill(A) # This is just A

        self.assertIsInstance(ill_proof.conclusion, ill.ILLSequent)
        # The conclusion should be !A* ⊢ A*
        self.assertEqual(ill_proof.conclusion.antecedent, Counter([OfCourse(A_star)]))
        self.assertEqual(ill_proof.conclusion.succedent_formula, A_star)
        self.assertEqual(ill_proof.rule.name, "Dereliction")

    def test_lj_implies_right_to_ill(self):
        """Tests the translation of an LJ proof with →-R."""
        A = Prop("A")
        lj_proof = lj.implies_right(lj.axiom(A), Implies(A, A))
        ill_proof = lj_to_ill_proof(lj_proof)
        self.assertEqual(ill_proof.rule.name, "!-R")
        self.assertEqual(ill_proof.premises[0].rule.name, "⊸-R")

if __name__ == '__main__':
    unittest.main()