import unittest
from unittest.mock import patch, MagicMock, ANY
from tooling.agent_shell import main

class TestAgentShell(unittest.TestCase):

    @patch('tooling.agent_shell.run_agent_loop')
    def test_main_with_model_a(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py', '--model', 'A']):
            main()
            mock_run_agent_loop.assert_called_once_with('Execute a self-improvement task under CSDC Model A.', ANY, model='A')

    @patch('tooling.agent_shell.run_agent_loop')
    def test_main_with_model_b(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py', '--model', 'B']):
            main()
            mock_run_agent_loop.assert_called_once_with('Execute a self-improvement task under CSDC Model B.', ANY, model='B')

    @patch('tooling.agent_shell.run_agent_loop')
    def test_main_with_no_model(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py']):
            main()
            mock_run_agent_loop.assert_called_once_with('Perform a basic self-check and greet the user.', ANY, model=None)

if __name__ == '__main__':
    unittest.main()