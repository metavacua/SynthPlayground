"""
The master orchestrator for the agent's lifecycle, governed by a Finite State Machine.

This script, master_control.py, is the heart of the agent's operational loop.
It implements a strict, protocol-driven workflow defined in a JSON file
(typically `tooling/fsm.json`). The MasterControlGraph class reads this FSM
definition and steps through the prescribed states, ensuring that the agent
cannot deviate from the established protocol.

This version has been refactored to be a library controlled by an external
shell (e.g., `agent_shell.py`), eliminating all file-based polling and making
the interaction purely programmatic.
"""
import json
import sys
import os
import subprocess
import shutil
import datetime
import tempfile

# Add tooling directory to path to import other tools
sys.path.insert(0, "./tooling")
from state import AgentState, PlanContext
from fdc_cli import MAX_RECURSION_DEPTH
from research import execute_research_protocol
from research_planner import plan_deep_research
from plan_parser import parse_plan, Command

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
        """
        Finds a trigger in the FSM definition for a transition from a source
        to a destination state. This is a helper to avoid hardcoding trigger
        strings in the state handlers.
        """
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
            try:
                probe_cmd = ["python3", "tooling/environmental_probe.py"]
                result = subprocess.run(
                    probe_cmd, capture_output=True, text=True, check=True
                )
                agent_state.vm_capability_report = result.stdout
                agent_state.messages.append(
                    {
                        "role": "system",
                        "content": f"L3 Orientation Complete.\n{result.stdout}",
                    }
                )
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                error_message = f"Environmental probe failed: {e}\n{e.stderr if hasattr(e, 'stderr') else ''}"
                agent_state.vm_capability_report = error_message
                agent_state.messages.append(
                    {"role": "system", "content": error_message}
                )

            agent_state.orientation_complete = True
            print("[MasterControl] Orientation Succeeded.")
            return self.get_trigger("ORIENTING", "PLANNING")
        except Exception as e:
            agent_state.error = f"Orientation failed: {e}"
            print(f"[MasterControl] Orientation Failed: {e}")
            return self.get_trigger("ORIENTING", "ERROR")

    def do_planning(self, agent_state: AgentState, plan_content: str) -> str:
        """
        Validates a given plan, parses it, and initializes the plan stack.
        """
        print("[MasterControl] State: PLANNING")

        # To validate, we must use the fdc_cli, which expects a file.
        # We'll write the content to a temporary file.
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt", prefix="plan-") as temp_plan:
            temp_plan_path = temp_plan.name
            temp_plan.write(plan_content)

        print(f"  - Validating plan content written to '{temp_plan_path}'...")
        validation_cmd = ["python3", "tooling/fdc_cli.py", "validate", temp_plan_path]
        result = subprocess.run(validation_cmd, capture_output=True, text=True)

        os.remove(temp_plan_path) # Clean up the temporary file

        if result.returncode != 0:
            error_message = f"Plan validation failed:\n{result.stderr}"
            agent_state.error = error_message
            print(f"[MasterControl] {error_message}")
            return self.get_trigger("PLANNING", "ERROR")

        print("  - Plan validation successful. Parsing plan into commands...")
        parsed_commands = parse_plan(plan_content)

        # The "plan_path" is now a logical concept, we'll use a placeholder.
        agent_state.plan_path = "agent_generated_plan"
        agent_state.plan_stack.append(
            PlanContext(plan_path=agent_state.plan_path, commands=parsed_commands)
        )
        agent_state.messages.append(
            {
                "role": "system",
                "content": "Validated and parsed plan has been loaded. Execution is starting.",
            }
        )
        print("[MasterControl] Planning Complete.")
        return "plan_is_set"


    def do_researching(self, agent_state: AgentState) -> str:
        """
        Generates, validates, and initiates a formal Deep Research FDC.
        """
        print("[MasterControl] State: RESEARCHING")
        topic = agent_state.research_findings.get("topic")
        if not topic:
            agent_state.error = "Cannot initiate research cycle without a topic."
            return self.get_trigger("RESEARCHING", "ERROR")

        # 1. Generate the executable research plan content
        print(f"  - Generating research plan for topic: '{topic}'")
        try:
            research_plan_content = plan_deep_research(topic=topic)
        except Exception as e:
            agent_state.error = f"Failed to generate research plan: {e}"
            return self.get_trigger("RESEARCHING", "ERROR")

        # 2. Validate the plan against the research FSM
        print(f"  - Validating research plan content...")
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt", prefix="research-plan-") as temp_plan:
            temp_plan_path = temp_plan.name
            temp_plan.write(research_plan_content)

        validation_cmd = ["python3", "tooling/fdc_cli.py", "validate", temp_plan_path]
        result = subprocess.run(validation_cmd, capture_output=True, text=True)
        os.remove(temp_plan_path)

        if result.returncode != 0:
            error_message = f"Research plan validation failed:\n{result.stderr}"
            agent_state.error = error_message
            return self.get_trigger("RESEARCHING", "ERROR")

        # 3. Push the validated research plan onto the execution stack
        print("  - Research plan is valid. Pushing to execution stack.")
        parsed_commands = parse_plan(research_plan_content)
        agent_state.plan_stack.append(
            PlanContext(plan_path="research_plan.txt", commands=parsed_commands)
        )
        agent_state.messages.append(
            {
                "role": "system",
                "content": f"L4 Deep Research Cycle initiated for topic: '{topic}'.",
            }
        )
        return self.get_trigger("RESEARCHING", "EXECUTING")

    def _handle_call_plan(self, agent_state: AgentState, args: list) -> str:
        """Handles the 'call_plan' directive during execution."""
        if len(agent_state.plan_stack) > MAX_RECURSION_DEPTH:
            agent_state.error = (
                f"Maximum recursion depth ({MAX_RECURSION_DEPTH}) exceeded."
            )
            print(f"[MasterControl] Error: {agent_state.error}")
            return self.get_trigger("EXECUTING", "ERROR")

        plan_name_or_path = args[0]
        registry = _load_plan_registry()
        sub_plan_path = registry.get(plan_name_or_path, plan_name_or_path)

        print(
            f"  - Calling sub-plan: {sub_plan_path} (resolved from '{plan_name_or_path}')"
        )
        try:
            with open(sub_plan_path, "r") as f:
                raw_sub_plan_content = f.read()
            parsed_sub_commands = parse_plan(raw_sub_plan_content)
        except FileNotFoundError:
            agent_state.error = f"Sub-plan file not found: {sub_plan_path}"
            print(f"[MasterControl] Error: {agent_state.error}")
            return self.get_trigger("EXECUTING", "ERROR")

        # Advance the current plan's step *before* pushing the new one
        current_context = agent_state.plan_stack[-1]
        current_context.current_step += 1

        # Push the new plan onto the stack
        new_context = PlanContext(
            plan_path=sub_plan_path, commands=parsed_sub_commands
        )
        agent_state.plan_stack.append(new_context)
        return self.get_trigger("EXECUTING", "EXECUTING")

    def get_current_step(self, agent_state: AgentState) -> Command | None:
        """
        Returns the current command to be executed by the agent, or None if execution is complete.
        """
        if not agent_state.plan_stack:
            return None

        current_context = agent_state.plan_stack[-1]
        if current_context.current_step >= len(current_context.commands):
            return None # This plan is done, shell should call do_execution to pop it.

        return current_context.commands[current_context.current_step]

    def do_execution(self, agent_state: AgentState, step_result: str | None) -> str:
        """
        Processes the result of a step and advances the execution state.
        """
        print("[MasterControl] State: EXECUTING")

        if not agent_state.plan_stack:
            print("[MasterControl] Execution Complete (plan stack is empty).")
            return self.get_trigger("EXECUTING", "FINALIZING")

        # Always work with the plan at the top of the stack
        current_context = agent_state.plan_stack[-1]

        # If we've finished all steps in the current plan, pop it and continue
        if current_context.current_step >= len(current_context.commands):
            agent_state.plan_stack.pop()
            if not agent_state.plan_stack:
                 print("  - Finished final plan. Moving to FINALIZING.")
                 return self.get_trigger("EXECUTING", "FINALIZING")
            else:
                print(f"  - Finished sub-plan '{current_context.plan_path}'. Resuming parent.")
                # Return a trigger that keeps us in the EXECUTING state for the next loop
                return self.get_trigger("EXECUTING", "EXECUTING")

        command_obj = current_context.commands[current_context.current_step]
        tool_name = command_obj.tool_name
        args_text = command_obj.args_text

        # Handle special directives that are executed by the FSM itself
        if tool_name == "call_plan":
            return self._handle_call_plan(agent_state, args_text.strip().split())

        # Enforce protocol for destructive commands.
        if tool_name == "reset_all":
            error_message = "The 'reset_all' tool is deprecated and strictly forbidden. Its use is a critical protocol violation."
            agent_state.error = error_message
            print(f"[MasterControl] FATAL: {error_message}")
            return "execution_failed"

        # The agent shell has executed the command and provided the result.
        # Now we just log it and advance the step.
        step_representation = (
            f"{tool_name} {args_text[:50]}..." if args_text else tool_name
        )

        agent_state.messages.append(
            {
                "role": "system",
                "content": f"Completed step {current_context.current_step + 1} in '{current_context.plan_path}': {step_representation}\nResult: {step_result}",
            }
        )

        current_context.current_step += 1

        print(
            f"  - Step {current_context.current_step} of {len(current_context.commands)} in '{current_context.plan_path}' signaled complete."
        )
        # Stay in the EXECUTING state for the next loop
        return self.get_trigger("EXECUTING", "EXECUTING")

    def do_finalizing(self, agent_state: AgentState, analysis_content: str) -> str:
        """
        Handles the finalization of the task with agent-provided analysis.
        """
        print("[MasterControl] State: FINALIZING")
        try:
            # 1. Use the agent's analysis to create the post-mortem report
            task_id = agent_state.task
            draft_path = f"DRAFT-{task_id}.md"
            agent_state.draft_postmortem_path = draft_path

            # Create the report content
            report_header = f"# Post-Mortem Report for Task: {task_id}\n\n"
            report_body = f"## Agent Analysis\n\n{analysis_content}\n"
            with open(draft_path, "w") as f:
                f.write(report_header + report_body)
            print(f"  - Created draft post-mortem from agent analysis at '{draft_path}'.")

            # 2. Finalize the post-mortem and compile lessons
            safe_task_id = "".join(c for c in task_id if c.isalnum() or c in ("-", "_"))
            final_path = f"postmortems/{datetime.date.today()}-{safe_task_id}.md"
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            os.rename(draft_path, final_path)
            report_message = f"Post-mortem analysis finalized. Report saved to '{final_path}'."
            agent_state.final_report = report_message
            agent_state.messages.append({"role": "system", "content": report_message})
            print(f"  - {report_message}")

            compile_cmd = ["python3", "tooling/knowledge_compiler.py", final_path]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode != 0:
                compile_msg = f"Knowledge compilation failed: {compile_result.stderr}"
                agent_state.error = compile_msg
                print(f"  - {agent_state.error}")
                return self.get_trigger("FINALIZING", "finalization_failed")
            agent_state.messages.append({"role": "system", "content": "Knowledge compilation successful."})
            print("  - Knowledge compilation successful.")

            # 3. Run self-correction
            print("  - Running self-correction cycle...")
            correction_cmd = ["python3", "tooling/self_correction_orchestrator.py"]
            correction_result = subprocess.run(correction_cmd, capture_output=True, text=True)
            agent_state.messages.append({"role": "system", "content": f"Self-Correction Output:\n{correction_result.stdout}"})
            if correction_result.returncode != 0:
                error_message = f"Self-correction cycle FAILED:\n{correction_result.stderr}"
                agent_state.error = error_message
                print(f"  - {error_message}")
                return self.get_trigger("FINALIZING", "finalization_failed")
            print("  - Self-correction cycle completed successfully.")

            print("[MasterControl] Finalization Complete.")
            return self.get_trigger("FINALIZING", "AWAITING_SUBMISSION")
        except Exception as e:
            agent_state.error = f"An unexpected error occurred during finalization: {e}"
            print(f"[MasterControl] {agent_state.error}")
            return self.get_trigger("FINALIZING", "finalization_failed")