import unittest
import hashlib
from main import ProcessA, ProcessB, diagonalization

class TestSelfImprovement(unittest.TestCase):

    def test_diagonalization(self):
        # Test with a known input and output
        input_set = {"a", "b", "c"}
        # Sorting will produce "abc"
        concatenated = "abc"
        expected_output = hashlib.sha256(concatenated.encode()).hexdigest()
        self.assertEqual(diagonalization(input_set), expected_output)

        # Test with a different order, should be the same due to sorting
        input_set_2 = {"c", "b", "a"}
        self.assertEqual(diagonalization(input_set_2), expected_output)

        # Test with an empty set
        input_set_3 = set()
        expected_output_3 = hashlib.sha256("".encode()).hexdigest()
        self.assertEqual(diagonalization(input_set_3), expected_output_3)


    def test_process_a(self):
        # Test the innovator process
        system_state = {"initial"}
        process_a = ProcessA(system_state)
        new_element = process_a.run()
        expected_element = diagonalization(system_state)
        self.assertEqual(new_element, expected_element)


    def test_process_b(self):
        # Test the stabilizer process
        system_state = {"initial"}
        process_b = ProcessB(system_state)

        # 'c' has an even hash, so it's "beneficial"
        beneficial_element = 'c'
        # 'a' has an odd hash, so it's "non-beneficial"
        non_beneficial_element = 'a'

        # Make sure our assumptions are correct
        self.assertTrue(process_b.is_beneficial(beneficial_element))
        self.assertFalse(process_b.is_beneficial(non_beneficial_element))

        # Test integration of a beneficial element
        initial_size = len(system_state)
        result = process_b.run(beneficial_element)
        self.assertTrue(result)
        self.assertEqual(len(system_state), initial_size + 1)
        self.assertIn(beneficial_element, system_state)

        # Test rejection of a non-beneficial element
        initial_size_after_add = len(system_state)
        result = process_b.run(non_beneficial_element)
        self.assertFalse(result)
        self.assertEqual(len(system_state), initial_size_after_add)
        self.assertNotIn(non_beneficial_element, system_state)


if __name__ == '__main__':
    unittest.main()