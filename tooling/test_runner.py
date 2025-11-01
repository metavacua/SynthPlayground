import argparse
import unittest
import os
import sys

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)


def run_tests(test_dir):
    """
    Discovers and runs all tests in the specified directory.
    """
    # Discover all test files in the specified directory
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir)

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=False)
    result = runner.run(suite)

    # Exit with a non-zero exit code if any tests failed
    if not result.wasSuccessful():
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Run all tests in the repository.")
    parser.add_argument(
        "--test-dir",
        default="tests",
        help="The directory containing the tests to run.",
    )
    args = parser.parse_args()
    run_tests(args.test_dir)


if __name__ == "__main__":
    main()
