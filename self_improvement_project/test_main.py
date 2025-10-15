import unittest
import hashlib
from unittest.mock import patch
from main import ProcessA, ProcessB, diagonalization

class TestSelfImprovement(unittest.TestCase):

    def test_diagonalization(self):
        # Test with a known input and output
        input_set = {"a", "b", "c"}
        concatenated = "abc"
        expected_output = hashlib.sha256(concatenated.encode()).hexdigest()
        self.assertEqual(diagonalization(input_set), expected_output)

    def test_process_a(self):
        # Test the innovator process
        system_state = {"initial"}
        process_a = ProcessA(system_state)
        new_element = process_a.run()
        expected_element = diagonalization(system_state)
        self.assertEqual(new_element, expected_element)

    def test_count_leading_zeros(self):
        # Test the helper function for counting zeros.
        # We can instantiate ProcessB because the method is self-contained.
        process_b = ProcessB(set())
        self.assertEqual(process_b._count_leading_zeros("000abc"), 3)
        self.assertEqual(process_b._count_leading_zeros("abc000"), 0)
        self.assertEqual(process_b._count_leading_zeros("12345"), 0)
        self.assertEqual(process_b._count_leading_zeros("0"), 1)

    def test_process_b_beneficial_integration(self):
        # Test that ProcessB correctly identifies and integrates a beneficial element.
        system_state = {"initial"}

        # We will mock the diagonalization and zero counting to control the test.
        # Let's define the sequence of hashes and their qualities (leading zeros).

        # Hash of initial state: 1 zero
        initial_state_hash = "0" + "f" * 63
        # Hash of potential next state (initial_state + new_element): 2 zeros
        next_state_hash = "00" + "f" * 62

        # The new element passed into run() is the hash of the initial state.
        new_element = initial_state_hash

        # Mock diagonalization to return the hashes we need in sequence.
        # 1. Inside ProcessB.__init__ for the initial quality.
        # 2. Inside ProcessB.is_beneficial for the next state quality.
        # 3. Inside ProcessB.run to update the best quality.
        with patch('main.diagonalization', side_effect=[initial_state_hash, next_state_hash, next_state_hash]) as mock_diag:
            process_b = ProcessB(system_state)

            # The initial quality should be 1.
            self.assertEqual(process_b.current_best_quality, 1)

            # Now, run the process with the new element.
            result = process_b.run(new_element)

            # Assert that the element was integrated because it was beneficial.
            self.assertTrue(result)
            self.assertIn(new_element, process_b.system_state)
            # The new best quality should be 2.
            self.assertEqual(process_b.current_best_quality, 2)


    def test_process_b_non_beneficial_rejection(self):
        # Test that ProcessB correctly rejects a non-beneficial element.
        system_state = {"initial"}

        # Hash of initial state: 2 zeros
        initial_state_hash = "00" + "f" * 62
        # Hash of potential next state: 1 zero
        next_state_hash = "0" + "f" * 63

        new_element = initial_state_hash

        with patch('main.diagonalization', side_effect=[initial_state_hash, next_state_hash]) as mock_diag:
            process_b = ProcessB(system_state)

            # Initial quality should be 2.
            self.assertEqual(process_b.current_best_quality, 2)
            initial_state_size = len(process_b.system_state)

            result = process_b.run(new_element)

            # Assert that the element was rejected.
            self.assertFalse(result)
            self.assertEqual(len(process_b.system_state), initial_state_size)
            # The quality should not have changed.
            self.assertEqual(process_b.current_best_quality, 2)


if __name__ == '__main__':
    unittest.main()