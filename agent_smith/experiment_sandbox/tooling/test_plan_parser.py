import unittest
from tooling.plan_parser import parse_plan, Command

class TestPlanParser(unittest.TestCase):

    def test_parse_single_command(self):
        """Tests parsing a single command."""
        plan_content = "set_plan\nThis is the plan."
        commands = parse_plan(plan_content)
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0], Command("set_plan", "This is the plan."))

    def test_parse_multiple_commands(self):
        """Tests parsing multiple commands separated by '---'."""
        plan_content = "set_plan\nPlan A\n---\nmessage_user\nMessage B"
        commands = parse_plan(plan_content)
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0], Command("set_plan", "Plan A"))
        self.assertEqual(commands[1], Command("message_user", "Message B"))

    def test_parse_multiline_args(self):
        """Tests parsing a command with multi-line arguments."""
        plan_content = "replace_with_git_merge_diff\npath/to/file.py\n<<<<<<<\nold\n=======\nnew\n>>>>>>>"
        commands = parse_plan(plan_content)
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].tool_name, "replace_with_git_merge_diff")
        self.assertIn("path/to/file.py", commands[0].args_text)
        self.assertIn("<<<<<<<", commands[0].args_text)

    def test_ignore_comments_and_empty_lines(self):
        """Tests that the parser ignores comments and empty lines."""
        plan_content = """
# This is a comment
set_plan
The real plan
# Another comment

---

# Comment for second command
message_user
The real message
"""
        commands = parse_plan(plan_content)
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0], Command("set_plan", "The real plan"))
        self.assertEqual(commands[1], Command("message_user", "The real message"))

if __name__ == "__main__":
    unittest.main()