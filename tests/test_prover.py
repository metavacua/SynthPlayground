import unittest
from lfi_ill.ast import *
from lfi_ill.prover import Sequent, prove

class TestProver(unittest.TestCase):

    def test_axiom(self):
        a = Atom("A")
        sequent = Sequent(antecedent=(a,), consequent=(a,))
        self.assertTrue(prove(sequent), "Axiom A ⊢ A failed")

    def test_linear_negation_axiom(self):
        a = Atom("A")
        sequent = Sequent(consequent=(a, a.neg()))
        self.assertTrue(prove(sequent), "Axiom ⊢ A, A⊥ failed")

    def test_tensor_right(self):
        a = Atom("A")
        b = Atom("B")
        # Test: A, B ⊢ A ⊗ B
        # This is a fundamental proof that requires splitting the context.
        # It should split the antecedent {A, B} into {A} and {B},
        # then prove the premises A ⊢ A and B ⊢ B.
        sequent = Sequent(antecedent=(a, b), consequent=(Tensor(a, b),))
        self.assertTrue(prove(sequent), "Tensor Right rule test (A, B ⊢ A ⊗ B) failed")

    def test_additive_provable(self):
        a = Atom("A")
        sequent = Sequent(antecedent=(a,), consequent=(With(a, a),))
        self.assertTrue(prove(sequent), "Additive A ⊢ A & A failed")

    def test_additive_not_provable(self):
        a = Atom("A")
        b = Atom("B")
        sequent = Sequent(antecedent=(Plus(a, b),), consequent=(With(a, b),))
        self.assertFalse(prove(sequent), "Additive A ⊕ B ⊢ A & B should not be provable")

    def test_modal_section_dereliction(self):
        a = Atom("A")
        sequent = Sequent(antecedent=(OfCourse(a),), consequent=(Section(a),))
        # This is !A ⊢ §A, which should be provable via the §R rule.
        # Premise for §R: A ⊢ A
        self.assertTrue(prove(sequent), "Modal !A ⊢ §A failed")

    def test_paraconsistent_non_explosion(self):
        a = Atom("A")
        b = Atom("B")
        sequent = Sequent(antecedent=(a, Negation(a)), consequent=(b,))
        self.assertFalse(prove(sequent), "Paraconsistency A, ¬A ⊢ B should not be provable")

    def test_multiplicative_connectives(self):
        a = Atom("A")
        b = Atom("B")
        sequent = Sequent(antecedent=(Tensor(a, b),), consequent=(Tensor(a, b),))
        self.assertTrue(prove(sequent), "Multiplicative A ⊗ B ⊢ A ⊗ B failed")

    def test_paraconsistent_gentle_explosion(self):
        a = Atom("A")
        b = Atom("B")
        sequent = Sequent(antecedent=(a, Negation(a), Consistency(a)), consequent=(b,))
        self.assertTrue(prove(sequent), "Paraconsistency A, ¬A, ∘A ⊢ B (Gentle Explosion) failed")


if __name__ == '__main__':
    unittest.main()