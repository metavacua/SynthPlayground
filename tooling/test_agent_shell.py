import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the root directory to the path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.agent_shell import main, run_agent_loop

class TestAgentShell(unittest.TestCase):

    @patch('tooling.agent_shell.run_agent_loop')
    def test_main_with_model_a(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py', '--model', 'A']):
            main()
            mock_run_agent_loop.assert_called_once_with('Execute a self-improvement task under CSDC Model A.', model='A')

    @patch('tooling.agent_shell.run_agent_loop')
    def test_main_with_model_b(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py', '--model', 'B']):
            main()
            mock_run_agent_loop.assert_called_once_with('Execute a self-improvement task under CSDC Model B.', model='B')

    @patch('tooling.agent_shell.run_agent_loop')
    def test_main_with_no_model(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py']):
            main()
            mock_run_agent_loop.assert_called_once_with('Perform a basic self-check and greet the user.', model=None)

if __name__ == '__main__':
    unittest.main()