import unittest
import sys
import os
import threading
import time
import datetime
from unittest.mock import patch

# Add tooling directory to path to import other tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from master_control import MasterControlGraph
from state import AgentState, PlanContext


class TestMasterControlGraphFullWorkflow(unittest.TestCase):
    """
    Tests the fully integrated FSM workflow, including plan validation,
    active execution, and the interactive analysis phase.
    """

    def setUp(self):
        self.task_id = "test-full-atomic-workflow"
        # Sanitize task_id for filename safety
        safe_task_id = "".join(
            c for c in self.task_id if c.isalnum() or c in ("-", "_")
        )

        # Define all file paths used in the test
        self.plan_file = "plan.txt"
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
        Validates the entire FSM flow: plan validation, active step-by-step
        execution, interactive analysis, and finalization.
        """
        # 1. Define a complete and valid command-based plan for the validator
        test_plan = (
            'set_plan "A valid test plan for the full workflow"\n'
            'plan_step_complete "This is the step that transitions to executing"\n'
            f'create_file_with_block {self.test_output_file} "content"\n'
            f'run_in_bash_session python3 tooling/fdc_cli.py close --task-id {self.task_id}\n'
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

        # 5. Manually signal completion for each step in the plan to drive the FSM.
        # The FSM's execution model is passive; it waits for an agent to signal
        # that a step has been completed by creating 'step_complete.txt'.
        time.sleep(1)  # Allow FSM to transition to EXECUTING state.

        for i, step in enumerate(plan_steps):
            # The FSM's main loop sleeps for 1s, so we wait for it to be ready.
            time.sleep(1.5)
            with open("step_complete.txt", "w") as f:
                f.write(f"Step {i+1} '{step}' complete.")

        # 6. Wait for the FSM to transition to AWAITING_ANALYSIS and create the draft post-mortem.
        timeout = 15  # seconds
        start_time = time.time()
        while not os.path.exists(self.draft_postmortem_file):
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                self.fail("FSM did not create draft post-mortem in time.")

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

        # 6. Signal that analysis is complete
        with open(self.analysis_complete_file, "w") as f:
            f.write("done")

        # 7. Wait for the FSM thread to complete its entire run
        fsm_thread.join(timeout=10)
        self.assertFalse(fsm_thread.is_alive(), "FSM thread did not complete in time.")

        # 8. Assertions
        self.assertIn(
            "final_state", final_state_container, "Final state object was not captured."
        )
        final_state = final_state_container["final_state"]

        self.assertIsNone(
            final_state.error, f"FSM ended in an error state: {final_state.error}"
        )
        # The plan is no longer stored directly; we assert the stack is empty on completion.
        self.assertEqual(len(final_state.plan_stack), 0)

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
        self.assertIn("Automated Performance Analysis", postmortem_content) # Check for new section
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
        self.assertFalse(os.path.exists(self.draft_postmortem_file))
        self.assertFalse(os.path.exists(self.analysis_complete_file))


class TestCFDCWorkflow(unittest.TestCase):
    """
    Tests the new Context-Free Development Cycle (CFDC) functionality,
    including hierarchical plans and recursion depth limits.
    """

    def setUp(self):
        self.task_id = "test-cfdc-task"
        self.sub_plan_file = "sub_plan.txt"
        self.step_complete_file = "step_complete.txt"
        self.analysis_complete_file = "analysis_complete.txt"
        self.output_file = "sub_plan_output.txt"
        self.draft_postmortem_file = f"DRAFT-{self.task_id}.md"
        self.root_plan_file = "plan.txt"
        self.cleanup_files()

    def tearDown(self):
        self.cleanup_files()

    def cleanup_files(self):
        """Helper function to remove all files created during the test."""
        files_to_delete = [
            self.sub_plan_file,
            self.step_complete_file,
            self.analysis_complete_file,
            self.output_file,
            self.root_plan_file,
            self.draft_postmortem_file,
        ]
        for f in os.listdir("postmortems"):
            if self.task_id in f:
                files_to_delete.append(os.path.join("postmortems", f))
        for f in files_to_delete:
            if os.path.exists(f):
                os.remove(f)

    def test_hierarchical_plan_execution(self):
        """
        Validates that the FSM can execute a plan that calls a sub-plan,
        where each plan is a valid, self-contained FSM traversal.
        """
        # 1. Define a complete, valid sub-plan
        sub_plan_content = (
            'set_plan "Sub-plan"\n'
            'plan_step_complete "Transition to executing in sub-plan"\n'
            f'create_file_with_block {self.output_file} "hello from sub-plan"\n'
            f"run_in_bash_session close --task-id {self.task_id}-sub\n"
            "submit"
        )
        with open(self.sub_plan_file, "w") as f:
            f.write(sub_plan_content)

        # 2. Define a complete, valid main plan that calls the sub-plan
        main_plan_content = (
            'set_plan "Hierarchical plan"\n'
            'plan_step_complete "Transition to executing in main plan"\n'
            f"call_plan {self.sub_plan_file}\n"
            f"run_in_bash_session close --task-id {self.task_id}\n"
            "submit"
        )
        with open(self.root_plan_file, "w") as f:
            f.write(main_plan_content)

        final_state_container = {}

        # 3. Run the FSM in a thread
        def run_fsm():
            initial_state = AgentState(task=self.task_id)
            graph = MasterControlGraph()
            final_state = graph.run(initial_state)
            final_state_container["final_state"] = final_state
            final_state_container["final_fsm_state"] = graph.current_state

        fsm_thread = threading.Thread(target=run_fsm)
        fsm_thread.start()

        # 4. Signal completion for every step in the correct order
        time.sleep(1.5)
        # Main plan steps
        with open(self.step_complete_file, "w") as f:
            f.write("set_plan complete.")
        time.sleep(1.5)
        with open(self.step_complete_file, "w") as f:
            f.write("plan_step_complete complete.")
        time.sleep(1.5)
        # Sub-plan steps
        with open(self.step_complete_file, "w") as f:
            f.write("sub set_plan complete.")
        time.sleep(1.5)
        with open(self.step_complete_file, "w") as f:
            f.write("sub plan_step_complete complete.")
        time.sleep(1.5)
        # Manually perform the action from the plan step, as the agent would
        with open(self.output_file, "w") as f:
            f.write("hello from sub-plan")
        with open(self.step_complete_file, "w") as f:
            f.write("sub create_file complete.")
        time.sleep(1.5)
        with open(self.step_complete_file, "w") as f:
            f.write("sub close complete.")
        time.sleep(1.5)
        with open(self.step_complete_file, "w") as f:
            f.write("sub submit complete.")
        time.sleep(1.5)
        # Final main plan steps
        with open(self.step_complete_file, "w") as f:
            f.write("main close complete.")
        time.sleep(1.5)
        with open(self.step_complete_file, "w") as f:
            f.write("main submit complete.")

        # 5. Wait for the FSM to create the draft post-mortem
        draft_created = False
        for _ in range(10):
            if os.path.exists(self.draft_postmortem_file):
                draft_created = True
                break
            time.sleep(0.5)
        self.assertTrue(
            draft_created, "Draft post-mortem file was not created in time."
        )

        # 6. Signal analysis is complete
        with open(self.analysis_complete_file, "w") as f:
            f.write("Analysis complete.")

        # 7. Wait for FSM thread to finish
        fsm_thread.join(timeout=30)
        self.assertFalse(fsm_thread.is_alive(), "FSM thread timed out.")

        # 8. Assertions
        final_state = final_state_container["final_state"]
        self.assertIsNone(final_state.error, f"FSM ended in error: {final_state.error}")
        self.assertEqual(final_state_container["final_fsm_state"], "AWAITING_SUBMISSION")

        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r") as f:
            self.assertEqual(f.read(), "hello from sub-plan")

    def test_recursion_depth_limit(self):
        """
        Validates that the FSM correctly terminates when the recursion
        depth limit is exceeded.
        """
        # 1. Create a fully valid, self-contained plan that calls itself.
        recursive_plan_content = (
            'set_plan "Recursive plan"\n'
            'plan_step_complete "Transition to executing"\n'
            f"call_plan {self.root_plan_file}\n"
            f"run_in_bash_session close --task-id {self.task_id}-recursive\n"
            "submit"
        )
        with open(self.root_plan_file, "w") as f:
            f.write(recursive_plan_content)

        final_state_container = {}

        # 2. Run the FSM in a thread, patching the depth limit for a fast test
        def run_fsm():
            initial_state = AgentState(task=self.task_id)
            graph = MasterControlGraph()
            with patch("master_control.MAX_RECURSION_DEPTH", 3):
                final_state = graph.run(initial_state)
            final_state_container["final_state"] = final_state
            final_state_container["final_fsm_state"] = graph.current_state

        fsm_thread = threading.Thread(target=run_fsm)
        fsm_thread.start()

        # 3. Signal completion for the first two steps to kick off the recursion
        time.sleep(1.5)
        with open(self.step_complete_file, "w") as f:
            f.write("set_plan complete.")
        time.sleep(1.5)
        with open(self.step_complete_file, "w") as f:
            f.write("plan_step_complete complete.")

        # 4. Wait for FSM to fail on its own due to recursion
        fsm_thread.join(timeout=15)
        self.assertFalse(fsm_thread.is_alive(), "FSM thread timed out.")

        # 5. Assertions
        final_state = final_state_container["final_state"]
        self.assertEqual(final_state_container["final_fsm_state"], "ERROR")
        self.assertIsNotNone(final_state.error)
        self.assertIn("Maximum recursion depth", final_state.error)
        self.assertIn("exceeded", final_state.error)


if __name__ == "__main__":
    # Create postmortems dir if it doesn't exist to avoid test failure
    if not os.path.exists("postmortems"):
        os.makedirs("postmortems")
    unittest.main()