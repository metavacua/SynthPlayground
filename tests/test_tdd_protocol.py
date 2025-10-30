import unittest
import os
import sys
import subprocess
import shutil

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

class TestTddProtocol(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'temp_tdd_test_dir'
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_dir, 'test_sample.py')
        self.implementation_file_path = os.path.join(self.test_dir, 'sample.py')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_tdd_protocol_enforced(self):
        # 1. Create a failing test
        with open(self.test_file_path, 'w') as f:
            f.write("""
import unittest
import sample

class SampleTest(unittest.TestCase):
    def test_sample(self):
        self.assertTrue(sample.is_true())
""")

        # 2. Run the tests and verify that they fail
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
        self.assertNotEqual(result.returncode, 0)

        # 3. Create the implementation
        with open(self.implementation_file_path, 'w') as f:
            f.write("""
def is_true():
    return True
""")

        # 4. Run the tests and verify that they pass
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
