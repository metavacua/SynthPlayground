import unittest
import os
import shutil
from unittest.mock import patch
from tooling.code_suggester import generate_suggestion_plan, main as code_suggester_main

class TestCodeSuggester(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_code_suggester_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.filepath = os.path.join(self.test_dir, "test_file.txt")
        with open(self.filepath, "w") as f:
            f.write("<<<<<<< SEARCH\nold content\n=======\nnew content\n>>>>>>> REPLACE")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_generate_suggestion_plan(self):
        """Tests the generation of a suggestion plan file."""
        diff_content = "<<<<<<< SEARCH\nold content\n=======\nnew content\n>>>>>>> REPLACE"
        plan_path = generate_suggestion_plan(self.filepath, diff_content)

        self.assertTrue(os.path.exists(plan_path))

        with open(plan_path, "r") as f:
            content = f.read()

        expected_content = f"""\
replace_with_git_merge_diff
{self.filepath}
{diff_content}
"""
        self.assertEqual(content, expected_content)

        os.remove(plan_path)

    @patch('sys.argv', ['tooling/code_suggester.py', '--filepath', 'test_file.txt', '--diff', 'test diff'])
    @patch('tooling.code_suggester.generate_suggestion_plan', return_value="test_plan.txt")
    @patch('builtins.print')
    def test_main_flow(self, mock_print, mock_generate_plan):
        """Tests the main function of the code suggester."""
        code_suggester_main()
        mock_generate_plan.assert_called_once_with('test_file.txt', 'test diff')
        mock_print.assert_called_once_with("test_plan.txt")

if __name__ == "__main__":
    unittest.main()