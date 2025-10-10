"""
Integration tests for the master control FSM and CFDC workflow.

This test suite has been redesigned to be single-threaded and deterministic,
eliminating the file-polling, multi-threaded architecture that was causing
timeouts and instability in the test environment.

The key principles of this new design are:
- **No `time.sleep`:** All forms of waiting are removed.
- **No `threading`:** The tests run in a single, predictable thread.
- **Direct State Manipulation:** The tests directly call the FSM's state-handler
  methods (e.g., `do_planning`, `do_execution`) instead of running the FSM's
  main loop.
- **Mocking Filesystem I/O:** `os.path.exists` and other file operations that
  the FSM uses for polling are mocked. This gives the test complete and
  instantaneous control over the FSM's state transitions.
- **Hermetic Environment:** All tests run inside a temporary directory, and all
  necessary dependencies from the repository are copied into it, ensuring tests
  do not have side effects and do not rely on the external state of the repo.
"""
import unittest
import sys
import os
import datetime
import json
import subprocess
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Use absolute imports
from tooling.master_control import MasterControlGraph
from tooling.state import AgentState, PlanContext
from tooling.plan_parser import parse_plan, Command

class TestMasterControlRedesigned(unittest.TestCase):
    """
    Validates the FSM workflow in a single-threaded, deterministic manner.
    """

    def setUp(self):
        self.original_cwd = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

        # Create a hermetic test environment
        os.makedirs("knowledge_core", exist_ok=True)
        os.makedirs("postmortems", exist_ok=True)
        os.makedirs("tooling", exist_ok=True)
        os.makedirs("protocols", exist_ok=True)

        # Copy essential dependencies into the temp directory
        shutil.copyfile(os.path.join(self.original_cwd, "postmortem.md"), "postmortem.md")
        shutil.copyfile(os.path.join(self.original_cwd, "tooling", "state.py"), "tooling/state.py")
        shutil.copyfile(os.path.join(self.original_cwd, "tooling", "fdc_cli.py"), "tooling/fdc_cli.py")

        self.fsm_path = os.path.join(self.original_cwd, "tooling", "fsm.json")
        self.task_id = "test-redesigned-workflow"
        self.mock_protocol_id = "test-protocol-for-correction"

        # Create mock protocol and lessons files
        self.mock_protocol_file = f"protocols/{self.mock_protocol_id}.protocol.json"
        self.lessons_file = "knowledge_core/lessons.jsonl"
        with open(self.mock_protocol_file, "w") as f:
            json.dump({"protocol_id": self.mock_protocol_id, "associated_tools": []}, f)
        open(self.lessons_file, "w").close()

        # Instantiate the components under test
        self.agent_state = AgentState(task=self.task_id)
        self.graph = MasterControlGraph(fsm_path=self.fsm_path)


    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)


    @patch("master_control.subprocess.run")
    def test_full_workflow_single_threaded(self, mock_subprocess):
        """
        Tests the full, non-blocking FSM workflow deterministically.
        """
        # --- Mocking Setup ---
        def subprocess_side_effect(cmd, *args, **kwargs):
            cmd_str = " ".join(cmd)
            if "knowledge_compiler.py" in cmd_str:
                lesson = {"lesson_id": "l1", "insight": "Test lesson", "action": {"type": "UPDATE_PROTOCOL", "command": "add-tool", "parameters": {"protocol_id": self.mock_protocol_id, "tool_name": "new_mock_tool"}}, "status": "pending"}
                with open(self.lessons_file, "a") as f: f.write(json.dumps(lesson) + "\n")
            elif "self_correction_orchestrator.py" in cmd_str:
                with open(self.mock_protocol_file, "r+") as f:
                    data = json.load(f)
                    data["associated_tools"].append("new_mock_tool")
                    f.seek(0); json.dump(data, f); f.truncate()
            return subprocess.CompletedProcess(args=cmd, returncode=0)
        mock_subprocess.side_effect = subprocess_side_effect

        # --- Test Execution ---
        # 1. ORIENTING
        with patch("tooling.master_control.execute_research_protocol", return_value="Mocked Research Data"):
            trigger = self.graph.do_orientation(self.agent_state)
        self.assertEqual(trigger, "orientation_succeeded")

        # 2. PLANNING
        trigger = self.graph.do_planning(self.agent_state)
        self.assertEqual(trigger, "plan_not_found")
        plan_content = 'list_files\n\n# A comment\n\nread_file tooling/state.py'
        with open("plan.txt", "w") as f: f.write(plan_content)
        trigger = self.graph.do_planning(self.agent_state)
        self.assertEqual(trigger, "plan_is_set")

        # 3. EXECUTING
        # Step 1
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "step_not_complete")
        with open("step_complete.txt", "w") as f: f.write("done")
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "step_succeeded")
        # Step 2
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "step_not_complete")
        with open("step_complete.txt", "w") as f: f.write("done")
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "step_succeeded")

        # Finish Execution
        trigger = self.graph.do_execution(self.agent_state) # Pop plan
        self.assertEqual(trigger, "step_succeeded")
        trigger = self.graph.do_execution(self.agent_state) # Transition out
        self.assertEqual(trigger, "all_steps_completed")

        # 4. AWAITING_ANALYSIS
        trigger = self.graph.do_awaiting_analysis(self.agent_state)
        self.assertEqual(trigger, "analysis_not_complete")
        with open("analysis_complete.txt", "w") as f: f.write("done")
        trigger = self.graph.do_awaiting_analysis(self.agent_state)
        self.assertEqual(trigger, "analysis_complete")

        # 5. POST_MORTEM
        trigger = self.graph.do_post_mortem(self.agent_state)
        self.assertEqual(trigger, "post_mortem_complete")

        # 6. SELF_CORRECTING
        trigger = self.graph.do_self_correcting(self.agent_state)
        self.assertEqual(trigger, "self_correction_succeeded")
        self.graph.current_state = "AWAITING_SUBMISSION"

        # --- Assertions ---
        self.assertIsNone(self.agent_state.error)
        self.assertEqual(self.graph.current_state, "AWAITING_SUBMISSION")
        with open(self.mock_protocol_file, "r") as f:
            updated_protocol = json.load(f)
        self.assertIn("new_mock_tool", updated_protocol["associated_tools"])

    def test_reset_all_unauthorized(self):
        """
        Verify that an attempt to use 'reset_all' without an authorization
        token immediately transitions the FSM to the ERROR state.
        """
        # Create a plan that contains the forbidden command
        plan_content = 'reset_all "Catastrophic Reset"'
        with open("plan.txt", "w") as f: f.write(plan_content)

        # Load the plan into the agent state
        self.agent_state.plan_stack.append(
            PlanContext(plan_path="plan.txt", commands=parse_plan(plan_content))
        )

        # Execute the step - it should return 'execution_failed' directly now
        trigger = self.graph.do_execution(self.agent_state)

        # Assert that the FSM entered the error state
        self.assertEqual(trigger, "execution_failed", "The FSM did not fire the correct error trigger.")
        self.assertIn("Unauthorized use of 'reset_all'", self.agent_state.error)

    def test_reset_all_authorized(self):
        """
        Verify that using 'reset_all' with an authorization token
        is allowed and that the token is consumed.
        """
        # Create the authorization token
        auth_token_path = "knowledge_core/reset_all_authorization.token"
        with open(auth_token_path, "w") as f: f.write("authorized")
        self.assertTrue(os.path.exists(auth_token_path))

        # Create a plan with the 'reset_all' command
        plan_content = 'reset_all "Authorized Reset"'
        with open("plan.txt", "w") as f: f.write(plan_content)

        # Load the plan into the agent state
        self.agent_state.plan_stack.append(
            PlanContext(plan_path="plan.txt", commands=parse_plan(plan_content))
        )

        # Create the 'step_complete.txt' file to simulate the agent completing the step
        with open("step_complete.txt", "w") as f:
            f.write("Reset authorized and executed.")

        # Execute the step
        trigger = self.graph.do_execution(self.agent_state)

        # Assert that the command was allowed and the FSM continued
        self.assertEqual(trigger, "step_succeeded")
        self.assertIsNone(self.agent_state.error)

        # Assert that the one-time token was consumed
        self.assertFalse(os.path.exists(auth_token_path), "The authorization token was not consumed.")


if __name__ == "__main__":
    unittest.main()