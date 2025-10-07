import unittest
import sys
import os
import threading
import time
import json
import datetime
from unittest.mock import patch, MagicMock

# Add tooling directory to path to import other tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from master_control import MasterControlGraph
from state import AgentState

class TestMasterControlGraphIntegrated(unittest.TestCase):
    """
    Tests the fully integrated FSM workflow, including validation and
    automated post-mortem generation.
    """

    def setUp(self):
        self.plan_file = "plan.txt"
        self.step_complete_file = "step_complete.txt"
        self.task_id = "test-integrated-workflow-task"
        # Sanitize task_id for filename
        safe_task_id = "".join(c for c in self.task_id if c.isalnum() or c in ('-', '_'))
        self.postmortem_file = f"postmortems/{datetime.date.today()}-{safe_task_id}.md"
        self.test_output_file = "test_output.txt"


        # Clean up files from previous runs
        for f in [self.plan_file, self.step_complete_file, self.postmortem_file, self.test_output_file]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        # Ensure all temp files are cleaned up
        for f in [self.plan_file, self.step_complete_file, self.postmortem_file, self.test_output_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_full_integrated_workflow(self):
        """
        Validates the full, integrated FSM flow: plan validation,
        step-by-step execution, and automated post-mortem.
        """
        # 1. Define a valid, command-based plan for the validator
        test_plan = (
            'set_plan "A valid test plan that creates a file"\n'
            'plan_step_complete "Create a test file"\n'
            f'create_file_with_block {self.test_output_file} "content"\n'
            f'run_in_bash_session close --task-id {self.task_id}\n'
            'submit'
        )
        plan_steps = [step for step in test_plan.split('\n') if step.strip()]

        final_state_container = {}

        # 2. Define the target function to run the FSM in a thread
        def run_fsm():
            initial_state = AgentState(task=self.task_id)
            graph = MasterControlGraph()
            final_state = graph.run(initial_state)
            final_state_container['final_state'] = final_state

        # 3. Start the FSM
        fsm_thread = threading.Thread(target=run_fsm)
        fsm_thread.start()

        # 4. Create the plan file to trigger planning and validation
        time.sleep(1) # Allow FSM to hit the plan wait loop
        with open(self.plan_file, "w") as f:
            f.write(test_plan)

        # 5. Sequentially signal completion for each step in the plan
        for i, step in enumerate(plan_steps):
            time.sleep(1.5) # Allow FSM to process and wait for next signal
            with open(self.step_complete_file, "w") as f:
                f.write(f"Successfully signaled completion for step {i+1}.")

        # 6. Wait for the FSM thread to complete
        fsm_thread.join(timeout=20) # Increased timeout for full flow
        self.assertFalse(fsm_thread.is_alive(), "FSM thread did not complete in time.")

        # 7. Assertions
        self.assertIn('final_state', final_state_container, "Final state was not captured.")
        final_state = final_state_container['final_state']

        self.assertIsNone(final_state.error, f"FSM ended in an error state: {final_state.error}")
        self.assertEqual(final_state.plan, test_plan)
        self.assertEqual(final_state.current_step_index, len(plan_steps))

        # Check that the post-mortem was created and the report reflects it
        self.assertTrue(os.path.exists(self.postmortem_file), f"Post-mortem file was not created at {self.postmortem_file}")
        self.assertIn(f"Post-mortem successfully generated for task: {self.task_id}", final_state.final_report)

        # Check that transient files were cleaned up
        self.assertFalse(os.path.exists(self.plan_file))
        self.assertFalse(os.path.exists(self.step_complete_file))

if __name__ == "__main__":
    # Create postmortems dir if it doesn't exist to avoid test failure
    if not os.path.exists("postmortems"):
        os.makedirs("postmortems")
    unittest.main()