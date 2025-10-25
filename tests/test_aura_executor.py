import unittest
from unittest.mock import patch
import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Add the tooling directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../tooling")))

from tooling import aura_executor

class TestAuraExecutor(unittest.TestCase):

    def setUp(self):
        # Create a dummy test file
        self.test_file = "test.aura"
        with open(self.test_file, "w") as f:
            f.write('print("Hello from Aura")')

    def tearDown(self):
        # Clean up the dummy test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("sys.argv", ["tooling/aura_executor.py", "test.aura"])
    @patch("builtins.print")
    def test_successful_execution(self, mock_print):
        aura_executor.main()
        # We need to check if any of the print calls contains the expected output.
        # This is because the executor now prints a lot of other things.
        self.assertTrue(any("Hello from Aura" in call[0][0] for call in mock_print.call_args_list))

    @patch("sys.argv", ["tooling/aura_executor.py", "integration_demo.aura"])
    @patch("builtins.print")
    def test_integration_demo_end_to_end_subprocess(self, mock_print):
        # This is a placeholder test. A more robust test would check the
        # output of the subprocess.
        aura_executor.main()
        self.assertTrue(any("Integration demo complete!" in call[0][0] for call in mock_print.call_args_list))

if __name__ == "__main__":
    unittest.main()
