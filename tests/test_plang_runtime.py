import os
import sys
import unittest

# This path manipulation MUST come before the local import to satisfy E402.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from toolchain.plang_runtime import ParaconsistentVariable


class TestPLangRuntime(unittest.TestCase):
    def test_variable_creation_success(self):
        """Test successful creation of a ParaconsistentVariable."""
        states = {"Safety": "safe_value", "Completeness": "complete_value"}
        pv = ParaconsistentVariable(states)
        self.assertIsInstance(pv, ParaconsistentVariable)
        self.assertEqual(
            repr(pv), "ParaconsistentVariable(stances=['Safety', 'Completeness'])"
        )

    def test_variable_creation_empty_dict_fails(self):
        """Test that creation fails with an empty dictionary."""
        with self.assertRaises(ValueError):
            ParaconsistentVariable({})

    def test_variable_creation_non_dict_fails(self):
        """Test that creation fails with a non-dictionary input."""
        with self.assertRaises(ValueError):
            ParaconsistentVariable([])

    def test_resolve_success(self):
        """Test successful resolution of a stance."""
        states = {"Safety": "safe_value", "Completeness": "complete_value"}
        pv = ParaconsistentVariable(states)
        self.assertEqual(pv.resolve("Safety"), "safe_value")
        self.assertEqual(pv.resolve("Completeness"), "complete_value")

    def test_resolve_nonexistent_stance_fails(self):
        """Test that resolving a non-existent stance raises a KeyError."""
        states = {"Safety": "safe_value"}
        pv = ParaconsistentVariable(states)
        with self.assertRaises(KeyError) as cm:
            pv.resolve("Performance")

        self.assertIn("Stance 'Performance' not found", str(cm.exception))
        self.assertIn("Available stances are: ['Safety']", str(cm.exception))


if __name__ == "__main__":
    unittest.main()