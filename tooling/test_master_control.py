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

# Add tooling directory to path to import other tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from master_control import MasterControlGraph
from state import AgentState

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
    @patch("master_control.os.path.exists")
    def test_full_workflow_single_threaded(self, mock_exists, mock_subprocess):
        """
        Tests the full FSM workflow deterministically without threads or sleeps.
        """
        # --- Mocking Setup ---
        def subprocess_side_effect(cmd, *args, **kwargs):
            script_name = os.path.basename(cmd[1])
            if script_name == "knowledge_compiler.py":
                lesson = {
                    "lesson_id": "l1", "insight": "Test lesson",
                    "action": {"type": "UPDATE_PROTOCOL", "command": "add-tool", "parameters": {"protocol_id": self.mock_protocol_id, "tool_name": "new_mock_tool"}},
                    "status": "pending"
                }
                with open(self.lessons_file, "a") as f: f.write(json.dumps(lesson) + "\n")
                return subprocess.CompletedProcess(args=cmd, returncode=0)
            if script_name == "self_correction_orchestrator.py":
                with open(self.mock_protocol_file, "r+") as f:
                    data = json.load(f)
                    data["associated_tools"].append("new_mock_tool")
                    f.seek(0); json.dump(data, f); f.truncate()
                return subprocess.CompletedProcess(args=cmd, returncode=0)
            return subprocess.CompletedProcess(args=cmd, returncode=0)
        mock_subprocess.side_effect = subprocess_side_effect

        # --- Test Execution ---
        # 1. ORIENTING
        with patch("master_control.execute_research_protocol", return_value="Mocked Research Data"):
             trigger = self.graph.do_orientation(self.agent_state)
        self.assertEqual(trigger, "orientation_succeeded")
        self.graph.current_state = "PLANNING"

        # 2. PLANNING
        plan_content = 'set_plan "Test Plan"\nplan_step_complete "Done"'
        with open("plan.txt", "w") as f: f.write(plan_content)
        mock_exists.return_value = True
        trigger = self.graph.do_planning(self.agent_state)
        self.assertEqual(trigger, "plan_is_set")
        self.graph.current_state = "EXECUTING"

        # 3. EXECUTING
        # Simulate completing the two steps in the plan
        for _ in range(2):
            with open("step_complete.txt", "w") as f: f.write("done")
            mock_exists.return_value = True
            trigger = self.graph.do_execution(self.agent_state)
            self.assertEqual(trigger, "step_succeeded")
            self.graph.current_state = "EXECUTING"
            mock_exists.return_value = False

        # After all steps are done, the FSM pops the plan from the stack
        # and returns a trigger to re-enter the execution loop.
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "step_succeeded") # This pops the finished plan
        self.assertTrue(not self.agent_state.plan_stack) # The plan stack should now be empty

        # The next call to do_execution finds the stack empty and transitions out.
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "all_steps_completed")
        self.graph.current_state = "AWAITING_ANALYSIS"

        # 4. AWAITING_ANALYSIS
        with open("analysis_complete.txt", "w") as f: f.write("done")
        mock_exists.return_value = True
        trigger = self.graph.do_awaiting_analysis(self.agent_state)
        self.assertEqual(trigger, "analysis_complete")
        self.graph.current_state = "POST_MORTEM"

        # 5. POST_MORTEM
        trigger = self.graph.do_post_mortem(self.agent_state)
        self.assertEqual(trigger, "post_mortem_complete")
        self.graph.current_state = "SELF_CORRECTING"

        # 6. SELF_CORRECTING
        # This is where the mocked subprocess for self_correction_orchestrator.py is called
        trigger = self.graph.do_self_correcting(self.agent_state)
        self.assertEqual(trigger, "self_correction_succeeded")
        self.graph.current_state = "AWAITING_SUBMISSION"

        # --- Assertions ---
        self.assertIsNone(self.agent_state.error)
        self.assertEqual(self.graph.current_state, "AWAITING_SUBMISSION")
        with open(self.mock_protocol_file, "r") as f:
            updated_protocol = json.load(f)
        # Now this assertion should pass because the mock was called
        self.assertIn("new_mock_tool", updated_protocol["associated_tools"])


if __name__ == "__main__":
    unittest.main()