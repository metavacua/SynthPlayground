import unittest
import os
import sys
from unittest.mock import MagicMock

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from tooling.master_control import MasterControlGraph
from tooling.state import AgentState
from utils.logger import Logger


class TestProtocolEnforcement(unittest.TestCase):
    """
    Tests the enforcement of critical, system-wide protocols.
    """

    def setUp(self):
        """Set up common objects for the tests."""
        self.agent_state = AgentState(task="test_task")
        # Mock the logger to prevent it from writing to a file
        self.logger = MagicMock(spec=Logger)
        self.mcg = MasterControlGraph()

    def test_reset_all_prohibition_protocol(self):
        """
        Verify that the 'reset-all-prohibition-001' protocol is enforced.

        This test checks that the MasterControl orchestrator's planning phase
        will identify a call to the forbidden `reset_all` tool within a plan
        and will refuse to validate it. This is a direct test of a critical,
        hard-coded safety protocol.
        """
        # A plan that attempts to use the forbidden tool
        malicious_plan = "reset_all"

        # The protocol dictates that an attempt to use `reset_all` should be
        # caught during the planning phase. The `do_planning` method should
        # return a trigger that leads to the ERROR state.
        trigger = self.mcg.do_planning(self.agent_state, malicious_plan, self.logger)

        # We expect the plan to be rejected and the FSM to transition to the ERROR state.
        expected_trigger = self.mcg.get_trigger("PLANNING", "ERROR")
        self.assertEqual(trigger, expected_trigger)
        self.assertIn(
            "CRITICAL: Use of the forbidden tool `reset_all` was detected in the plan.",
            self.agent_state.error,
        )


if __name__ == "__main__":
    unittest.main()
