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
    Tests the interactive planning feature of the MasterControlGraph.
    """

    def setUp(self):
        self.plan_file = "plan.txt"
        if os.path.exists(self.plan_file):
            os.remove(self.plan_file)

    def tearDown(self):
        if os.path.exists(self.plan_file):
            os.remove(self.plan_file)

    def test_interactive_planning_flow(self):
        """
        Validates that the FSM waits for a plan file, reads it,
        and transitions correctly.
        """
        # 1. Define a test plan to be written to the file
        test_plan = "1. *Test Step:* This is a test plan."

        # 2. Define the target function for the thread
        def run_fsm():
            # The FSM will run, but we will capture its final state
            # by mocking the run method's return
            task = "Test interactive planning."
            initial_state = AgentState(task=task)
            graph = MasterControlGraph()
            # We don't need the full run, just to check the state after planning
            # So we'll run the states manually for more control

            # ORIENTING
            orienting_trigger = graph.do_orientation(initial_state)
            self.assertEqual(orienting_trigger, "orientation_succeeded")
            graph.current_state = "PLANNING"

            # PLANNING
            planning_trigger = graph.do_planning(initial_state)
            self.assertEqual(planning_trigger, "plan_is_set")
            graph.current_state = "EXECUTING"

            # Assertions about the state after planning
            self.assertEqual(initial_state.plan, test_plan)
            self.assertFalse(os.path.exists(self.plan_file)) # Check cleanup

        # 3. Create and run the FSM in a separate thread
        fsm_thread = threading.Thread(target=run_fsm)

        # 4. Give the FSM time to start and enter the waiting state
        # In a real scenario, we'd need a more robust sync mechanism,
        # but for this test, a short sleep after starting the thread
        # and before creating the file is sufficient.
        fsm_thread.start()

        # Give it a moment to hit the wait loop in do_planning
        time.sleep(0.5)

        # 5. Create the plan file to unblock the FSM
        with open(self.plan_file, "w") as f:
            f.write(test_plan)

        # 6. Wait for the FSM thread to complete
        fsm_thread.join(timeout=5) # Timeout to prevent hanging tests

        self.assertFalse(fsm_thread.is_alive(), "FSM thread did not complete in time.")

if __name__ == "__main__":
    unittest.main()