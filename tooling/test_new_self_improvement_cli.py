import unittest
from unittest.mock import patch
from tooling.self_improvement_cli import main

class TestNewSelfImprovementCLI(unittest.TestCase):

    @patch('tooling.self_improvement_cli.run_self_improvement_task')
    def test_run_improvement_for_model_a(self, mock_run_task):
        with patch('sys.argv', ['tooling/self_improvement_cli.py', '--run-improvement-for-model', 'A']):
            main()
            mock_run_task.assert_called_once_with('A')

    @patch('tooling.self_improvement_cli.run_self_improvement_task')
    def test_run_improvement_for_model_b(self, mock_run_task):
        with patch('sys.argv', ['tooling/self_improvement_cli.py', '--run-improvement-for-model', 'B']):
            main()
            mock_run_task.assert_called_once_with('B')

if __name__ == '__main__':
    unittest.main()