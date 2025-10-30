import unittest
from skolem_arithmetic_witness import prove_skolem_proposition

class TestSkolemArithmeticWitness(unittest.TestCase):

    def test_prove_skolem_proposition(self):
        """
        Tests the prove_skolem_proposition function.
        """
        certificate = prove_skolem_proposition()
        self.assertTrue(certificate["proven"])
        self.assertTrue(certificate["witness_found"])
        self.assertEqual(certificate["value"], "S(S(0))")

if __name__ == '__main__':
    unittest.main()
