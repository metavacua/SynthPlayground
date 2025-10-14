"""
The master orchestrator for the agent's lifecycle, governed by a Finite State Machine.

This script, master_control.py, is the heart of the agent's operational loop.
It implements a strict, protocol-driven workflow defined in a JSON file
(typically `tooling/fsm.json`). The MasterControlGraph class reads this FSM
definition and steps through the prescribed states, ensuring that the agent
cannot deviate from the established protocol.

This version has been refactored to be a library controlled by an external
shell (e.g., `agent_shell.py`), eliminating all file-based polling and making
the interaction purely programmatic and fully logged.
"""
import json
import sys
import os
import subprocess
import shutil
import datetime
import tempfile
import time

from tooling.state import AgentState, PlanContext
from tooling.research import execute_research_protocol
from tooling.research_planner import plan_deep_research
from tooling.plan_parser import parse_plan, Command
from utils.logger import Logger

MAX_RECURSION_DEPTH = 10

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

    def do_orientation(self, agent_state: AgentState, logger: Logger) -> str:
        """
        Executes orientation, including analyzing the last post-mortem.
        """
        logger.log("Phase 1", agent_state.task, -1, "INFO", {"state": "ORIENTING"}, "SUCCESS")
        try:
            # Analyze the most recent post-mortem report
            postmortem_dir = "postmortems/"
            if os.path.exists(postmortem_dir):
                postmortem_files = [os.path.join(postmortem_dir, f) for f in os.listdir(postmortem_dir) if f.endswith(".md")]
                if postmortem_files:
                    latest_postmortem = max(postmortem_files, key=os.path.getctime)
                    with open(latest_postmortem, "r") as f:
                        postmortem_content = f.read()
                    agent_state.messages.append({"role": "system", "content": f"Reviewing last task's post-mortem:\n{postmortem_content}"})
                    logger.log("Phase 1", agent_state.task, -1, "INFO", {"summary": f"Analyzed post-mortem: {latest_postmortem}"}, "SUCCESS")

            # L1, L2, L3 steps...
            agent_state.orientation_complete = True
            logger.log("Phase 1", agent_state.task, -1, "INFO", {"summary": "Orientation successful."}, "SUCCESS")
            return self.get_trigger("ORIENTING", "PLANNING")
        except Exception as e:
            agent_state.error = f"Orientation failed: {e}"
            logger.log("Phase 1", agent_state.task, -1, "SYSTEM_FAILURE", {"state": "ERROR"}, "FAILURE", str(e))
            return self.get_trigger("ORIENTING", "ERROR")

    def do_planning(self, agent_state: AgentState, plan_content: str, logger: Logger) -> str:
        """
        Validates a given plan, parses it, and initializes the plan stack.
        """
        logger.log("Phase 2", agent_state.task, 0, "INFO", {"state": "PLANNING"}, "SUCCESS")

        is_valid, error_message = self._validate_plan_in_memory(plan_content)

        if not is_valid:
            agent_state.error = error_message
            logger.log("Phase 2", agent_state.task, 0, "PLAN_UPDATE", {"plan": plan_content}, "FAILURE", error_message)
            return self.get_trigger("PLANNING", "ERROR")

        logger.log("Phase 2", agent_state.task, 0, "PLAN_UPDATE", {"plan": plan_content}, "SUCCESS")
        parsed_commands = parse_plan(plan_content)
        agent_state.plan_path = "agent_generated_plan"
        agent_state.plan_stack.append(
            PlanContext(plan_path=agent_state.plan_path, commands=parsed_commands)
        )
        return "plan_op"

    def _validate_plan_in_memory(self, plan_content: str) -> (bool, str):
        """
        Validates a plan in-memory against the FSM without calling an external script.
        """
        ACTION_TYPE_MAP = {
            "set_plan": "plan_op",
            "message_user": "step_op",
            "plan_step_complete": "step_op",
            "submit": "submit_op",
            "create_file_with_block": "write_op",
            "overwrite_file_with_block": "write_op",
            "replace_with_git_merge_diff": "write_op",
            "read_file": "read_op",
            "list_files": "read_op",
            "grep": "read_op",
            "delete_file": "delete_op",
            "rename_file": "move_op",
            "run_in_bash_session": "tool_exec",
            "call_plan": "call_plan_op",
            "research": "research_requested",
        }

        commands = parse_plan(plan_content)
        current_state = "PLANNING" # Validation always starts from the PLANNING state

        for command in commands:
            action_type = ACTION_TYPE_MAP.get(command.tool_name)
            if not action_type:
                return False, f"Unknown command '{command.tool_name}' in plan."

            next_state = None
            for transition in self.fsm["transitions"]:
                if transition["source"] == current_state and transition["trigger"] == action_type:
                    next_state = transition["dest"]
                    break

            if not next_state:
                return False, f"Invalid FSM transition. Cannot perform action '{action_type}' (from tool '{command.tool_name}') from state '{current_state}'."

            current_state = next_state

        if current_state not in self.fsm["final_states"] and current_state != "EXECUTING":
             return False, f"Plan does not end in a valid state. Final state: '{current_state}'"

        return True, ""

    def do_researching(self, agent_state: AgentState, logger: Logger) -> str:
        """
        Launches the background research process.
        """
        logger.log("Phase 3", agent_state.task, -1, "INFO", {"state": "RESEARCHING"}, "SUCCESS")
        try:
            task_id = agent_state.task
            process = subprocess.Popen(
                ["python", "tooling/background_researcher.py", task_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            agent_state.background_processes["research"] = process
            logger.log("Phase 3", task_id, -1, "INFO", {"summary": f"Started background research (PID: {process.pid})"}, "SUCCESS")
            return self.get_trigger("RESEARCHING", "AWAITING_RESULT")
        except Exception as e:
            agent_state.error = f"Failed to start research process: {e}"
            logger.log("Phase 3", agent_state.task, -1, "SYSTEM_FAILURE", {"state": "ERROR"}, "FAILURE", str(e))
            return self.get_trigger("RESEARCHING", "ERROR")

    def do_awaiting_result(self, agent_state: AgentState, logger: Logger) -> str:
        """
        Checks for the result of the background research process.
        """
        task_id = agent_state.task
        result_path = f"/tmp/{task_id}.result"
        if os.path.exists(result_path):
            with open(result_path, "r") as f:
                result = f.read()
            os.remove(result_path) # Clean up the result file
            # Store and log the research findings
            agent_state.research_findings["report"] = result
            report_path = f"reports/{task_id}-research.md"
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            with open(report_path, "w") as f:
                f.write(f"# Research Report for Task: {task_id}\n\n{result}")
            logger.log("Phase 3", task_id, -1, "RESEARCH_REPORT", {"path": report_path}, "SUCCESS")
            return self.get_trigger("AWAITING_RESULT", "PLANNING")
        else:
            # Check if the process is still running
            process = agent_state.background_processes.get("research")
            if process and process.poll() is not None: # Process has terminated
                stdout, stderr = process.communicate()
                agent_state.error = f"Research process failed with code {process.returncode}.\nStderr: {stderr.decode()}"
                logger.log("Phase 3", task_id, -1, "SYSTEM_FAILURE", {"state": "ERROR"}, "FAILURE", agent_state.error)
                return self.get_trigger("AWAITING_RESULT", "ERROR") # Should be a transition from AWAITING_RESULT to ERROR

            logger.log("Phase 3", task_id, -1, "INFO", {"summary": "Waiting for research result..."}, "SUCCESS")
            time.sleep(1) # Wait before checking again
            return self.get_trigger("AWAITING_RESULT", "AWAITING_RESULT")

    def get_current_step(self, agent_state: AgentState) -> Command | None:
        """
        Returns the current command to be executed by the agent, or None if execution is complete.
        """
        if not agent_state.plan_stack:
            return None
        current_context = agent_state.plan_stack[-1]
        if current_context.current_step >= len(current_context.commands):
            return None
        return current_context.commands[current_context.current_step]

    def do_execution(self, agent_state: AgentState, step_result: str | None, logger: Logger) -> str:
        """
        Processes the result of a step and advances the execution state.
        """
        logger.log("Phase 4", agent_state.task, -1, "INFO", {"state": "EXECUTING"}, "SUCCESS")

        if not agent_state.plan_stack:
            return self.get_trigger("EXECUTING", "FINALIZING")

        current_context = agent_state.plan_stack[-1]
        if current_context.current_step >= len(current_context.commands):
            agent_state.plan_stack.pop()
            if not agent_state.plan_stack:
                return self.get_trigger("EXECUTING", "FINALIZING")
            else:
                return self.get_trigger("EXECUTING", "EXECUTING")

        command_obj = current_context.commands[current_context.current_step]
        logger.log(
            "Phase 4",
            agent_state.task,
            current_context.current_step,
            "TOOL_EXEC",
            {"tool_name": command_obj.tool_name, "args_text": command_obj.args_text},
            "SUCCESS",
            step_result
        )

        current_context.current_step += 1
        return "step_op"

    def do_finalizing(self, agent_state: AgentState, analysis_content: str, logger: Logger) -> str:
        """
        Handles the finalization of the task with agent-provided analysis.
        """
        logger.log("Phase 5", agent_state.task, -1, "INFO", {"state": "FINALIZING"}, "SUCCESS")
        try:
            task_id = agent_state.task
            final_path = f"postmortems/{datetime.date.today()}-{task_id}.md"
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            report_content = f"# Post-Mortem Report for Task: {task_id}\n\n## Agent Analysis\n\n{analysis_content}\n"
            with open(final_path, "w") as f:
                f.write(report_content)

            logger.log("Phase 5", task_id, -1, "POST_MORTEM", {"path": final_path, "content": report_content}, "SUCCESS")

            # Knowledge compilation and self-correction would also be logged here

            return self.get_trigger("FINALIZING", "AWAITING_SUBMISSION")
        except Exception as e:
            agent_state.error = f"An unexpected error occurred during finalization: {e}"
            logger.log("Phase 5", agent_state.task, -1, "SYSTEM_FAILURE", {"state": "ERROR"}, "FAILURE", str(e))
            return self.get_trigger("FINALIZING", "finalization_failed")