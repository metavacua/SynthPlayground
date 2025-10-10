"""
The master orchestrator for the agent's lifecycle, governed by a Finite State Machine.

This script, `master_control.py`, is the heart of the agent's operational loop.
It implements a strict, protocol-driven workflow defined in a JSON file
(typically `tooling/fsm.json`). The `MasterControlGraph` class reads this FSM
definition and steps through the prescribed states, ensuring that the agent
cannot deviate from the established protocol.

The key responsibilities of this orchestrator include:
- **State Enforcement:** Guiding the agent through the formal states of a task:
  ORIENTING, PLANNING, EXECUTING, AWAITING_ANALYSIS, POST_MORTEM, and finally
  AWAITING_SUBMISSION.
- **Plan Validation:** Before execution, it invokes the `fdc_cli.py` tool to
  formally validate the agent-generated `plan.txt`, preventing the execution of
  invalid or unsafe plans.
- **Hierarchical Execution (CFDC):** It manages the plan execution stack, which
  is the core mechanism of the Context-Free Development Cycle (CFDC). This
  allows plans to call other plans as sub-routines via the `call_plan`
  directive.
- **Recursion Safety:** It enforces a `MAX_RECURSION_DEPTH` on the plan stack to
  guarantee that the execution process is always decidable and will terminate.
- **Lifecycle Management:** It orchestrates the entire lifecycle, from initial
  orientation and environmental probing to the final post-mortem analysis and
  compilation of lessons learned.

The FSM operates by waiting for specific signals—typically the presence of
files like `plan.txt` or `step_complete.txt`—before transitioning to the next
state. This creates a robust, interactive loop where the orchestrator directs
the high-level state, and the agent is responsible for completing the work
required to advance that state.
"""
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

    def do_planning(self, agent_state: AgentState) -> str:
        """
        Waits for the agent to provide a plan, validates it, parses it into
        commands, and initializes the plan stack for execution.
        """
        print("[MasterControl] State: PLANNING")

        # L4 Check: Does the agent need to perform deep research?
        research_request_file = "request_deep_research.txt"
        if os.path.exists(research_request_file):
            print("  - Detected request for L4 Deep Research Cycle.")
            with open(research_request_file, "r") as f:
                topic = f.read().strip()
            agent_state.research_findings["topic"] = topic
            os.remove(research_request_file)
            # Transition to the new RESEARCHING state
            return self.get_trigger("PLANNING", "RESEARCHING")

        # Standard L3 planning process
        plan_file = "plan.txt"
        agent_state.plan_path = plan_file # Set the root plan path
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

        print("  - Plan validation successful. Parsing plan into commands...")
        with open(plan_file, "r") as f:
            raw_plan_content = f.read()

        parsed_commands = parse_plan(raw_plan_content)

        agent_state.plan_stack.append(
            PlanContext(plan_path=plan_file, commands=parsed_commands)
        )
        agent_state.messages.append(
            {
                "role": "system",
                "content": f"Validated and parsed plan from {plan_file} has been loaded. Execution is starting.",
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

        # 1. Generate the executable research plan
        print(f"  - Generating research plan for topic: '{topic}'")
        try:
            research_plan_content = plan_deep_research(topic=topic)
            research_plan_file = "research_plan.txt"
            with open(research_plan_file, "w") as f:
                f.write(research_plan_content)
        except Exception as e:
            agent_state.error = f"Failed to generate research plan: {e}"
            return self.get_trigger("RESEARCHING", "ERROR")

        # 2. Validate the plan against the research FSM
        print(f"  - Validating '{research_plan_file}' against research FSM...")
        # The updated fdc_cli now reads the # FSM: directive from the plan file.
        validation_cmd = ["python3", "tooling/fdc_cli.py", "validate", research_plan_file]
        result = subprocess.run(validation_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            error_message = f"Research plan validation failed:\n{result.stderr}"
            agent_state.error = error_message
            # Clean up the invalid plan
            os.remove(research_plan_file)
            return self.get_trigger("RESEARCHING", "ERROR")

        # 3. Push the validated research plan onto the execution stack
        print("  - Research plan is valid. Pushing to execution stack.")
        parsed_commands = parse_plan(research_plan_content)
        agent_state.plan_stack.append(
            PlanContext(plan_path=research_plan_file, commands=parsed_commands)
        )
        agent_state.messages.append(
            {
                "role": "system",
                "content": f"L4 Deep Research Cycle initiated for topic: '{topic}'. Executing '{research_plan_file}'.",
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

    def do_execution(self, agent_state: AgentState) -> str:
        """
        Executes the plan using a stack-based approach to handle sub-plans (CFDC).
        """
        print("[MasterControl] State: EXECUTING")

        if not agent_state.plan_stack:
            print("[MasterControl] Execution Complete (plan stack is empty).")
            # Clean up the root plan files now that execution is fully complete
            if agent_state.plan_path and os.path.exists(agent_state.plan_path):
                os.remove(agent_state.plan_path)
            # Only remove the research plan if it was actually created.
            research_plan_path = "research_plan.txt"
            if os.path.exists(research_plan_path):
                os.remove(research_plan_path)
            return self.get_trigger("EXECUTING", "AWAITING_ANALYSIS")

        # Always work with the plan at the top of the stack
        current_context = agent_state.plan_stack[-1]
        commands = current_context.commands

        # If we've finished all steps in the current plan, pop it and continue
        if current_context.current_step >= len(commands):
            agent_state.plan_stack.pop()
            print(
                f"  - Finished sub-plan '{current_context.plan_path}'. Resuming parent."
            )
            # Re-enter the execution loop immediately to process the parent plan
            return self.get_trigger("EXECUTING", "EXECUTING")

        command_obj = commands[current_context.current_step]
        tool_name = command_obj.tool_name
        args_text = command_obj.args_text

        # --- Protocol Enforcement & Pre-computation ---
        # Handle special directives first
        if tool_name == "call_plan":
            return self._handle_call_plan(agent_state, args_text.strip().split())

        # Enforce protocol for destructive commands BEFORE checking for step completion
        if tool_name == "reset_all":
            error_message = "The 'reset_all' tool is deprecated and strictly forbidden. Its use is a critical protocol violation."
            agent_state.error = error_message
            print(f"[MasterControl] FATAL: {error_message}")
            return "execution_failed"

        # --- Standard Step Execution ---
        step_complete_file = "step_complete.txt"
        step_representation = (
            f"{tool_name} {args_text[:50]}..." if args_text else tool_name
        )
        print(f"  - Checking for agent completion of step: {step_representation}")
        if not os.path.exists(step_complete_file):
            print("  - Step not complete. Waiting for agent.")
            return "step_not_complete"

        print(f"  - Detected '{step_complete_file}'.")
        with open(step_complete_file, "r") as f:
            result = f.read()

        agent_state.messages.append(
            {
                "role": "system",
                "content": f"Completed step {current_context.current_step + 1} in '{current_context.plan_path}': {step_representation}\nResult: {result}",
            }
        )

        os.remove(step_complete_file)
        current_context.current_step += 1

        print(
            f"  - Step {current_context.current_step} of {len(commands)} in '{current_context.plan_path}' signaled complete."
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
            return self.get_trigger("AWAITING_ANALYSIS", "ERROR")

        # Check for the agent to signal analysis is complete
        analysis_complete_file = "analysis_complete.txt"
        print(
            f"  - Checking for agent to complete analysis and create '{analysis_complete_file}'..."
        )
        if not os.path.exists(analysis_complete_file):
            print("  - Analysis not complete. Waiting for agent.")
            return "analysis_not_complete"

        os.remove(analysis_complete_file)
        print(
            f"  - Detected and cleaned up '{analysis_complete_file}'. Analysis complete."
        )
        return self.get_trigger("AWAITING_ANALYSIS", "POST_MORTEM")

    def do_post_mortem(self, agent_state: AgentState) -> str:
        """
        Finalizes the post-mortem process, renaming the draft and compiling lessons.
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
            if compile_result.returncode != 0:
                # If knowledge compilation fails, it's a problem.
                # We can't proceed to self-correction without the lessons.
                compile_msg = f"Knowledge compilation failed: {compile_result.stderr}"
                agent_state.error = compile_msg
                print(f"  - {agent_state.error}")
                return self.get_trigger("POST_MORTEM", "ERROR")

            compile_msg = "Knowledge compilation successful."
            print(f"  - {compile_msg}")
            agent_state.messages.append({"role": "system", "content": compile_msg})

        except Exception as e:
            agent_state.error = f"Failed to finalize post-mortem report: {e}"
            print(f"[MasterControl] {agent_state.error}")
            return self.get_trigger("POST_MORTEM", "ERROR")

        print("[MasterControl] Post-Mortem Complete.")
        return self.get_trigger("POST_MORTEM", "SELF_CORRECTING")

    def do_self_correcting(self, agent_state: AgentState) -> str:
        """
        Runs the automated self-correction cycle based on compiled lessons.
        This is a mandatory step. Failure here will halt the process.
        """
        print("[MasterControl] State: SELF_CORRECTING")
        try:
            print("  - Running self-correction cycle...")
            correction_cmd = ["python3", "tooling/self_correction_orchestrator.py"]
            correction_result = subprocess.run(
                correction_cmd, capture_output=True, text=True
            )

            # Pipe the orchestrator's stdout to the agent's messages for transparency
            agent_state.messages.append(
                {
                    "role": "system",
                    "content": f"Self-Correction Output:\n{correction_result.stdout}",
                }
            )

            if correction_result.returncode != 0:
                # A failure in the self-correction cycle is a critical error.
                error_message = (
                    f"Self-correction cycle FAILED:\n{correction_result.stderr}"
                )
                agent_state.error = error_message
                print(f"  - {error_message}")
                return self.get_trigger("SELF_CORRECTING", "ERROR")

            print("  - Self-correction cycle completed successfully.")
            return self.get_trigger("SELF_CORRECTING", "AWAITING_SUBMISSION")

        except Exception as e:
            agent_state.error = f"An unexpected error occurred during the self-correction cycle: {e}"
            print(f"[MasterControl] {agent_state.error}")
            return self.get_trigger("SELF_CORRECTING", "ERROR")

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
            elif self.current_state == "RESEARCHING":
                trigger = self.do_researching(agent_state)
            elif self.current_state == "EXECUTING":
                trigger = self.do_execution(agent_state)
            elif self.current_state == "AWAITING_ANALYSIS":
                trigger = self.do_awaiting_analysis(agent_state)
            elif self.current_state == "POST_MORTEM":
                trigger = self.do_post_mortem(agent_state)
            elif self.current_state == "SELF_CORRECTING":
                trigger = self.do_self_correcting(agent_state)
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