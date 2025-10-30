import unittest
from presburger_arithmetic_witness import prove_presburger_proposition

class TestPresburgerArithmeticWitness(unittest.TestCase):

    def test_prove_presburger_proposition(self):
        """
        Tests the prove_presburger_proposition function.
        """
        certificate = prove_presburger_proposition()
        self.assertTrue(certificate["proven"])
        self.assertTrue(certificate["witness_found"])
        self.assertEqual(certificate["value"], 4)

if __name__ == '__main__':
    unittest.main()
