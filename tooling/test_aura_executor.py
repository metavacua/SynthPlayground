import unittest
import os
import shutil
from unittest.mock import patch, MagicMock, call
from tooling.aura_executor import main as aura_main

class TestAuraExecutor(unittest.TestCase):

    @patch('sys.argv', new_callable=lambda: ['tooling/aura_executor.py', 'tests/test.aura'])
    @patch('builtins.print')
    def test_successful_execution(self, mock_print, mock_argv):
        """Tests that a valid Aura script executes successfully."""
        aura_main()
        mock_print.assert_any_call("hello from aura")

if __name__ == "__main__":
    unittest.main()