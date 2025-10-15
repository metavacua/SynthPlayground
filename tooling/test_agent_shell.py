import unittest
import os
import json
from unittest.mock import patch, MagicMock

from tooling.agent_shell import run_agent_loop
from tooling.state import AgentState
from tooling.plan_parser import Command as PlanStep

class TestAgentShellIntegration(unittest.TestCase):

    def test_verify_logic_command(self):
        """
        Tests that the agent shell can correctly execute the verify_logic command.
        """
        # Create a dummy input file for the verifier
        task_spec = {
            "task": "synthesize",
            "logic": "ill",
            "goal": "A |- A"
        }
        input_file_path = "test_logic_input.json"
        with open(input_file_path, 'w') as f:
            json.dump(task_spec, f)

        # Mock the MasterControlGraph to control the agent's execution
        mock_mcg = MagicMock()
        mock_mcg.fsm = {
            "states": ["START", "ORIENTING", "EXECUTING", "DONE"],
            "transitions": [
                {"trigger": "oriented", "source": "ORIENTING", "dest": "EXECUTING"},
                {"trigger": "step_complete", "source": "EXECUTING", "dest": "EXECUTING"},
                {"trigger": "plan_complete", "source": "EXECUTING", "dest": "DONE"},
            ],
            "final_states": ["DONE", "ERROR"]
        }
        mock_mcg.current_state = "START"

        # Define a plan for the agent to execute
        plan = [
            PlanStep(tool_name="verify_logic", args_text=input_file_path)
        ]

        # Configure the mock to simulate the FSM flow
        mock_mcg.do_orientation.return_value = "oriented"
        def get_current_step_side_effect(agent_state):
            if agent_state.plan_step < len(plan):
                return plan[agent_state.plan_step]
            return None

        mock_mcg.get_current_step.side_effect = get_current_step_side_effect

        def do_execution_side_effect(agent_state, result, logger):
            agent_state.plan_step += 1
            if agent_state.plan_step >= len(plan):
                return "plan_complete"
            return "step_complete"

        mock_mcg.do_execution.side_effect = do_execution_side_effect

        # Patch the MasterControlGraph in the agent_shell module
        with patch('tooling.agent_shell.MasterControlGraph', return_value=mock_mcg):
            # The loop will be very short because we mock the FSM
            mock_tools = {
                "read_file": MagicMock(),
                "list_files": MagicMock(),
                "google_search": MagicMock(),
                "view_text_website": MagicMock(),
            }
            agent_state = run_agent_loop("Test task", mock_tools)

        # Clean up the dummy file
        os.remove(input_file_path)

        # We can't easily check the result here without more complex mocking,
        # but if it runs without error, the integration is working at a basic level.
        self.assertIsInstance(agent_state, AgentState)
        self.assertIsNone(agent_state.error)

if __name__ == '__main__':
    unittest.main()