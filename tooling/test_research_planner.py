import unittest
from tooling.research_planner import plan_deep_research


class TestNewResearchPlanner(unittest.TestCase):
    """
    Tests for the refactored, FSM-compliant research planner.
    """

    def test_plan_deep_research_generates_executable_plan(self):
        """
        Verify that the new plan_deep_research generates a valid, executable
        FSM-compliant plan.
        """
        topic = "The Role of AI in Modern Software Engineering"
        safe_topic_name = "the_role_of_ai_in_modern_software_engineering"
        expected_report_file = f"research_report_{safe_topic_name}.md"
        expected_task_id = f"research-{safe_topic_name}"

        # Generate the plan
        plan = plan_deep_research(topic)
        plan_lines = plan.splitlines()

        # 1. Verify it's a non-empty string
        self.assertIsInstance(plan, str)
        self.assertTrue(len(plan) > 0)

        # 2. Verify it contains the correct FSM directive as the second line
        self.assertIn("# FSM: tooling/research_fsm.json", plan_lines[1])

        # 3. Verify it contains the core executable commands in order
        executable_lines = [
            line
            for line in plan_lines
            if line.strip() and not line.strip().startswith("#")
        ]
        self.assertEqual(len(executable_lines), 4)
        self.assertIn(
            f"set_plan This is the research plan for the topic: '{topic}'.",
            executable_lines[0],
        )
        self.assertIn("plan_step_complete", executable_lines[1])
        self.assertIn(
            f"create_file_with_block {expected_report_file}", executable_lines[2]
        )
        self.assertIn(
            f'run_in_bash_session python3 tooling/fdc_cli.py close --task-id "{expected_task_id}"',
            executable_lines[3],
        )


if __name__ == "__main__":
    unittest.main()
