import unittest
import os
import sys
import subprocess
import shutil

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

class TestTestRunner(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'temp_test_dir'
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_dir, 'test_sample.py')
        with open(self.test_file_path, 'w') as f:
            f.write("""
import unittest

class SampleTest(unittest.TestCase):
    def test_sample(self):
        print("This is a print statement from a test.")
        self.assertTrue(False)
""")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_test_runner_captures_output_and_fails(self):
        command = [
            'python3',
            'tooling/test_runner.py',
            '--test-dir',
            self.test_dir
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        self.assertIn("This is a print statement from a test.", result.stdout)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
