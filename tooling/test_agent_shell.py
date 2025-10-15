import unittest
from unittest.mock import patch, MagicMock

# Mock the functions that are imported from __main__
mock_main_imports = {
    'read_file': MagicMock(),
    'list_files': MagicMock(),
    'google_search': MagicMock(),
    'view_text_website': MagicMock(),
}

with patch.dict('sys.modules', {'__main__': MagicMock(**mock_main_imports)}):
    from tooling.agent_shell import main, run_agent_loop

class TestAgentShell(unittest.TestCase):

    @patch('tooling.agent_shell.run_agent_loop')
    def test_run_agent_loop_with_model_a(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py', '--model', 'A']):
            main()
            mock_run_agent_loop.assert_called_once_with('Execute a self-improvement task under CSDC Model A.', model='A')

    @patch('tooling.agent_shell.run_agent_loop')
    def test_run_agent_loop_with_model_b(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py', '--model', 'B']):
            main()
            mock_run_agent_loop.assert_called_once_with('Execute a self-improvement task under CSDC Model B.', model='B')

    @patch('tooling.agent_shell.run_agent_loop')
    def test_run_agent_loop_with_no_model(self, mock_run_agent_loop):
        with patch('sys.argv', ['tooling/agent_shell.py']):
            main()
            mock_run_agent_loop.assert_called_once_with('Perform a basic self-check and greet the user.', model=None)

if __name__ == '__main__':
    unittest.main()