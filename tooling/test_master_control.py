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

    @patch("tooling.master_control.subprocess.run")
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

        # 2. PLANNING (Standard Workflow)
        plan_content = 'set_plan "Test Plan"\n\nplan_step_complete "Done"'
        with open("plan.txt", "w") as f: f.write(plan_content)

        with patch("tooling.master_control.os.path.exists") as mock_exists:
            mock_exists.side_effect = lambda path: path == "plan.txt"
            trigger = self.graph.do_planning(self.agent_state)
        self.assertEqual(trigger, "plan_validated")

        self.assertEqual(trigger, "plan_is_set")

        # 3. EXECUTING
        with patch("tooling.master_control.os.path.exists") as mock_exists:
            mock_exists.side_effect = lambda path: path in ['plan.txt', 'step_complete.txt']
            for _ in range(2):
                with open("step_complete.txt", "w") as f: f.write("done")
                trigger = self.graph.do_execution(self.agent_state)
                self.assertEqual(trigger, "step_succeeded")
                self.graph.current_state = "EXECUTING"

            trigger = self.graph.do_execution(self.agent_state)
            self.assertEqual(trigger, "step_succeeded")
            self.assertTrue(not self.agent_state.plan_stack)

            trigger = self.graph.do_execution(self.agent_state)
            self.assertEqual(trigger, "all_steps_completed")
            self.graph.current_state = "AWAITING_ANALYSIS"

        # 4. AWAITING_ANALYSIS
        with patch("tooling.master_control.os.path.exists", return_value=True):
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
        self.assertIsNone(self.agent_state.error, f"Agent entered an error state: {self.agent_state.error}")
        with open(self.mock_protocol_file, "r") as f:
            updated_protocol = json.load(f)
        self.assertIn("new_mock_tool", updated_protocol["associated_tools"])

    @patch("master_control.subprocess.run")
    def test_l4_research_workflow(self, mock_subprocess):
        """
        Tests the L4 Deep Research Cycle is correctly triggered and executed.
        """
        mock_subprocess.return_value = subprocess.CompletedProcess(args=[], returncode=0)
        self.graph.current_state = "PLANNING"
        research_topic = "testing the L4 cycle"

        # 1. PLANNING -> RESEARCHING
        with patch("master_control.os.path.exists") as mock_exists:
            mock_exists.side_effect = lambda path: path == "request_deep_research.txt"
            with open("request_deep_research.txt", "w") as f:
                f.write(research_topic)
            trigger = self.graph.do_planning(self.agent_state)

        self.assertEqual(trigger, "research_requested")
        self.assertEqual(self.agent_state.research_findings["topic"], research_topic)
        self.graph.current_state = "RESEARCHING"

        # 2. RESEARCHING -> EXECUTING
        trigger = self.graph.do_researching(self.agent_state)
        self.assertEqual(trigger, "research_plan_validated")
        self.assertEqual(len(self.agent_state.plan_stack), 1)
        self.assertEqual(self.agent_state.plan_stack[0].plan_path, "research_plan.txt")
        self.assertTrue(os.path.exists("research_plan.txt"))
        self.graph.current_state = "EXECUTING"

        # 3. EXECUTING (the research plan)
        # The generated research plan has 4 steps
        with patch("master_control.os.path.exists") as mock_exists:
            mock_exists.side_effect = lambda path: path in ['research_plan.txt', 'step_complete.txt']
            for _ in range(4):
                with open("step_complete.txt", "w") as f: f.write("done")
                trigger = self.graph.do_execution(self.agent_state)
                self.assertEqual(trigger, "step_succeeded")
                self.graph.current_state = "EXECUTING"

            # After the loop, the plan is finished. The next call to do_execution
            # will find the current context is done, pop it, and return a trigger to re-enter.
            trigger = self.graph.do_execution(self.agent_state)
            self.assertEqual(trigger, "step_succeeded") # This pops the finished plan
            self.assertTrue(not self.agent_state.plan_stack) # The plan stack should now be empty

            # The final call to do_execution finds the stack empty and transitions out.
            trigger = self.graph.do_execution(self.agent_state)
            self.assertEqual(trigger, "all_steps_completed")

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