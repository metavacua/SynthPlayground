"""
Integration tests for the master control FSM and CFDC workflow.

This test suite has been redesigned to be single-threaded and deterministic,
eliminating the file-polling, multi-threaded architecture that was causing
timeouts and instability in the test environment.
"""
import unittest
import sys
import os
import datetime
import json
import subprocess
import tempfile
import shutil
from unittest.mock import patch

from tooling.master_control import MasterControlGraph
from tooling.state import AgentState, PlanContext
from tooling.plan_parser import parse_plan

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
        shutil.copyfile(os.path.join(self.original_cwd, "postmortem.md"), "postmortem.md")
        shutil.copyfile(os.path.join(self.original_cwd, "tooling", "fdc_cli.py"), "tooling/fdc_cli.py")
        # Create a dummy fsm.json
        with open("tooling/fsm.json", "w") as f:
            json.dump({
                "initial_state": "START",
                "final_states": ["AWAITING_SUBMISSION", "ERROR"],
                "transitions": [
                    {"source": "ORIENTING", "dest": "PLANNING", "trigger": "orientation_succeeded"},
                    {"source": "ORIENTING", "dest": "ERROR", "trigger": "orientation_failed"},
                    {"source": "PLANNING", "dest": "EXECUTING", "trigger": "plan_validated"},
                    {"source": "PLANNING", "dest": "ERROR", "trigger": "plan_failed"},
                    {"source": "EXECUTING", "dest": "EXECUTING", "trigger": "step_succeeded"},
                    {"source": "EXECUTING", "dest": "AWAITING_ANALYSIS", "trigger": "all_steps_completed"},
                    {"source": "EXECUTING", "dest": "ERROR", "trigger": "execution_failed"},
                    {"source": "AWAITING_ANALYSIS", "dest": "POST_MORTEM", "trigger": "analysis_complete"},
                    {"source": "AWAITING_ANALYSIS", "dest": "ERROR", "trigger": "analysis_failed"},
                    {"source": "POST_MORTEM", "dest": "SELF_CORRECTING", "trigger": "post_mortem_complete"},
                    {"source": "POST_MORTEM", "dest": "ERROR", "trigger": "post_mortem_failed"},
                     {"source": "SELF_CORRECTING", "dest": "AWAITING_SUBMISSION", "trigger": "self_correction_succeeded"},
                    {"source": "SELF_CORRECTING", "dest": "ERROR", "trigger": "self_correction_failed"}
                ]
            }, f)


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
    @patch("tooling.master_control.execute_research_protocol", return_value="Mocked Research Data")
    def test_happy_path(self, mock_research, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="mocked output", stderr="")
        self.graph.fsm["transitions"].append({"source": "PLANNING", "dest": "RESEARCHING", "trigger": "research_requested"})
        self.graph.fsm["transitions"].append({"source": "RESEARCHING", "dest": "EXECUTING", "trigger": "research_plan_validated"})

        # 1. ORIENTING -> PLANNING
        trigger = self.graph.do_orientation(self.agent_state)
        self.assertEqual(trigger, "orientation_succeeded")

        # 2. PLANNING -> EXECUTING
        plan_content = 'tool_one "arg"'
        with open("plan.txt", "w") as f: f.write(plan_content)
        with patch("tooling.master_control.os.path.exists", side_effect=lambda p: p == "plan.txt"):
            trigger = self.graph.do_planning(self.agent_state)
        self.assertEqual(trigger, "plan_validated")

        # 3. EXECUTING -> AWAITING_ANALYSIS
        with patch("tooling.master_control.os.path.exists", side_effect=lambda p: p == "step_complete.txt"):
            with open("step_complete.txt", "w") as f: f.write("done")
            trigger = self.graph.do_execution(self.agent_state) # Execute step
            self.assertEqual(trigger, "step_succeeded")
            trigger = self.graph.do_execution(self.agent_state) # Pop stack
            self.assertEqual(trigger, "step_succeeded")
            trigger = self.graph.do_execution(self.agent_state) # Transition out
        self.assertEqual(trigger, "all_steps_completed")

if __name__ == "__main__":
    unittest.main()