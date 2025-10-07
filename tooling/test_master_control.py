import unittest
import sys
import os
import threading
import time
import json
from unittest.mock import patch, MagicMock

# Add tooling directory to path to import other tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from master_control import MasterControlGraph
from state import AgentState

class TestMasterControlGraphInteractive(unittest.TestCase):
    """
    Tests the interactive planning and execution features of the MasterControlGraph.
    """

    def setUp(self):
        self.plan_file = "plan.txt"
        self.step_complete_file = "step_complete.txt"
        if os.path.exists(self.plan_file):
            os.remove(self.plan_file)
        if os.path.exists(self.step_complete_file):
            os.remove(self.step_complete_file)

    def tearDown(self):
        if os.path.exists(self.plan_file):
            os.remove(self.plan_file)
        if os.path.exists(self.step_complete_file):
            os.remove(self.step_complete_file)

    def test_interactive_planning_and_execution_flow(self):
        """
        Validates the full FSM flow: waiting for a plan, then executing
        each step based on file signals.
        """
        # 1. Define a multi-step test plan
        test_plan = "1. First test step.\n2. Second test step."
        plan_steps = [step for step in test_plan.split('\n') if step.strip()]

        # This will hold the final state of the FSM for inspection
        final_state_container = {}

        # 2. Define the target function for the thread to run the FSM
        def run_fsm():
            task = "Test interactive planning and execution."
            initial_state = AgentState(task=task)
            graph = MasterControlGraph()
            # Run the entire FSM
            final_state = graph.run(initial_state)
            final_state_container['final_state'] = final_state

        # 3. Create and start the FSM thread
        fsm_thread = threading.Thread(target=run_fsm)
        fsm_thread.start()

        # 4. Give the FSM time to start and wait for the plan
        time.sleep(0.5) # Wait for FSM to hit the plan wait loop
        with open(self.plan_file, "w") as f:
            f.write(test_plan)

        # 5. Sequentially signal completion for each step
        for i, step in enumerate(plan_steps):
            # Wait for the FSM to be waiting for the next step signal
            time.sleep(1.5) # Needs to be >1s to account for FSM polling interval
            with open(self.step_complete_file, "w") as f:
                f.write(f"Successfully completed step {i+1}.")

        # 6. Wait for the FSM thread to complete
        fsm_thread.join(timeout=10)
        self.assertFalse(fsm_thread.is_alive(), "FSM thread did not complete in time.")

        # 7. Assertions
        self.assertIn('final_state', final_state_container, "Final state was not captured.")
        final_state = final_state_container['final_state']

        self.assertIsNone(final_state.error, f"FSM ended in an error state: {final_state.error}")
        self.assertEqual(final_state.plan, test_plan)
        self.assertEqual(final_state.current_step_index, len(plan_steps))
        self.assertIn("Final report for task", final_state.final_report)

        # Check that cleanup happened
        self.assertFalse(os.path.exists(self.plan_file))
        self.assertFalse(os.path.exists(self.step_complete_file))

if __name__ == "__main__":
    unittest.main()