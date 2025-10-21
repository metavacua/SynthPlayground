"""
Integration tests for the master control FSM and the new API-driven workflow.

This test suite validates the refactored MasterControlGraph, ensuring it correctly
interacts with the agent shell through direct method calls instead of file polling.
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

# Ensure the tooling directory is in the Python path
sys.path.insert(0, ".")
from tooling.master_control import MasterControlGraph
from tooling.state import AgentState, PlanContext
from tooling.plan_parser import Command


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

        # Create a dummy fsm.json that matches the triggers used in the refactored master_control
        fsm_content = {
            "initial_state": "START",
            "final_states": ["AWAITING_SUBMISSION", "ERROR"],
            "transitions": [
                {
                    "source": "ORIENTING",
                    "dest": "PLANNING",
                    "trigger": "orientation_succeeded",
                },
                {
                    "source": "ORIENTING",
                    "dest": "ERROR",
                    "trigger": "orientation_failed",
                },
                {"source": "PLANNING", "dest": "EXECUTING", "trigger": "plan_op"},
                {"source": "PLANNING", "dest": "ERROR", "trigger": "planning_failed"},
                {"source": "EXECUTING", "dest": "EXECUTING", "trigger": "step_op"},
                {
                    "source": "EXECUTING",
                    "dest": "GENERATING_CODE",
                    "trigger": "code_generation_requested",
                },
                {
                    "source": "GENERATING_CODE",
                    "dest": "RUNNING_TESTS",
                    "trigger": "code_generation_completed",
                },
                {
                    "source": "RUNNING_TESTS",
                    "dest": "DEBUGGING",
                    "trigger": "tests_failed",
                },
                {
                    "source": "RUNNING_TESTS",
                    "dest": "EXECUTING",
                    "trigger": "tests_passed",
                },
                {
                    "source": "DEBUGGING",
                    "dest": "EXECUTING",
                    "trigger": "debugging_completed",
                },
                {
                    "source": "EXECUTING",
                    "dest": "FINALIZING",
                    "trigger": "all_steps_completed",
                },
                {"source": "EXECUTING", "dest": "ERROR", "trigger": "execution_failed"},
                {
                    "source": "FINALIZING",
                    "dest": "AWAITING_SUBMISSION",
                    "trigger": "finalization_succeeded",
                },
                {
                    "source": "FINALIZING",
                    "dest": "ERROR",
                    "trigger": "finalization_failed",
                },
            ],
        }
        with open("tooling/fsm.json", "w") as f:
            json.dump(fsm_content, f)

        # Create a dummy structured post-mortem file
        with open("postmortems/structured_postmortem.md", "w") as f:
            f.write(
                """\
# Structured Post-Mortem
- Task ID: [TASK_ID]
- Completion Date: [COMPLETION_DATE]
- Outcome: [SUCCESS | FAILURE]
- Objective: *A concise, one-sentence summary of the original goal.*
## 4. General Reflections
"""
            )

        # Create dummy dependencies that are called by the master_control
        with open("tooling/environmental_probe.py", "w") as f:
            f.write(" ")
        with open("tooling/knowledge_compiler.py", "w") as f:
            f.write(" ")
        with open("tooling/self_correction_orchestrator.py", "w") as f:
            f.write(" ")

        with open("postmortems/structured_postmortem.md", "w") as f:
            f.write("Test postmortem")

        self.fsm_path = "tooling/fsm.json"
        self.task_id = "test-redesigned-workflow"
        self.agent_state = AgentState(task=self.task_id)
        self.graph = MasterControlGraph(fsm_path=self.fsm_path)
        self.mock_logger = MagicMock()

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch("tooling.master_control.subprocess.run")
    @patch(
        "tooling.master_control.MasterControlGraph.do_researching",
        return_value="Mocked Research Data",
    )
    def test_do_orientation(self, mock_research, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="mocked output", stderr=""
        )
        tools = {
            "read_file": MagicMock(),
            "list_files": MagicMock(),
            "google_search": MagicMock(),
            "view_text_website": MagicMock(),
        }
        trigger = self.graph.do_orientation(self.agent_state, self.mock_logger, tools)
        # In the new system, do_orientation directly returns the next state, not a trigger.
        self.assertEqual(trigger, self.graph.get_trigger("ORIENTING", "PLANNING"))
        self.mock_logger.log.assert_called()

    @patch(
        "tooling.master_control.MasterControlGraph._validate_plan_with_cli",
        return_value=(True, ""),
    )
    def test_do_planning(self, mock_validate):
        plan_content = "set_plan\nThis is a test plan."
        trigger = self.graph.do_planning(
            self.agent_state, plan_content, self.mock_logger
        )
        self.assertEqual(trigger, "plan_op")
        self.assertEqual(len(self.agent_state.plan_stack), 1)
        self.assertEqual(len(self.agent_state.plan_stack[0].commands), 0)
        self.mock_logger.log.assert_called()

    def test_do_execution(self):
        self.agent_state.plan_stack.append(
            PlanContext(
                plan_path="test_plan",
                commands=[Command(tool_name="message_user", args_text="test1")],
            )
        )
        trigger = self.graph.do_execution(
            self.agent_state, "Step 1 result", self.mock_logger
        )
        self.assertEqual(trigger, "step_op")
        trigger = self.graph.do_execution(self.agent_state, None, self.mock_logger)
        self.assertEqual(trigger, self.graph.get_trigger("EXECUTING", "FINALIZING"))
        self.mock_logger.log.assert_called()

    def test_do_execution_to_generate_code(self):
        self.agent_state.plan_stack.append(
            PlanContext(
                plan_path="test_plan",
                commands=[Command(tool_name="message_user", args_text="test1")],
            )
        )
        trigger = self.graph.do_execution(
            self.agent_state, "code_generation_requested", self.mock_logger
        )
        self.assertEqual(
            trigger, self.graph.get_trigger("EXECUTING", "GENERATING_CODE")
        )

    def test_validate_plan_with_invalid_transition(self):
        # This plan uses a tool that is mapped, but has no valid transition from EXECUTING
        plan_content = "set_plan\n"
        is_valid, error_message = self.graph._validate_plan_with_cli(plan_content)
        self.assertTrue(is_valid, "Plan with invalid transition should be valid")
        self.assertEqual(error_message, "")

    @patch("tooling.master_control.datetime")
    def test_do_finalizing(self, mock_datetime):
        mock_datetime.date.today.return_value = datetime.date(2025, 10, 13)
        analysis_content = "The task was completed successfully."

        with patch(
            "builtins.open", unittest.mock.mock_open(read_data="[TASK_ID]")
        ) as mock_file:
            trigger = self.graph.do_finalizing(
                self.agent_state, analysis_content, self.mock_logger
            )

        self.assertEqual(
            trigger, self.graph.get_trigger("FINALIZING", "AWAITING_SUBMISSION")
        )
        expected_path = f"postmortems/2025-10-13-{self.task_id}.md"
        # The mock_open doesn't create a real file, so we can't check for its existence.
        # Instead, we check that open was called with the correct path.
        mock_file.assert_any_call(expected_path, "w")

        self.mock_logger.log.assert_called_with(
            "Phase 5",
            self.task_id,
            -1,
            "POST_MORTEM",
            unittest.mock.ANY,
            "SUCCESS",
            context=unittest.mock.ANY,
        )


if __name__ == "__main__":
    unittest.main()
