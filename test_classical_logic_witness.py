import unittest
from classical_logic_witness import prove_classical_tautology

class TestClassicalLogicWitness(unittest.TestCase):

    def test_prove_classical_tautology(self):
        """
        Tests the prove_classical_tautology function.
        """
        certificate = prove_classical_tautology()
        self.assertTrue(certificate["proven"])
        self.assertEqual(certificate["logic_system"], "Classical Propositional Logic")
        self.assertEqual(certificate["proposition"], "P or not P")
        self.assertEqual(certificate["witness_found"], "N/A (Tautology)")

if __name__ == '__main__':
    unittest.main()
