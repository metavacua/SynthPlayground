import unittest
import os


def run_tests():
    """
    Discovers and runs all protocol tests.
    """
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__), pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    run_tests()
