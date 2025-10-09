import json
import sys
import time
import os
import subprocess
import shutil
import datetime

# Add tooling directory to path to import other tools
sys.path.insert(0, "./tooling")
from state import AgentState, PlanContext
from fdc_cli import MAX_RECURSION_DEPTH
from research import execute_research_protocol

PLAN_REGISTRY_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "knowledge_core", "plan_registry.json")
)


def _load_plan_registry():
    """Loads the plan registry, returning an empty dict if it doesn't exist or is invalid."""
    if not os.path.exists(PLAN_REGISTRY_PATH):
        return {}
    try:
        with open(PLAN_REGISTRY_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


class MasterControlGraph:
    """
    A Finite State Machine (FSM) that enforces the agent's protocol.
    This graph reads a state definition and orchestrates the agent's workflow,
    ensuring that all protocol steps are followed in the correct order.
    """

    def __init__(self, fsm_path: str = "tooling/fsm.json"):
        with open(fsm_path, "r") as f:
            self.fsm = json.load(f)
        self.current_state = self.fsm["initial_state"]

    def get_trigger(self, source_state: str, dest_state: str) -> str:
        """Finds the trigger for a transition between two states."""
        for transition in self.fsm["transitions"]:
            if (
                transition["source"] == source_state
                and transition["dest"] == dest_state
            ):
                return transition["trigger"]
        raise ValueError(
            f"No trigger found for transition from {source_state} to {dest_state}"
        )

    def do_orientation(self, agent_state: AgentState) -> str:
        """Executes the L1, L2, and L3 orientation steps."""
        print("[MasterControl] State: ORIENTING")
        try:
            # L1: Self-Awareness
            print("  - Executing L1: Self-Awareness...")
            l1_constraints = {
                "target": "local_filesystem",
                "scope": "file",
                "path": "knowledge_core/agent_meta.json",
            }
            agent_meta = execute_research_protocol(l1_constraints)
            agent_state.messages.append(
                {
                    "role": "system",
                    "content": f"L1 Orientation Complete. Agent Meta: {agent_meta[:100]}...",
                }
            )

            # L2: Repo Sync
            print("  - Executing L2: Repository Sync...")
            l2_constraints = {
                "target": "local_filesystem",
                "scope": "directory",
                "path": "knowledge_core/",
            }
            repo_state = execute_research_protocol(l2_constraints)
            agent_state.messages.append(
                {
                    "role": "system",
                    "content": f"L2 Orientation Complete. Repo State: {repo_state[:100]}...",
                }
            )

            # L3: Environmental Probe
            print("  - Executing L3: Environmental Probe...")
            # This would call the environmental_probe.py script in a real scenario
            agent_state.vm_capability_report = (
                "Mock VM Capability Report: Filesystem OK, Network OK."
            )
            agent_state.messages.append(
                {"role": "system", "content": "L3 Orientation Complete."}
            )

            agent_state.orientation_complete = True
            print("[MasterControl] Orientation Succeeded.")
            return self.get_trigger("ORIENTING", "PLANNING")
        except Exception as e:
            agent_state.error = f"Orientation failed: {e}"
            print(f"[MasterControl] Orientation Failed: {e}")
            return self.get_trigger("ORIENTING", "ERROR")

    def do_planning(self, agent_state: AgentState) -> str:
        """
        Waits for the agent to provide a plan, validates it, and initializes
        the plan stack for execution.
        """
        print("[MasterControl] State: PLANNING")
        plan_file = "plan.txt"

        print(f"  - Waiting for agent to create '{plan_file}'...")
        while not os.path.exists(plan_file):
            time.sleep(1)

        print(f"  - Detected '{plan_file}'. Reading and validating plan...")
        validation_cmd = ["python3", "tooling/fdc_cli.py", "validate", plan_file]
        result = subprocess.run(validation_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            error_message = f"Plan validation failed:\n{result.stderr}"
            agent_state.error = error_message
            print(f"[MasterControl] {error_message}")
            return self.get_trigger("PLANNING", "ERROR")

        print("  - Plan validation successful.")
        with open(plan_file, "r") as f:
            plan_content = [line for line in f.read().split("\n") if line.strip()]

        # Initialize the plan stack with the root plan
        agent_state.plan_stack.append(
            PlanContext(plan_path=plan_file, plan_content=plan_content)
        )
        agent_state.messages.append(
            {
                "role": "system",
                "content": f"Validated plan from {plan_file} has been loaded and execution is starting.",
            }
        )
        print("[MasterControl] Planning Complete.")
        # We keep plan.txt for now for traceability during execution
        return self.get_trigger("PLANNING", "EXECUTING")

    def do_execution(self, agent_state: AgentState) -> str:
        """
        Executes the plan using a stack-based approach to handle sub-plans (CFDC).
        """
        print("[MasterControl] State: EXECUTING")

        if not agent_state.plan_stack:
            print("[MasterControl] Execution Complete (plan stack is empty).")
            # Clean up the root plan file now that execution is fully complete
            if os.path.exists("plan.txt"):
                os.remove("plan.txt")
            return self.get_trigger("EXECUTING", "AWAITING_ANALYSIS")

        # Always work with the plan at the top of the stack
        current_context = agent_state.plan_stack[-1]
        plan_steps = current_context.plan_content

        # If we've finished all steps in the current plan, pop it and continue
        if current_context.current_step >= len(plan_steps):
            agent_state.plan_stack.pop()
            print(
                f"  - Finished sub-plan '{current_context.plan_path}'. Resuming parent."
            )
            # Re-enter the execution loop immediately to process the parent plan
            return self.get_trigger("EXECUTING", "EXECUTING")

        step = plan_steps[current_context.current_step].strip()
        command, *args = step.split()

        # Handle the new 'call_plan' directive
        if command == "call_plan":
            if len(agent_state.plan_stack) > MAX_RECURSION_DEPTH:
                agent_state.error = f"Maximum recursion depth ({MAX_RECURSION_DEPTH}) exceeded."
                print(f"[MasterControl] Error: {agent_state.error}")
                return self.get_trigger("EXECUTING", "ERROR")

            plan_name_or_path = args[0]
            registry = _load_plan_registry()
            sub_plan_path = registry.get(plan_name_or_path, plan_name_or_path)

            print(f"  - Calling sub-plan: {sub_plan_path} (resolved from '{plan_name_or_path}')")
            try:
                with open(sub_plan_path, "r") as f:
                    sub_plan_content = [
                        line for line in f.read().split("\n") if line.strip()
                    ]
            except FileNotFoundError:
                agent_state.error = f"Sub-plan file not found: {sub_plan_path}"
                print(f"[MasterControl] Error: {agent_state.error}")
                return self.get_trigger("EXECUTING", "ERROR")

            # Advance the current plan's step *before* pushing the new one
            current_context.current_step += 1

            # Push the new plan onto the stack
            new_context = PlanContext(
                plan_path=sub_plan_path, plan_content=sub_plan_content
            )
            agent_state.plan_stack.append(new_context)
            return self.get_trigger("EXECUTING", "EXECUTING")

        # --- Standard Step Execution ---
        step_complete_file = "step_complete.txt"
        print(f"  - Waiting for agent to complete step: {step}")
        while not os.path.exists(step_complete_file):
            time.sleep(1)

        print(f"  - Detected '{step_complete_file}'.")
        with open(step_complete_file, "r") as f:
            result = f.read()

        agent_state.messages.append(
            {
                "role": "system",
                "content": f"Completed step {current_context.current_step + 1} in '{current_context.plan_path}': {step}\nResult: {result}",
            }
        )

        os.remove(step_complete_file)
        current_context.current_step += 1

        print(
            f"  - Step {current_context.current_step} of {len(plan_steps)} in '{current_context.plan_path}' signaled complete."
        )
        return self.get_trigger("EXECUTING", "EXECUTING")

    def do_awaiting_analysis(self, agent_state: AgentState) -> str:
        """
        Creates a draft post-mortem and waits for the agent to analyze it.
        """
        print("[MasterControl] State: AWAITING_ANALYSIS")
        task_id = agent_state.task
        draft_path = f"DRAFT-{task_id}.md"
        agent_state.draft_postmortem_path = draft_path

        # Create the draft file from the template
        try:
            shutil.copyfile("postmortem.md", draft_path)
            print(f"  - Created draft post-mortem at '{draft_path}'.")
        except Exception as e:
            agent_state.error = f"Failed to create draft post-mortem: {e}"
            print(f"[MasterControl] {agent_state.error}")
            return self.get_trigger("EXECUTING", "ERROR")  # Or a new trigger if needed

        # Wait for the agent to signal analysis is complete
        analysis_complete_file = "analysis_complete.txt"
        print(
            f"  - Waiting for agent to complete analysis and create '{analysis_complete_file}'..."
        )
        while not os.path.exists(analysis_complete_file):
            time.sleep(1)

        os.remove(analysis_complete_file)
        print(
            f"  - Detected and cleaned up '{analysis_complete_file}'. Analysis complete."
        )
        return self.get_trigger("AWAITING_ANALYSIS", "POST_MORTEM")

    def do_post_mortem(self, agent_state: AgentState) -> str:
        """
        Finalizes the post-mortem process by renaming the draft file.
        """
        print("[MasterControl] State: POST_MORTEM")
        draft_path = agent_state.draft_postmortem_path
        if not draft_path or not os.path.exists(draft_path):
            agent_state.error = f"Draft post-mortem file '{draft_path}' not found."
            print(f"[MasterControl] {agent_state.error}")
            return self.get_trigger("POST_MORTEM", "ERROR")

        # Create a safe, timestamped final path
        task_id = agent_state.task
        safe_task_id = "".join(c for c in task_id if c.isalnum() or c in ("-", "_"))
        final_path = f"postmortems/{datetime.date.today()}-{safe_task_id}.md"

        try:
            os.rename(draft_path, final_path)
            report_message = (
                f"Post-mortem analysis finalized. Report saved to '{final_path}'."
            )
            agent_state.final_report = report_message
            agent_state.messages.append({"role": "system", "content": report_message})
            print(f"[MasterControl] {report_message}")

            # Automatically compile lessons learned from the new post-mortem
            print(f"  - Compiling lessons from '{final_path}'...")
            compile_cmd = ["python3", "tooling/knowledge_compiler.py", final_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode == 0:
                compile_msg = "Knowledge compilation successful."
                print(f"  - {compile_msg}")
                agent_state.messages.append({"role": "system", "content": compile_msg})
            else:
                compile_msg = f"Knowledge compilation failed: {compile_result.stderr}"
                print(f"  - {compile_msg}")
                agent_state.messages.append({"role": "system", "content": compile_msg})
                # For now, this is not a critical FSM failure.

        except Exception as e:
            agent_state.error = f"Failed to finalize post-mortem report: {e}"
            print(f"[MasterControl] {agent_state.error}")
            return self.get_trigger("POST_MORTEM", "ERROR")

        print("[MasterControl] Post-Mortem Complete.")
        return self.get_trigger("POST_MORTEM", "AWAITING_SUBMISSION")

    def get_trigger(self, source_state: str, dest_state: str) -> str:
        """
        Finds a trigger in the FSM definition for a transition from a source
        to a destination state. This is a helper to avoid hardcoding trigger
        strings in the state handlers.
        """
        for transition in self.fsm["transitions"]:
            if transition["source"] == source_state and transition["dest"] == dest_state:
                # Return the first trigger found that matches the transition.
                return transition["trigger"]
        # This case indicates a logic error or an incomplete FSM definition.
        raise RuntimeError(
            f"No trigger defined in FSM for transition from '{source_state}' to '{dest_state}'"
        )

    def run(self, initial_agent_state: AgentState):
        """Runs the agent's workflow through the FSM."""
        agent_state = initial_agent_state

        while self.current_state not in self.fsm["final_states"]:
            if self.current_state == "START":
                self.current_state = "ORIENTING"
                continue

            if self.current_state == "ORIENTING":
                trigger = self.do_orientation(agent_state)
            elif self.current_state == "PLANNING":
                trigger = self.do_planning(agent_state)
            elif self.current_state == "EXECUTING":
                trigger = self.do_execution(agent_state)
            elif self.current_state == "AWAITING_ANALYSIS":
                trigger = self.do_awaiting_analysis(agent_state)
            elif self.current_state == "POST_MORTEM":
                trigger = self.do_post_mortem(agent_state)
            else:
                agent_state.error = f"Unknown state: {self.current_state}"
                self.current_state = "ERROR"
                break

            # Find the next state based on the trigger
            found_transition = False
            for transition in self.fsm["transitions"]:
                if (
                    transition["source"] == self.current_state
                    and transition["trigger"] == trigger
                ):
                    self.current_state = transition["dest"]
                    found_transition = True
                    break

            if not found_transition:
                agent_state.error = f"No transition found for state {self.current_state} with trigger {trigger}"
                self.current_state = "ERROR"

        print(f"[MasterControl] Workflow finished in state: {self.current_state}")
        if agent_state.error:
            print(f"  - Error: {agent_state.error}")
        return agent_state


if __name__ == "__main__":
    print("--- Initializing Master Control Graph Demonstration ---")
    # 1. Initialize the agent's state for a new task
    task = "Demonstrate the self-enforcing protocol."
    initial_state = AgentState(task=task)

    # 2. Initialize and run the master control graph
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)

    # 3. Print the final report
    print("\n--- Final State ---")
    print(json.dumps(final_state.to_json(), indent=2))
    print("--- Demonstration Complete ---")
