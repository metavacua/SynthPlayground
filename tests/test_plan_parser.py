import unittest
import os
import sys

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from tooling.plan_parser import parse_plan

class TestPlanParser(unittest.TestCase):
    """
    Tests the plan_parser.py script.
    """

    def test_parse_plan(self):
        """
        Verify that the parse_plan function can correctly parse a simple plan.
        """
        plan_content = "set_plan: This is a test plan.\n---\nplan_step_complete: Done."
        commands = parse_plan(plan_content)
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0].tool_name, "set_plan")
        self.assertEqual(commands[0].args_text, "This is a test plan.")
        self.assertEqual(commands[1].tool_name, "plan_step_complete")
        self.assertEqual(commands[1].args_text, "Done.")

if __name__ == "__main__":
    unittest.main()
