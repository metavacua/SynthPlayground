import unittest
import os
import sys
from unittest.mock import MagicMock, patch, mock_open

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from tooling.master_control import MasterControlGraph
from tooling.state import AgentState
from utils.logger import Logger

class TestMasterControl(unittest.TestCase):
    """
    Tests the MasterControlGraph FSM.
    """

    def setUp(self):
        """Set up common objects for the tests."""
        self.agent_state = AgentState(task="test_task")
        # Mock the logger to prevent it from writing to a file
        self.logger = MagicMock(spec=Logger)
        self.mcg = MasterControlGraph()

    @patch('os.path.exists', return_value=False)
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open, read_data="audit report content")
    @patch('tooling.master_control.MasterControlGraph._validate_plan_with_cli', return_value=(True, ""))
    def test_fsm_transitions(self, mock_validate_plan, mock_open_file, mock_subprocess, mock_os_path_exists):
        """
        Verify that the FSM transitions are working correctly.
        """
        # Configure subprocess.run mock to simulate success
        mock_subprocess.return_value = MagicMock(returncode=0)

        # Check that the initial state is correct
        self.assertEqual(self.mcg.current_state, "START")

        # Mock the tools
        tools = {'list_files': MagicMock(return_value=["file1.py", "file2.py"])}

        # Set current state to ORIENTING to test the do_orientation method
        self.mcg.current_state = "ORIENTING"

        # Call do_orientation and check the trigger
        trigger = self.mcg.do_orientation(self.agent_state, self.logger, tools)
        self.assertEqual(trigger, self.mcg.get_trigger("ORIENTING", "PLANNING"))

        # Set current state to PLANNING to test the do_planning method
        self.mcg.current_state = "PLANNING"

        # Call do_planning and check the trigger
        plan_content = "set_plan: This is a test plan.\nplan_step_complete: Done."
        trigger = self.mcg.do_planning(self.agent_state, plan_content, self.logger)
        self.assertEqual(trigger, self.mcg.get_trigger("PLANNING", "EXECUTING"))

if __name__ == "__main__":
    unittest.main()
