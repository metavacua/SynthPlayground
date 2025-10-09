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
from research import execute_research_protocol


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
        Waits for the agent to provide a plan, validates it, and transitions.

        This node polls for `plan.txt`, validates it using `fdc_cli.py`,
        and on success, loads the plan into the state and transitions.
        On failure, it enters an error state.
        """
        print("[MasterControl] State: PLANNING")
        plan_file = "plan.txt"

        # Wait for the agent to create the plan file
        print(f"  - Waiting for agent to create '{plan_file}'...")
        while not os.path.exists(plan_file):
            time.sleep(1)  # Poll every second

        print(f"  - Detected '{plan_file}'. Reading and validating plan...")

        # Validate the plan using the fdc_cli.py tool
        validation_cmd = ["python3", "tooling/fdc_cli.py", "validate", plan_file]
        result = subprocess.run(validation_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            error_message = f"Plan validation failed:\n{result.stderr}"
            agent_state.error = error_message
            print(f"[MasterControl] {error_message}")
            # Note: We don't delete the plan file on failure so it can be inspected.
            return self.get_trigger("PLANNING", "ERROR")

        print("  - Plan validation successful.")
        with open(plan_file, "r") as f:
            plan = f.read()

        agent_state.plan = plan
        agent_state.messages.append(
            {
                "role": "system",
                "content": f"Validated plan has been set from {plan_file}.",
            }
        )
        print("[MasterControl] Planning Complete.")

        # Clean up the plan file after successful validation
        os.remove(plan_file)
        print(f"  - Cleaned up '{plan_file}'.")

        return self.get_trigger("PLANNING", "EXECUTING")

    def do_execution(self, agent_state: AgentState) -> str:
        """
        Executes the plan step-by-step by calling the execution_wrapper.

        This node is the active executor. It parses each step of the plan
        and invokes the `execution_wrapper.py` script to perform the action
        and handle logging. This ensures that every action is centrally
        managed and robustly logged.
        """
        print("[MasterControl] State: EXECUTING")
        plan_steps = [step for step in agent_state.plan.split("\n") if step.strip()]

        if agent_state.current_step_index < len(plan_steps):
            step = plan_steps[agent_state.current_step_index]
            print(f"  - Executing step {agent_state.current_step_index + 1}/{len(plan_steps)}: {step}")

            try:
                # Use shlex to safely parse the command-line string
                parts = shlex.split(step)
                tool_name = parts[0]
                args_list = parts[1:]

                # Prepare the command to call the execution wrapper
                wrapper_cmd = [
                    "python3",
                    "tooling/execution_wrapper.py",
                    "--tool",
                    tool_name,
                    "--args",
                    json.dumps(args_list),
                    "--task-id",
                    agent_state.task,
                    "--plan-step",
                    str(agent_state.current_step_index),
                ]

                # Execute the command
                result = subprocess.run(
                    wrapper_cmd, capture_output=True, text=True
                )

                # If the wrapper script itself fails, it's a critical error
                if result.returncode != 0:
                    error_message = f"Execution wrapper failed for step: {step}\nStderr: {result.stderr}"
                    agent_state.error = error_message
                    print(f"[MasterControl] {error_message}")
                    return self.get_trigger("EXECUTING", "ERROR")

                # The wrapper's stdout might contain JSON results from tools like read_file
                agent_state.messages.append(
                    {
                        "role": "system",
                        "content": f"Successfully executed step {agent_state.current_step_index + 1}: {step}\nResult: {result.stdout}",
                    }
                )

                agent_state.current_step_index += 1
                return self.get_trigger("EXECUTING", "EXECUTING")

            except Exception as e:
                error_message = f"Orchestrator failed to execute step: {step}\nError: {e}\n{traceback.format_exc()}"
                agent_state.error = error_message
                print(f"[MasterControl] {error_message}")
                return self.get_trigger("EXECUTING", "ERROR")
        else:
            print("[MasterControl] Execution Complete.")
            return self.get_trigger("EXECUTING", "AWAITING_ANALYSIS")

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
        Finalizes the post-mortem process, compiles lessons, and runs automated analysis.
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
            # Finalize the report by renaming the draft
            os.rename(draft_path, final_path)
            report_message = (
                f"Post-mortem analysis finalized. Report saved to '{final_path}'."
            )
            agent_state.final_report = report_message
            agent_state.messages.append({"role": "system", "content": report_message})
            print(f"[MasterControl] {report_message}")

            # Step 1: Compile lessons learned from the report
            print(f"  - Compiling lessons from '{final_path}'...")
            compile_cmd = ["python3", "tooling/knowledge_compiler.py", final_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode == 0:
                agent_state.messages.append({"role": "system", "content": "Knowledge compilation successful."})
            else:
                agent_state.messages.append({"role": "system", "content": f"Knowledge compilation failed: {compile_result.stderr}"})

            # Step 2: Run automated self-improvement analysis
            print(f"  - Running self-improvement analysis on activity log...")
            analysis_cmd = ["python3", "tooling/self_improvement_cli.py"]
            analysis_result = subprocess.run(analysis_cmd, capture_output=True, text=True)

            # Append analysis to the post-mortem report
            analysis_output = f"""
---
## 4. Automated Performance Analysis
This section is automatically generated by the `self_improvement_cli.py` tool.

```
{analysis_result.stdout.strip()}
```
"""
            with open(final_path, "a") as f:
                f.write(analysis_output)

            analysis_msg = "Automated performance analysis complete and appended to report."
            print(f"  - {analysis_msg}")
            agent_state.messages.append({"role": "system", "content": analysis_msg})

        except Exception as e:
            agent_state.error = f"Failed to finalize post-mortem report: {e}\n{traceback.format_exc()}"
            print(f"[MasterControl] {agent_state.error}")
            return self.get_trigger("POST_MORTEM", "ERROR")

        print("[MasterControl] Post-Mortem Complete.")
        return self.get_trigger("POST_MORTEM", "AWAITING_SUBMISSION")

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
