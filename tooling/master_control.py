import json
import os
import time
import subprocess
from tooling.state import AgentState
from tooling.research_suite.orchestrator import run_research_task

class MasterControlGraph:
    """
    A Finite State Machine (FSM) that enforces a structured development protocol.
    It orchestrates the agent's workflow by transitioning through states defined
    in an FSM definition file and interacting with the agent via the filesystem.
    """
    def __init__(self, fsm_path: str = "tooling/fsm.json"):
        with open(fsm_path, 'r') as f:
            self.fsm = json.load(f)
        self.current_state = self.fsm["initial_state"]

    def get_trigger(self, source_state: str, dest_state: str) -> str:
        """Finds the trigger for a valid transition."""
        for transition in self.fsm["transitions"]:
            if transition["source"] == source_state and transition["dest"] == dest_state:
                return transition["trigger"]
        raise ValueError(f"No trigger found for transition from {source_state} to {dest_state}")

    def get_next_state(self, trigger: str) -> str:
        """Finds the destination state for a given trigger from the current state."""
        for transition in self.fsm["transitions"]:
            if transition["source"] == self.current_state and transition["trigger"] == trigger:
                return transition["dest"]
        raise ValueError(f"No transition found for state {self.current_state} with trigger {trigger}")

    def do_understanding_request(self, agent_state: AgentState) -> str:
        """State for initial request analysis."""
        print("[FSM] State: UNDERSTANDING_REQUEST")
        print(f"  - Task: {agent_state.task}")
        time.sleep(1)
        return "request_understood"

    def do_exploring_codebase(self, agent_state: AgentState) -> str:
        """State for exploring the existing codebase."""
        print("[FSM] State: EXPLORING_CODEBASE")
        print("  - The agent should now use tools like `list_files` and `read_file` to understand the codebase.")
        time.sleep(2)
        return "exploration_complete"

    def do_formulating_plan(self, agent_state: AgentState) -> str:
        """State for creating a step-by-step plan."""
        print("[FSM] State: FORMULATING_PLAN")
        plan_file = "plan.txt"
        print(f"  - Waiting for the agent to create a plan file at '{plan_file}'...")

        while not os.path.exists(plan_file):
            time.sleep(1)

        print(f"  - Detected '{plan_file}'. Reading plan.")
        with open(plan_file, 'r') as f:
            plan = f.read()

        if not plan.strip():
            agent_state.error = "Plan file is empty."
            print("  - Error: Plan is empty.")
            return "error"

        agent_state.plan = plan
        agent_state.messages.append({"role": "system", "content": f"Plan has been set from {plan_file}."})
        print("  - Plan successfully loaded into agent state.")
        os.remove(plan_file)
        print(f"  - Cleaned up '{plan_file}'.")
        return "plan_set"

    def do_implementing_changes(self, agent_state: AgentState) -> str:
        """
        State for executing the plan. It now can dispatch to the research suite.
        """
        print("[FSM] State: IMPLEMENTING_CHANGES")
        plan_steps = [step for step in agent_state.plan.split('\n') if step.strip()]

        if agent_state.current_step_index >= len(plan_steps):
            print("  - All plan steps have been completed.")
            return "implementation_complete"

        step = plan_steps[agent_state.current_step_index]

        # Check if the step requires research
        if "research" in step.lower() or "search for" in step.lower():
            print(f"  - Step requires research: '{step}'")
            # This is a simplified approach to parsing the research task from the step.
            # A more robust solution would use more sophisticated NLP or structured plan steps.
            research_query = step.replace("Research", "").strip()
            constraints = {"task": "search", "query": research_query, "is_test_query": True}

            print(f"  - Dispatching to research suite with constraints: {constraints}")
            research_result_json = run_research_task(constraints)

            agent_state.messages.append({
                "role": "system",
                "content": f"Research for step {agent_state.current_step_index + 1} completed. Result: {research_result_json}"
            })
            print("  - Research complete and results logged.")
        else:
            # If not a research step, wait for the agent to signal completion manually.
            print(f"  - Waiting for agent to manually complete step {agent_state.current_step_index + 1}: {step}")
            step_complete_file = "step_complete.txt"
            while not os.path.exists(step_complete_file):
                time.sleep(1)

            print(f"  - Detected '{step_complete_file}'.")
            with open(step_complete_file, 'r') as f:
                result = f.read()

            agent_state.messages.append({
                "role": "system",
                "content": f"Completed step {agent_state.current_step_index + 1}: {step}\nResult: {result}"
            })
            os.remove(step_complete_file)

        agent_state.current_step_index += 1

        if agent_state.current_step_index < len(plan_steps):
            return "step_succeeded"
        else:
            return "implementation_complete"

    def do_validating_work(self, agent_state: AgentState) -> str:
        """State for running tests and validation checks."""
        print("[FSM] State: VALIDATING_WORK")
        validation_file = "validation_result.txt"
        print(f"  - Waiting for agent to provide validation results in '{validation_file}'...")

        while not os.path.exists(validation_file):
            time.sleep(1)

        with open(validation_file, 'r') as f:
            result = f.read().strip().lower()

        os.remove(validation_file)

        if result == "passed":
            agent_state.validation_passed = True
            print("  - Validation PASSED.")
            return "validation_passed"
        else:
            agent_state.validation_passed = False
            agent_state.messages.append({"role": "system", "content": f"Validation FAILED. Reason: {result}"})
            print(f"  - Validation FAILED. Reason: {result}")
            agent_state.current_step_index = 0
            return "validation_failed"

    def run(self, agent_state: AgentState):
        """Runs the agent's workflow through the FSM."""
        while self.current_state not in self.fsm["final_states"]:
            try:
                if self.current_state == "START":
                    trigger = "task_initiated"
                elif self.current_state == "UNDERSTANDING_REQUEST":
                    trigger = self.do_understanding_request(agent_state)
                elif self.current_state == "EXPLORING_CODEBASE":
                    trigger = self.do_exploring_codebase(agent_state)
                elif self.current_state == "FORMULATING_PLAN":
                    trigger = self.do_formulating_plan(agent_state)
                elif self.current_state == "IMPLEMENTING_CHANGES":
                    trigger = self.do_implementing_changes(agent_state)
                elif self.current_state == "VALIDATING_WORK":
                    trigger = self.do_validating_work(agent_state)
                else:
                    agent_state.error = f"Unknown state: {self.current_state}"
                    trigger = "error"

                next_state = self.get_next_state(trigger)
                print(f"  - Trigger: '{trigger}' -> Transitioning to {next_state}")
                self.current_state = next_state

            except Exception as e:
                agent_state.error = f"FSM Error in state {self.current_state}: {e}"
                self.current_state = "ERROR"

        print(f"\n[FSM] ==> Workflow finished in state: {self.current_state}")
        if agent_state.error:
            print(f"  - Final Status: ERROR")
            print(f"  - Details: {agent_state.error}")
            agent_state.final_summary = f"Task failed with error: {agent_state.error}"
        else:
            print("  - Final Status: SUCCESS")
            agent_state.final_summary = "Task completed successfully."

        return agent_state