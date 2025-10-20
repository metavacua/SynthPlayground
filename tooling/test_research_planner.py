import unittest
import os
import uuid
from tooling.research_planner import plan_deep_research


class TestNewResearchPlanner(unittest.TestCase):
    """
    Tests for the refactored, FSM-compliant research planner that uses templates.
    """

    def setUp(self):
        """Create dummy template files for testing."""
        self.research_plan_template_path = "research/research_plan.md"
        self.research_report_template_path = "research/research_report_template.md"

        os.makedirs("research", exist_ok=True)

        with open(self.research_plan_template_path, "w") as f:
            f.write(
                "# Research Plan: [Topic]\n**ID:** [RESEARCH_ID]\n**Objective:** [Objective]"
            )

        with open(self.research_report_template_path, "w") as f:
            f.write("# Research Report: [Topic]\n**ID:** [RESEARCH_ID]")

    def tearDown(self):
        """Remove dummy template files."""
        os.remove(self.research_plan_template_path)
        os.remove(self.research_report_template_path)
        # Clean up any generated files if they exist
        if hasattr(self, "plan_file") and os.path.exists(self.plan_file):
            os.remove(self.plan_file)
        if hasattr(self, "report_file") and os.path.exists(self.report_file):
            os.remove(self.report_file)

    def test_plan_deep_research_uses_templates_correctly(self):
        """
        Verify that plan_deep_research generates a plan that correctly
        populates and creates files from the templates.
        """
        topic = "The Impact of Quantum Computing on Cryptography"
        research_id = str(uuid.uuid4())
        self.plan_file = f"research/research_plan_{research_id}.md"
        self.report_file = f"research/research_report_{research_id}.md"

        # Generate the plan
        plan = plan_deep_research(topic, research_id)
        plan_lines = plan.splitlines()

        # 1. Verify it's a non-empty string
        self.assertIsInstance(plan, str)
        self.assertTrue(len(plan) > 0)

        # 2. Verify it contains the correct FSM directive
        self.assertIn("# FSM: tooling/research_fsm.json", plan_lines[0])

        # 3. Verify the executable commands
        executable_lines = [
            line
            for line in plan_lines
            if line.strip() and not line.strip().startswith("#")
        ]

        # Check for the key commands in the new plan structure
        self.assertIn("set_plan", executable_lines[0])
        self.assertIn(f"create_file_with_block {self.plan_file}", executable_lines[1])
        self.assertIn(f"create_file_with_block {self.report_file}", executable_lines[4])
        self.assertIn("message_user", executable_lines[6])
        self.assertIn("plan_step_complete", executable_lines[7])
        self.assertIn("submit", executable_lines[8])

        # 4. Verify that the template content is correctly embedded
        self.assertIn(f"# Research Plan: {topic}", plan)
        self.assertIn(f"**ID:** {research_id}", plan)
        self.assertIn(f"# Research Report: {topic}", plan)


if __name__ == "__main__":
    unittest.main()
