import unittest
import sys
import os
import threading
import time
import datetime

# Add tooling directory to path to import other tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from master_control import MasterControlGraph
from state import AgentState


class TestMasterControlGraphFullWorkflow(unittest.TestCase):
    """
    Tests the fully integrated FSM workflow, including plan validation,
    interactive execution, and the new interactive analysis phase.
    """

    def setUp(self):
        self.task_id = "test-full-atomic-workflow"
        # Sanitize task_id for filename safety
        safe_task_id = "".join(
            c for c in self.task_id if c.isalnum() or c in ("-", "_")
        )

        # Define all file paths used in the test
        self.plan_file = "plan.txt"
        self.step_complete_file = "step_complete.txt"
        self.analysis_complete_file = "analysis_complete.txt"
        self.draft_postmortem_file = f"DRAFT-{self.task_id}.md"
        self.final_postmortem_file = (
            f"postmortems/{datetime.date.today()}-{safe_task_id}.md"
        )
        self.test_output_file = "test_output.txt"
        self.lessons_learned_file = "knowledge_core/lessons_learned.md"

        # Clean up all potential artifacts from previous runs
        self.cleanup_files()

        # Backup original lessons if it exists and create a fresh one for the test
        if os.path.exists(self.lessons_learned_file):
            os.rename(self.lessons_learned_file, self.lessons_learned_file + ".bak")
        with open(self.lessons_learned_file, "w") as f:
            f.write("# Lessons Learned\n")

    def tearDown(self):
        self.cleanup_files()
        # Clean up the test lessons learned and restore backup
        if os.path.exists(self.lessons_learned_file):
            os.remove(self.lessons_learned_file)
        if os.path.exists(self.lessons_learned_file + ".bak"):
            os.rename(self.lessons_learned_file + ".bak", self.lessons_learned_file)

    def cleanup_files(self):
        """Helper function to remove all files created during the test."""
        files_to_delete = [
            self.plan_file,
            self.step_complete_file,
            self.analysis_complete_file,
            self.draft_postmortem_file,
            self.final_postmortem_file,
            self.test_output_file,
        ]
        for f in files_to_delete:
            if os.path.exists(f):
                os.remove(f)

    def test_full_atomic_workflow_with_analysis(self):
        """
        Validates the entire FSM flow: plan validation, step-by-step
        execution, interactive analysis, and finalization.
        """
        # 1. Define a complete and valid command-based plan for the validator
        test_plan = (
            'set_plan "A valid test plan for the full workflow"\n'
            'plan_step_complete "This is the step that transitions to executing"\n'
            f'create_file_with_block {self.test_output_file} "content"\n'
            f"run_in_bash_session close --task-id {self.task_id}\n"
            "submit"
        )
        plan_steps = [step for step in test_plan.split("\n") if step.strip()]

        final_state_container = {}

        # 2. Define the target function to run the FSM in a thread
        def run_fsm():
            initial_state = AgentState(task=self.task_id)
            graph = MasterControlGraph()
            final_state = graph.run(initial_state)
            final_state_container["final_state"] = final_state
            final_state_container["final_fsm_state"] = graph.current_state

        # 3. Start the FSM thread
        fsm_thread = threading.Thread(target=run_fsm)
        fsm_thread.start()

        # 4. Create the plan file to trigger planning and validation
        time.sleep(1)  # Allow FSM to hit the plan wait loop
        self.assertFalse(os.path.exists(self.plan_file))
        with open(self.plan_file, "w") as f:
            f.write(test_plan)

        # 5. Sequentially signal completion for each execution step
        for i, step in enumerate(plan_steps):
            time.sleep(1.5)  # Allow FSM to process and wait for the next signal
            with open(self.step_complete_file, "w") as f:
                f.write(f"Successfully signaled execution for step {i+1}.")

        # 6. Wait for the FSM to create the draft post-mortem, then "analyze" it
        time.sleep(1.5)  # Allow FSM to transition to AWAITING_ANALYSIS
        self.assertTrue(
            os.path.exists(self.draft_postmortem_file),
            "Draft post-mortem file was not created.",
        )

        # This content simulates the agent filling out the draft file.
        analysis_content = f"""
# Post-Mortem Report
**Task ID:** `{self.task_id}`
**Completion Date:** `{datetime.date.today()}`
---
## 1. Task Summary
A test summary.
---
## 2. Process Analysis
A test analysis.
---
## 3. Corrective Actions & Lessons Learned

1. **Lesson:** This is a test lesson from the integration test.
   **Action:** The corresponding test action.
---
"""
        # Overwrite the draft file with the now-completed analysis
        with open(self.draft_postmortem_file, "w") as f:
            f.write(analysis_content)

        # 7. Signal that analysis is complete
        with open(self.analysis_complete_file, "w") as f:
            f.write("done")

        # 8. Wait for the FSM thread to complete its entire run
        fsm_thread.join(timeout=25)  # Increased timeout for the full, complex flow
        self.assertFalse(fsm_thread.is_alive(), "FSM thread did not complete in time.")

        # 9. Assertions
        self.assertIn(
            "final_state", final_state_container, "Final state object was not captured."
        )
        final_state = final_state_container["final_state"]

        self.assertIsNone(
            final_state.error, f"FSM ended in an error state: {final_state.error}"
        )
        self.assertEqual(final_state.plan, test_plan)
        self.assertEqual(final_state.current_step_index, len(plan_steps))

        # Assert that the FSM ended in the correct pre-submission state
        self.assertIn(
            "final_fsm_state",
            final_state_container,
            "Final FSM state was not captured.",
        )
        self.assertEqual(
            final_state_container["final_fsm_state"], "AWAITING_SUBMISSION"
        )

        # Assert that the final post-mortem file was created and contains the analysis
        self.assertTrue(
            os.path.exists(self.final_postmortem_file),
            f"Final post-mortem file was not created at {self.final_postmortem_file}",
        )
        with open(self.final_postmortem_file, "r") as f:
            postmortem_content = f.read()
        self.assertIn(
            "This is a test lesson from the integration test.", postmortem_content
        )
        self.assertIn(
            f"Post-mortem analysis finalized. Report saved to '{self.final_postmortem_file}'",
            final_state.final_report,
        )

        # Assert that the knowledge core was updated
        with open(self.lessons_learned_file, "r") as f:
            lessons_content = f.read()
        self.assertIn(
            "Insight:** This is a test lesson from the integration test.",
            lessons_content,
        )
        self.assertIn(
            "Actionable Guidance:** The corresponding test action.", lessons_content
        )

        # Assert that all transient files were cleaned up correctly
        self.assertFalse(os.path.exists(self.plan_file))
        self.assertFalse(os.path.exists(self.step_complete_file))
        self.assertFalse(os.path.exists(self.draft_postmortem_file))
        self.assertFalse(os.path.exists(self.analysis_complete_file))


if __name__ == "__main__":
    # Create postmortems dir if it doesn't exist to avoid test failure
    if not os.path.exists("postmortems"):
        os.makedirs("postmortems")
    unittest.main()
