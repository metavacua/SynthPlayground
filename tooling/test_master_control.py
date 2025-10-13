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
                {"source": "ORIENTING", "dest": "PLANNING", "trigger": "orientation_succeeded"},
                {"source": "ORIENTING", "dest": "ERROR", "trigger": "orientation_failed"},
                {"source": "PLANNING", "dest": "EXECUTING", "trigger": "plan_is_set"},
                {"source": "PLANNING", "dest": "ERROR", "trigger": "planning_failed"},
                {"source": "EXECUTING", "dest": "EXECUTING", "trigger": "step_succeeded"},
                {"source": "EXECUTING", "dest": "FINALIZING", "trigger": "all_steps_completed"},
                {"source": "EXECUTING", "dest": "ERROR", "trigger": "execution_failed"},
                {"source": "FINALIZING", "dest": "AWAITING_SUBMISSION", "trigger": "finalization_succeeded"},
                {"source": "FINALIZING", "dest": "ERROR", "trigger": "finalization_failed"}
            ]
        }
        with open("tooling/fsm.json", "w") as f:
            json.dump(fsm_content, f)

        # Create dummy dependencies that are called by the master_control
        with open("tooling/fdc_cli.py", "w") as f: f.write(" ")
        with open("tooling/environmental_probe.py", "w") as f: f.write(" ")
        with open("tooling/knowledge_compiler.py", "w") as f: f.write(" ")
        with open("tooling/self_correction_orchestrator.py", "w") as f: f.write(" ")


        self.fsm_path = "tooling/fsm.json"
        self.task_id = "test-redesigned-workflow"
        self.agent_state = AgentState(task=self.task_id)
        self.graph = MasterControlGraph(fsm_path=self.fsm_path)


    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch("tooling.master_control.subprocess.run")
    @patch("tooling.master_control.execute_research_protocol", return_value="Mocked Research Data")
    def test_do_orientation(self, mock_research, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="mocked output", stderr="")
        trigger = self.graph.do_orientation(self.agent_state)
        # In the new system, do_orientation directly returns the next state, not a trigger.
        self.assertEqual(trigger, self.graph.get_trigger("ORIENTING", "PLANNING"))

    @patch("tooling.master_control.subprocess.run")
    def test_do_planning(self, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        # The plan content is now passed directly as an argument, with a double newline
        plan_content = "# FSM: tooling/fsm.json\n\nmessage_user\n\nTest message"
        trigger = self.graph.do_planning(self.agent_state, plan_content)
        self.assertEqual(trigger, "plan_is_set")
        self.assertEqual(len(self.agent_state.plan_stack), 1)
        self.assertEqual(self.agent_state.plan_stack[0].commands[0].tool_name, "message_user")

    def test_do_execution(self):
        # Set up a plan on the stack
        self.agent_state.plan_stack.append(
            PlanContext(plan_path="test_plan", commands=[
                Command(tool_name="message_user", args_text="test1"),
                Command(tool_name="message_user", args_text="test2")
            ])
        )
        # Simulate the agent shell loop
        # Step 1
        step1 = self.graph.get_current_step(self.agent_state)
        self.assertIsNotNone(step1)
        self.assertEqual(step1.tool_name, "message_user")
        trigger1 = self.graph.do_execution(self.agent_state, "Step 1 result")
        self.assertEqual(trigger1, self.graph.get_trigger("EXECUTING", "EXECUTING"))

        # Step 2
        step2 = self.graph.get_current_step(self.agent_state)
        self.assertIsNotNone(step2)
        self.assertEqual(step2.tool_name, "message_user")
        trigger2 = self.graph.do_execution(self.agent_state, "Step 2 result")
        self.assertEqual(trigger2, self.graph.get_trigger("EXECUTING", "EXECUTING"))

        # End of plan
        step3 = self.graph.get_current_step(self.agent_state)
        self.assertIsNone(step3) # No more steps
        trigger3 = self.graph.do_execution(self.agent_state, None) # Signal end of plan
        self.assertEqual(trigger3, self.graph.get_trigger("EXECUTING", "FINALIZING"))


    @patch("tooling.master_control.subprocess.run")
    def test_do_finalizing(self, mock_subprocess):
        mock_subprocess.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        # The analysis content is now passed as an argument
        analysis_content = "The task was completed successfully."
        trigger = self.graph.do_finalizing(self.agent_state, analysis_content)
        self.assertEqual(trigger, self.graph.get_trigger("FINALIZING", "AWAITING_SUBMISSION"))
        self.assertIn("Post-mortem analysis finalized", self.agent_state.final_report)


if __name__ == "__main__":
    unittest.main()