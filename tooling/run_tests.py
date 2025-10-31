"""
This module provides functionality for...
"""

import unittest
import os
import sys

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

def run_tests():
    """
    Discovers and runs all tests in the 'tests/' directory.
    """
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result

if __name__ == '__main__':
    result = run_tests()
    if result.wasSuccessful():
        print("All tests passed successfully.")
    else:
        print("Some tests failed.")
        exit(1)
