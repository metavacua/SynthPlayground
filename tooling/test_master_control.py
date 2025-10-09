import unittest
import sys
import os
import threading
import time
import datetime
import json
import subprocess
from unittest.mock import patch

# Add tooling directory to path to import other tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from master_control import MasterControlGraph
from state import AgentState, PlanContext


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
        time.sleep(1)
        self.assertFalse(os.path.exists(self.plan_file))
        with open(self.plan_file, "w") as f:
            f.write(test_plan)

        # 5. Sequentially signal completion for each execution step
        for i, step in enumerate(plan_steps):
            time.sleep(1.5)
            with open(self.step_complete_file, "w") as f:
                f.write(f"Successfully signaled execution for step {i+1}.")

        # 6. Wait for the FSM to create the draft post-mortem, then "analyze" it
        time.sleep(1.5)
        self.assertTrue(
            os.path.exists(self.draft_postmortem_file),
            "Draft post-mortem file was not created.",
        )

        analysis_content = f"""
# Post-Mortem Report
**Task ID:** `{self.task_id}`
"""
        with open(self.draft_postmortem_file, "w") as f:
            f.write(analysis_content)

        # 7. Signal that analysis is complete
        with open(self.analysis_complete_file, "w") as f:
            f.write("done")

        # 8. Wait for the FSM thread to complete its entire run
        fsm_thread.join(timeout=25)
        self.assertFalse(fsm_thread.is_alive(), "FSM thread did not complete in time.")

        # 9. Assertions
        final_state = final_state_container["final_state"]
        self.assertIsNone(
            final_state.error, f"FSM ended in an error state: {final_state.error}"
        )
        self.assertEqual(len(final_state.plan_stack), 0)
        self.assertEqual(
            final_state_container["final_fsm_state"], "AWAITING_SUBMISSION"
        )
        self.assertTrue(os.path.exists(self.final_postmortem_file))


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
        self.plan_registry_file = os.path.join(
            "knowledge_core", "plan_registry.json"
        )
        self.cleanup_files()
        with open(self.plan_registry_file, "w") as f:
            json.dump({}, f)

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
            self.plan_registry_file,
        ]
        for f in os.listdir("postmortems"):
            if self.task_id in f:
                files_to_delete.append(os.path.join("postmortems", f))
        for f in files_to_delete:
            if os.path.exists(f):
                os.remove(f)

    def test_plan_registry_execution(self):
        """
        Validates that the FSM can execute a plan by its logical name
        from the plan registry.
        """
        # 1. Register a plan using the plan_manager tool
        sub_plan_name = "create-hello-file"
        sub_plan_content = (
            'set_plan "Sub-plan"\n'
            'plan_step_complete " "\n'
            f'create_file_with_block {self.output_file} "hello from registry"\n'
            'run_in_bash_session close --task-id sub-task\n'
            'submit'
        )
        with open(self.sub_plan_file, "w") as f:
            f.write(sub_plan_content)

        register_cmd = ["python3", "tooling/plan_manager.py", "register", sub_plan_name, self.sub_plan_file]
        subprocess.run(register_cmd, check=True)

        # 2. Define a main plan that calls the registered plan by its logical name
        main_plan_content = (
            'set_plan "Main plan"\n'
            'plan_step_complete " "\n'
            f"call_plan {sub_plan_name}\n"
            'run_in_bash_session close --task-id main-task\n'
            'submit'
        )
        with open(self.root_plan_file, "w") as f:
            f.write(main_plan_content)

        # 3. Run the FSM
        final_state_container = {}
        def run_fsm():
            initial_state = AgentState(task=self.task_id)
            graph = MasterControlGraph()
            final_state = graph.run(initial_state)
            final_state_container["final_state"] = final_state

        fsm_thread = threading.Thread(target=run_fsm)
        fsm_thread.start()

        # 4. Signal all steps
        all_steps = main_plan_content.split('\n') + sub_plan_content.split('\n')
        # This is a brittle way to signal, a better test would parse the steps.
        # For now, we know the order.
        step_signals = [
            "main set_plan", "main plan_step_complete", "sub set_plan", "sub plan_step_complete",
            "sub create_file", "sub close", "sub submit", "main close", "main submit"
        ]

        for i, signal in enumerate(step_signals):
            time.sleep(1.5)
            # If this is the step that creates the file, we must manually create it
            # to correctly simulate the agent's action.
            if signal == "sub create_file":
                with open(self.output_file, "w") as f:
                    f.write("hello from registry")

            with open(self.step_complete_file, "w") as f:
                f.write(f"Signal for: {signal}")

        # 5. Signal analysis completion
        time.sleep(1.5)
        with open(self.analysis_complete_file, "w") as f:
            f.write("done")

        fsm_thread.join(timeout=30)
        self.assertFalse(fsm_thread.is_alive(), "FSM thread timed out.")

        # 6. Assertions
        final_state = final_state_container["final_state"]
        self.assertIsNone(final_state.error)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r") as f:
            self.assertEqual(f.read(), "hello from registry")


if __name__ == "__main__":
    # Create postmortems dir if it doesn't exist to avoid test failure
    if not os.path.exists("postmortems"):
        os.makedirs("postmortems")
    if not os.path.exists("knowledge_core"):
        os.makedirs("knowledge_core")
    unittest.main()