import unittest
import os
import sys
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from tooling.master_control import MasterControlGraph
from tooling.state import AgentState
from utils.logger import Logger

class TestMasterControlIntegration(unittest.TestCase):
    """
    Tests the MasterControlGraph FSM with more realistic, integration-style tests.
    """

    def setUp(self):
        """Set up common objects for the tests."""
        self.agent_state = AgentState(task="test_task")
        self.mcg = MasterControlGraph()

    def tearDown(self):
        """Clean up after tests."""
        # No shared logger to clean up
        pass

    def test_do_orientation_success(self):
        """
        Tests the do_orientation function in a safely isolated environment.
        """
        test_env_dir = os.path.abspath("temp_orientation_test_env")
        if os.path.exists(test_env_dir):
            import shutil
            shutil.rmtree(test_env_dir)
        os.makedirs(test_env_dir)

        original_cwd = os.getcwd()
        os.chdir(test_env_dir)

        try:
            # 1. Set up the simulated environment inside the temp dir
            os.makedirs("knowledge_core")
            os.makedirs("postmortems")
            os.makedirs("tooling")
            # Create a dummy schema file
            with open("LOGGING_SCHEMA.md", "w") as f:
                f.write("```json\n{}\n```")

            with open("knowledge_core/symbols.json", "w") as f:
                f.write('{"symbol": "test"}')
            with open("knowledge_core/dependency_graph.json", "w") as f:
                f.write('{"dependency": "test"}')
            with open("postmortems/2023-01-01-test.md", "w") as f:
                f.write("Old postmortem")
            with open("postmortems/2023-01-02-test.md", "w") as f:
                f.write("New postmortem")

            # The auditor script is expected to create the audit report.
            auditor_path = os.path.join("tooling", "auditor.py")
            with open(auditor_path, "w") as f:
                f.write(
                    "#!/usr/bin/env python\n"
                    "import sys\n"
                    "with open('audit_report.md', 'w') as f:\n"
                    "    f.write('Audit successful')\n"
                    "sys.exit(0)\n"
                )
            os.chmod(auditor_path, 0o755)

            tools = {"list_files": lambda: ["file1.py", "file2.py"]}

            # Use a logger that is local to the test and its temp directory
            log_path = os.path.abspath("test_activity.log.jsonl")
            local_logger = Logger(schema_path="LOGGING_SCHEMA.md", log_path=log_path)

            # 2. Run the do_orientation function
            trigger = self.mcg.do_orientation(self.agent_state, local_logger, tools)

            # 3. Assert the results
            self.assertEqual(trigger, "orientation_succeeded")
            self.assertTrue(self.agent_state.orientation_complete)
            self.assertEqual(self.agent_state.symbols, {"symbol": "test"})
            self.assertEqual(self.agent_state.dependency_graph, {"dependency": "test"})

            postmortem_message_found = any(
                "New postmortem" in m.get("content", "") for m in self.agent_state.messages
            )
            self.assertTrue(postmortem_message_found, "Post-mortem content not found")

        finally:
            # 4. Clean up
            os.chdir(original_cwd)
            import shutil
            shutil.rmtree(test_env_dir)

    def test_do_planning_valid_plan(self):
        """
        Tests the do_planning function with a valid plan using the correct '---' separator.
        """
        plan_content = (
            "set_plan: Test plan\n"
            "---\n"
            "read_file: file.txt\n"
            "---\n"
            "plan_step_complete: Done"
        )
        trigger = self.mcg.do_planning(self.agent_state, plan_content, MagicMock(spec=Logger))
        self.assertEqual(trigger, "plan_op", f"Expected 'plan_op' but got '{trigger}'. Agent state error: {self.agent_state.error}")
        self.assertEqual(len(self.agent_state.plan_stack), 1)
        # set_plan is stripped, so we expect 2 commands left
        self.assertEqual(len(self.agent_state.plan_stack[0].commands), 2)
        self.assertEqual(self.agent_state.plan_stack[0].commands[0].tool_name, "read_file")
        self.assertEqual(self.agent_state.plan_stack[0].commands[1].tool_name, "plan_step_complete")

    def test_do_planning_invalid_fsm_transition(self):
        """
        Tests the do_planning function with a plan that violates FSM rules.
        """
        # 'submit' requires a transition that doesn't exist from EXECUTING.
        plan_content = (
            "set_plan: Invalid plan\n"
            "---\n"
            "submit: changes"
        )
        trigger = self.mcg.do_planning(self.agent_state, plan_content, MagicMock(spec=Logger))
        self.assertEqual(trigger, "planning_failed")
        self.assertIn("Invalid FSM transition", self.agent_state.error)
        self.assertIn("'submit_op'", self.agent_state.error)
        self.assertIn("'EXECUTING'", self.agent_state.error)


    def test_do_planning_forbidden_tool(self):
        """
        Tests that a plan with the forbidden 'reset_all' tool is rejected.
        """
        plan_content = (
            "set_plan: Forbidden plan\n"
            "---\n"
            "reset_all: now"
        )
        trigger = self.mcg.do_planning(self.agent_state, plan_content, MagicMock(spec=Logger))
        self.assertEqual(trigger, "planning_failed")
        self.assertIn("forbidden tool `reset_all`", self.agent_state.error)

    def test_do_execution_simple_plan(self):
        """
        Tests the do_execution function by executing a simple, valid plan.
        """
        # 1. First, create a valid plan and push it to the stack
        plan_content = (
            "set_plan: Simple execution plan\n"
            "---\n"
            "read_file: file1.txt\n"
            "---\n"
            "create_file_with_block: file2.txt\n"
            "content: Hello"
        )
        local_logger = MagicMock(spec=Logger)
        trigger = self.mcg.do_planning(self.agent_state, plan_content, local_logger)
        self.assertEqual(len(self.agent_state.plan_stack), 1)

        # 2. Execute the first step
        trigger = self.mcg.do_execution(self.agent_state, "Step 1 result", local_logger)
        self.assertEqual(trigger, "step_op")
        self.assertEqual(self.agent_state.plan_stack[-1].current_step, 1)

        # 3. Execute the second step
        trigger = self.mcg.do_execution(self.agent_state, "Step 2 result", local_logger)
        self.assertEqual(trigger, "step_op")
        self.assertEqual(self.agent_state.plan_stack[-1].current_step, 2)

        # 4. Execute after the last step, which should finalize the plan
        trigger = self.mcg.do_execution(self.agent_state, "Step 3 result", local_logger)
        self.assertEqual(trigger, "all_steps_completed")
        self.assertEqual(len(self.agent_state.plan_stack), 0) # Plan stack should be empty

    def test_do_finalizing_success(self):
        """
        Tests the do_finalizing function to ensure it creates a valid post-mortem report.
        """
        test_env_dir = os.path.abspath("temp_finalizing_test_env")
        if os.path.exists(test_env_dir):
            import shutil
            shutil.rmtree(test_env_dir)
        os.makedirs(test_env_dir)

        original_cwd = os.getcwd()
        os.chdir(test_env_dir)

        try:
            # 1. Set up the environment
            os.makedirs("postmortems")
            with open("LOGGING_SCHEMA.md", "w") as f:
                f.write("```json\n{}\n```")
            with open("postmortems/structured_postmortem.md", "w") as f:
                f.write(
                    "# Post-Mortem Report\n\n"
                    "**Task ID:** [TASK_ID]\n\n"
                    "## 1. Summary\n\n*A concise, one-sentence summary of the original goal.*\n\n"
                    "## 4. General Reflections\n\n*A high-level, narrative description of how the task unfolded. What was the overall approach? Were there any major surprises or deviations from the initial plan?*\n"
                )

            self.agent_state.task_description = "Test task description."
            analysis_content = "This was a test analysis."

            # Use a logger that is local to the test and its temp directory
            log_path = os.path.abspath("test_activity.log.jsonl")
            local_logger = Logger(schema_path="LOGGING_SCHEMA.md", log_path=log_path)


            # Simulate prior FSM steps by setting required state
            self.agent_state.session_start_time = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
            # This log entry needs to match the structure expected by the post-mortem generator
            local_logger.log(
                "Phase 4",
                self.agent_state.task,
                0,
                "TOOL_EXEC",
                {"tool_name": "dummy_tool", "args_text": "some_args"},
                "SUCCESS",
                "dummy result"
            )

            # 2. Run the do_finalizing function
            trigger = self.mcg.do_finalizing(self.agent_state, analysis_content, local_logger)

            # 3. Assert the results
            self.assertEqual(trigger, "finalization_succeeded", f"Finalization failed with error: {self.agent_state.error}")

            # Find the created post-mortem file
            postmortem_files = os.listdir("postmortems")
            self.assertEqual(len(postmortem_files), 2) # Template and new report
            report_file = [f for f in postmortem_files if f.startswith(str(datetime.now().date()))][0]
            self.assertTrue(report_file.endswith("-test_task.md"))

            with open(os.path.join("postmortems", report_file), "r") as f:
                content = f.read()

            self.assertIn("test_task", content)
            self.assertIn("Test task description.", content)
            self.assertIn("This was a test analysis.", content)

        finally:
            # 4. Clean up
            os.chdir(original_cwd)
            import shutil
            shutil.rmtree(test_env_dir)

if __name__ == "__main__":
    unittest.main()
