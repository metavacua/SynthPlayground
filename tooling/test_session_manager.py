"""
Tests for the session_manager tool.
"""

import unittest
import os
import json
from tooling.state import AgentState
from tooling.session_manager import save_session, load_session

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.session_file = "test_session.json"
        import tooling.session_manager
        tooling.session_manager.SESSION_FILE = self.session_file

    def tearDown(self):
        if os.path.exists(self.session_file):
            os.remove(self.session_file)

    def test_save_and_load_session(self):
        # Create a sample AgentState
        agent_state = AgentState()
        agent_state.task = "test_task"
        agent_state.task_description = "This is a test task."
        agent_state.research_findings = ["Finding 1", "Finding 2"]

        # Save the session
        save_session(agent_state)

        # Load the session
        loaded_state = load_session()

        # Check that the loaded state is the same as the original state
        self.assertEqual(loaded_state.task, agent_state.task)
        self.assertEqual(loaded_state.task_description, agent_state.task_description)
        self.assertEqual(loaded_state.research_findings, agent_state.research_findings)

    def test_load_session_no_file(self):
        # Load a session when the file doesn't exist
        loaded_state = load_session()

        # Check that a new AgentState is returned
        self.assertIsInstance(loaded_state, AgentState)
        self.assertIsNone(loaded_state.task)

if __name__ == '__main__':
    unittest.main()
