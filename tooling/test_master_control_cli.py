import unittest
from unittest.mock import patch
from tooling.master_control_cli import main as master_control_main
from tooling.state import AgentState


class TestMasterControlCli(unittest.TestCase):

    @patch("sys.argv", ["tooling/master_control_cli.py", "Test task"])
    @patch("tooling.master_control_cli.run_agent_loop")
    def test_main_calls_run_agent_loop(self, mock_run_agent_loop):
        """Tests that the main function calls the agent shell's run_agent_loop."""
        # Mock the return value of run_agent_loop to be a valid AgentState object
        mock_run_agent_loop.return_value = AgentState(task="test")

        master_control_main()

        mock_run_agent_loop.assert_called_once_with(task_description="Test task")


if __name__ == "__main__":
    unittest.main()
