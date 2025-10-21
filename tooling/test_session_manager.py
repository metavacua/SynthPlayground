"""
Tests for the session_manager tool.
"""

import os
import json
import unittest
import tempfile
from tooling.state import AgentState, PlanContext
from tooling.plan_parser import Command
from tooling.session_manager import save_session, load_session

class TestSessionManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.session_file = os.path.join(self.temp_dir.name, 'session.json')
        # Override the default session file path for testing
        import tooling.session_manager
        tooling.session_manager.SESSION_FILE = self.session_file

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_session(self):
        """
        Tests that a session can be saved and then loaded correctly.
        """
        command = Command(tool_name='message_user', args_text='{"message": "Hello"}')
        plan_context = PlanContext(
            plan_path='plans/test_plan.txt',
            commands=[command],
            current_step=0
        )
        original_state = AgentState(
            task='Test task',
            plan_path='plans/test_plan.txt',
            plan_stack=[plan_context],
            messages=[{'role': 'user', 'content': 'Test message'}],
            orientation_complete=True,
            vm_capability_report='OK',
            research_findings={'topic': 'finding'},
            draft_postmortem_path='postmortems/draft.md',
            final_report='Done',
            error=None
        )

        save_session(original_state)
        loaded_state = load_session()

        self.assertEqual(original_state.task, loaded_state.task)
        self.assertEqual(original_state.plan_path, loaded_state.plan_path)
        self.assertEqual(len(original_state.plan_stack), len(loaded_state.plan_stack))

        # Compare plan context in detail
        original_pc = original_state.plan_stack[0]
        loaded_pc = loaded_state.plan_stack[0]
        self.assertEqual(original_pc.plan_path, loaded_pc.plan_path)
        self.assertEqual(original_pc.current_step, loaded_pc.current_step)
        self.assertEqual(len(original_pc.commands), len(loaded_pc.commands))
        self.assertEqual(original_pc.commands[0].tool_name, loaded_pc.commands[0].tool_name)
        self.assertEqual(original_pc.commands[0].args_text, loaded_pc.commands[0].args_text)

        self.assertEqual(original_state.messages, loaded_state.messages)
        self.assertEqual(original_state.orientation_complete, loaded_state.orientation_complete)
        self.assertEqual(original_state.vm_capability_report, loaded_state.vm_capability_report)
        self.assertEqual(original_state.research_findings, loaded_state.research_findings)
        self.assertEqual(original_state.draft_postmortem_path, loaded_state.draft_postmortem_path)
        self.assertEqual(original_state.final_report, loaded_state.final_report)
        self.assertEqual(original_state.error, loaded_state.error)

    def test_load_no_session(self):
        """
        Tests that a new session is created if no session file exists.
        """
        # Ensure the session file does not exist
        if os.path.exists(self.session_file):
            os.remove(self.session_file)

        loaded_state = load_session()
        self.assertIsInstance(loaded_state, AgentState)
        self.assertEqual(loaded_state.task, "New Task")
        self.assertEqual(loaded_state.plan_stack, [])

if __name__ == '__main__':
    unittest.main()
