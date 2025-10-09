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
from state import AgentState

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
        """Waits for and validates a plan, then returns a trigger."""
        print("[MasterControl] State: PLANNING")
        plan_file = "plan.txt"
        print(f"  - Waiting for agent to create '{plan_file}'...")
        while not os.path.exists(plan_file):
            time.sleep(0.1)

        print(f"  - Detected '{plan_file}'. Reading and validating plan...")
        with open(plan_file, "r") as f:
            agent_state.plan = f.read()

        if not agent_state.plan:
            agent_state.error = "Planning failed: plan.txt was empty."
            print(f"[MasterControl] {agent_state.error}")
            os.remove(plan_file)
            return "planning_failed"

        print("[MasterControl] Planning Complete.")
        os.remove(plan_file)
        return "plan_is_set"

    def do_execution(self, agent_state: AgentState) -> str:
        """Executes one plan step and returns a trigger."""
        print(f"[MasterControl] State: EXECUTING (Step {agent_state.current_step_index})")
        plan_steps = [step for step in agent_state.plan.split("\n") if step.strip()]

        if agent_state.current_step_index >= len(plan_steps):
            print("[MasterControl] Execution phase complete.")
            return "all_steps_completed"

        step = plan_steps[agent_state.current_step_index]
        print(f"  - Executing step {agent_state.current_step_index + 1}/{len(plan_steps)}: {step}")

        try:
            parts = shlex.split(step)
            tool_name = parts[0]
            args_list = parts[1:]

            wrapper_cmd = [
                "python3", "tooling/execution_wrapper.py",
                "--tool", tool_name,
                "--args", json.dumps(args_list),
                "--task-id", agent_state.task,
                "--plan-step", str(agent_state.current_step_index),
            ]
            result = subprocess.run(wrapper_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                agent_state.error = f"Execution wrapper failed for step: {step}\nStderr: {result.stderr}"
                print(f"[MasterControl] {agent_state.error}")
                return "execution_failed"

            agent_state.current_step_index += 1
            return "step_succeeded"
        except Exception as e:
            agent_state.error = f"Orchestrator failed to execute step: {step}\nError: {e}\n{traceback.format_exc()}"
            print(f"[MasterControl] {agent_state.error}")
            return "execution_failed"

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