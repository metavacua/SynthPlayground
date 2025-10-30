import unittest
import os
import sys

# Add the root directory to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from tooling.state import AgentState

class TestAgentState(unittest.TestCase):
    """
    Tests the AgentState class.
    """

    def test_initialization(self):
        """
        Verify that the AgentState class is initialized correctly.
        """
        agent_state = AgentState(task="test_task")
        self.assertEqual(agent_state.task, "test_task")
        self.assertEqual(agent_state.messages, [])
        self.assertEqual(agent_state.plan_stack, [])
        self.assertEqual(agent_state.research_findings, {})
        self.assertEqual(agent_state.background_processes, {})
        self.assertEqual(agent_state.error, None)

if __name__ == "__main__":
    unittest.main()
