import json
import sys
import time
import os
import subprocess
import shutil
import datetime
import shlex
import traceback

# Add tooling directory to path to import other tools
sys.path.insert(0, "./tooling")
from state import AgentState, PlanContext
from fdc_cli import MAX_RECURSION_DEPTH
from research import execute_research_protocol

# The research module is not yet implemented, so we will stub it.
def execute_research_protocol(constraints):
    """Stub function for the research protocol."""
    print(f"  - (Stub) Executing research protocol with constraints: {constraints}")
    return f"Stubbed research result for {constraints.get('path', 'N/A')}"

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

    def do_orientation(self, agent_state: AgentState) -> str:
        """Executes orientation steps and returns a trigger."""
        print("[MasterControl] State: ORIENTING")
        try:
            print("  - Executing Protocol Self-Awareness Check...")
            subprocess.run(["make", "AGENTS.md"], check=True, capture_output=True, text=True)
            print("  - AGENTS.md is up-to-date.")
            agent_state.orientation_complete = True
            print("[MasterControl] Orientation Succeeded.")
            return "orientation_succeeded"
        except Exception as e:
            agent_state.error = f"Orientation failed: {e}\n{traceback.format_exc()}"
            print(f"[MasterControl] Orientation Failed: {agent_state.error}")
            return "orientation_failed"

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

            sub_plan_path = args[0]
            print(f"  - Calling sub-plan: {sub_plan_path}")
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
        """Creates a draft post-mortem and waits for analysis."""
        print("[MasterControl] State: AWAITING_ANALYSIS")
        draft_path = f"DRAFT-{agent_state.task}.md"
        agent_state.draft_postmortem_path = draft_path

        try:
            template_path = "postmortem.md"
            if os.path.exists(template_path):
                 shutil.copyfile(template_path, draft_path)
            else:
                with open(draft_path, "w") as f: f.write("# Post-Mortem\n")
            print(f"  - Created draft post-mortem at '{draft_path}'.")
        except Exception as e:
            agent_state.error = f"Failed to create draft post-mortem: {e}"
            return "post_mortem_failed"

        analysis_complete_file = "analysis_complete.txt"
        print(f"  - Waiting for agent to complete analysis and create '{analysis_complete_file}'...")
        while not os.path.exists(analysis_complete_file):
            time.sleep(0.1)

        os.remove(analysis_complete_file)
        print("  - Analysis complete.")
        return "analysis_complete"

    def do_post_mortem(self, agent_state: AgentState) -> str:
        """Finalizes the post-mortem and returns a trigger."""
        print("[MasterControl] State: POST_MORTEM")
        draft_path = agent_state.draft_postmortem_path
        if not draft_path or not os.path.exists(draft_path):
            agent_state.error = f"Draft post-mortem file '{draft_path}' not found."
            return "post_mortem_failed"

        safe_task_id = "".join(c for c in agent_state.task if c.isalnum() or c in ("-", "_"))
        os.makedirs("postmortems", exist_ok=True)
        final_path = f"postmortems/{datetime.date.today()}-{safe_task_id}.md"

        try:
            os.rename(draft_path, final_path)
            agent_state.final_report = f"Post-mortem analysis finalized. Report saved to '{final_path}'."
            print(f"  - {agent_state.final_report}")

            # Step 1: Compile lessons learned from the report
            print(f"  - Compiling lessons from '{final_path}'...")
            compile_cmd = ["python3", "tooling/knowledge_compiler.py", final_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode == 0:
                print("  - Knowledge compilation successful.")
            else:
                print(f"  - Warning: Knowledge compilation failed: {compile_result.stderr}")

            # Step 2: Run automated self-improvement analysis
            analysis_cmd = ["python3", "tooling/self_improvement_cli.py"]
            analysis_result = subprocess.run(analysis_cmd, capture_output=True, text=True)
            analysis_output = f"\n\n---\n## Automated Performance Analysis\n```\n{analysis_result.stdout.strip()}\n```"
            with open(final_path, "a") as f: f.write(analysis_output)
            print("  - Automated performance analysis complete.")
            return "post_mortem_complete"
        except Exception as e:
            agent_state.error = f"Failed to finalize post-mortem report: {e}\n{traceback.format_exc()}"
            return "post_mortem_failed"

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
        state_handler_map = {
            "ORIENTING": self.do_orientation,
            "PLANNING": self.do_planning,
            "EXECUTING": self.do_execution,
            "AWAITING_ANALYSIS": self.do_awaiting_analysis,
            "POST_MORTEM": self.do_post_mortem,
        }

        while self.current_state not in self.fsm["final_states"]:
            if self.current_state == "START":
                self.current_state = "ORIENTING"
                continue

            handler = state_handler_map.get(self.current_state)
            if not handler:
                agent_state.error = f"FATAL: Unknown or unimplemented state handler for '{self.current_state}'"
                self.current_state = "ERROR"
                break

            trigger = handler(agent_state)

            found_transition = False
            for transition in self.fsm["transitions"]:
                if transition["source"] == self.current_state and transition["trigger"] == trigger:
                    self.current_state = transition["dest"]
                    found_transition = True
                    break

            if not found_transition:
                agent_state.error = f"FATAL: No valid FSM transition found for state '{self.current_state}' with trigger '{trigger}'"
                self.current_state = "ERROR"

        print(f"[MasterControl] Workflow finished in state: {self.current_state}")
        if agent_state.error:
            print(f"  - Final Error: {agent_state.error}")
        return agent_state

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Demonstrate the self-enforcing protocol."
    print(f"--- Initializing Master Control Graph: {task} ---")
    initial_state = AgentState(task=task)
    graph = MasterControlGraph()
    final_state = graph.run(initial_state)
    print("\n--- Final State ---")
    print(final_state.to_json(indent=2))
    print("--- Demonstration Complete ---")
    if final_state.error:
        sys.exit(1)