"""
Integration tests for the master control FSM and CFDC workflow.

This test suite has been redesigned to be single-threaded and deterministic,
eliminating the file-polling, multi-threaded architecture that was causing
timeouts and instability in the test environment.
"""

import unittest
import sys
import os

sys.path.insert(0, ".")
import json
import subprocess
import tempfile
import shutil
from unittest.mock import patch

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
        os.makedirs("protocols", exist_ok=True)
        # Copy essential dependencies
        shutil.copyfile(
            os.path.join(self.original_cwd, "postmortem.md"), "postmortem.md"
        )
        shutil.copyfile(
            os.path.join(self.original_cwd, "tooling", "fdc_cli.py"),
            "tooling/fdc_cli.py",
        )
        shutil.copyfile(
            os.path.join(self.original_cwd, "tooling", "master_control.py"),
            "tooling/master_control.py",
        )
        shutil.copyfile(
            os.path.join(self.original_cwd, "tooling", "fsm.json"), "tooling/fsm.json"
        )

        # Create a dummy fsm.json
        with open("tooling/fsm.json", "w") as f:
            json.dump(
                {
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
                        {
                            "source": "PLANNING",
                            "dest": "EXECUTING",
                            "trigger": "plan_is_set",
                        },
                        {
                            "source": "PLANNING",
                            "dest": "ERROR",
                            "trigger": "planning_failed",
                        },
                        {
                            "source": "EXECUTING",
                            "dest": "EXECUTING",
                            "trigger": "step_succeeded",
                        },
                        {
                            "source": "EXECUTING",
                            "dest": "FINALIZING",
                            "trigger": "all_steps_completed",
                        },
                        {
                            "source": "EXECUTING",
                            "dest": "ERROR",
                            "trigger": "execution_failed",
                        },
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
                },
                f,
            )

        self.fsm_path = "tooling/fsm.json"
        self.task_id = "test-redesigned-workflow"
        self.agent_state = AgentState(task=self.task_id)
        self.graph = MasterControlGraph(fsm_path=self.fsm_path)

        # Ensure a clean slate for tests that use tokens
        if os.path.exists("authorization.token"):
            os.remove("authorization.token")

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch("tooling.master_control.subprocess.run")
    @patch(
        "tooling.master_control.execute_research_protocol",
        return_value="Mocked Research Data",
    )
    def test_do_orientation(self, mock_research, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="mocked output", stderr=""
        )
        trigger = self.graph.do_orientation(self.agent_state)
        self.assertEqual(trigger, "orientation_succeeded")

    @patch("tooling.master_control.subprocess.run")
    def test_do_planning(self, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="mocked output", stderr=""
        )
        with open("plan.txt", "w") as f:
            f.write("# FSM: tooling/fsm.json\n---\n1. message_user: Test message")
        with patch("time.sleep", return_value=None):
            trigger = self.graph.do_planning(self.agent_state)
        self.assertEqual(trigger, "plan_is_set")

    def test_do_execution(self):
        self.agent_state.plan_stack.append(
            PlanContext(
                plan_path="plan.txt",
                commands=[
                    Command(tool_name="message_user", args_text="test"),
                    Command(tool_name="message_user", args_text="test2"),
                ],
            )
        )
        with open("step_complete.txt", "w") as f:
            f.write("done")
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "step_succeeded")
        with open("step_complete.txt", "w") as f:
            f.write("done")
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "step_succeeded")
        trigger = self.graph.do_execution(self.agent_state)
        self.assertEqual(trigger, "all_steps_completed")

    @patch("tooling.master_control.subprocess.run")
    def test_do_finalizing(self, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="mocked output", stderr=""
        )
        with open("analysis_complete.txt", "w") as f:
            f.write("Analysis complete")
        trigger = self.graph.do_finalizing(self.agent_state)
        self.assertEqual(trigger, "finalization_succeeded")


if __name__ == "__main__":
    unittest.main()
