"""
The new, interactive, API-driven entry point for the agent.

This script replaces the old file-based signaling system with a direct,
programmatic interface to the MasterControlGraph FSM. It is responsible for:
1.  Initializing the agent's state and a centralized logger.
2.  Instantiating and running the MasterControlGraph.
3.  Driving the FSM by calling its methods and passing data and the logger.
4.  Containing the core "agent logic" (e.g., an LLM call) to generate plans
    and respond to requests for action.
"""

import uuid
import os
import sys

# Add the root directory to the path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.master_control import MasterControlGraph
from tooling.state import AgentState
from utils.logger import Logger


def find_fsm_transition(fsm, source_state, trigger):
    """Finds the destination state for a given source and trigger."""
    for transition in fsm["transitions"]:
        if transition["source"] == source_state and transition["trigger"] == trigger:
            return transition["dest"]
    return None


import argparse


def run_agent_loop(task_description: str, tools: dict, model: str = None):
    """
    The main loop that drives the agent's lifecycle via the FSM.
    """
    # 1. Initialize State and Logger
    task_id = f"task-{uuid.uuid4()}"
    agent_state = AgentState(task=task_id)
    # Ensure the schema path is correct relative to the repo root
    schema_path = os.path.join(os.path.dirname(__file__), "..", "LOGGING_SCHEMA.md")
    logger = Logger(schema_path=schema_path)
    mcg = MasterControlGraph()

    print(f"--- Starting Agent Task: {task_description} ({task_id}) ---")
    if model:
        print(f"--- Running under CSDC Model: {model} ---")

    while mcg.current_state not in mcg.fsm["final_states"]:
        current_state = mcg.current_state
        print(f"[AgentShell] FSM State: {current_state}")

        trigger = None
        if current_state == "START":
            mcg.current_state = "ORIENTING"
            continue

        if current_state == "ORIENTING":
            trigger = mcg.do_orientation(agent_state, logger, tools)

        elif current_state == "PLANNING":
            # If a CSDC model is specified, load the corresponding plan
            if model:
                plan_path = f"plans/self_improvement_model_{model.lower()}.txt"
                print(f"[AgentShell] Loading CSDC plan from: {plan_path}")
                try:
                    with open(plan_path, "r") as f:
                        plan_content = f.read()

                    # Validate the plan against the specified model
                    is_valid, error_message = mcg.validate_plan_for_model(
                        plan_content, model
                    )
                    if not is_valid:
                        agent_state.error = (
                            f"Plan validation failed for model {model}: {error_message}"
                        )
                        mcg.current_state = "ERROR"
                        continue

                    print(f"[AgentShell] Plan is valid for Model {model}.")
                    trigger = mcg.do_planning(agent_state, plan_content, logger)

                except FileNotFoundError:
                    agent_state.error = f"Plan file not found: {plan_path}"
                    mcg.current_state = "ERROR"
                    continue
            # If we have research findings, create a real plan.
            elif agent_state.research_findings:
                print("[AgentShell] Research complete. Now creating an informed plan.")
                plan_content = """\
# FSM: tooling/fsm.json
set_plan
This is a plan created with research findings.
---
message_user
The research findings have been integrated.
"""
                trigger = mcg.do_planning(agent_state, plan_content, logger)
            # Otherwise, create a plan to do research first.
            else:
                print("[AgentShell] No research found. Planning to do research first.")
                # This is a meta-command, so we transition directly.
                mcg.current_state = "RESEARCHING"
                continue

        elif current_state == "RESEARCHING":
            trigger = mcg.do_researching(agent_state, logger)

        elif current_state == "AWAITING_RESULT":
            trigger = mcg.do_awaiting_result(agent_state, logger)

        elif current_state == "EXECUTING":
            step_to_execute = mcg.get_current_step(agent_state)
            if step_to_execute:
                print(
                    f"[AgentShell] Agent must now execute: {step_to_execute.tool_name} {step_to_execute.args_text}"
                )
                step_result = f"Successfully executed {step_to_execute.tool_name}."
                trigger = mcg.do_execution(agent_state, step_result, logger)
            else:
                trigger = mcg.do_execution(
                    agent_state, None, logger
                )  # Signals end of plan

        elif current_state == "FINALIZING":
            print("[AgentShell] Agent must now perform post-mortem analysis.")
            analysis_content = "The task was a test run to verify the new logging and artifact generation. It completed successfully."
            trigger = mcg.do_finalizing(agent_state, analysis_content, logger)

        else:
            agent_state.error = (
                f"Unknown state encountered in AgentShell: {current_state}"
            )
            mcg.current_state = "ERROR"

        # Transition the FSM to the next state
        next_state = find_fsm_transition(mcg.fsm, current_state, trigger)
        if next_state:
            mcg.current_state = next_state
        else:
            agent_state.error = f"No transition found for state '{current_state}' with trigger '{trigger}'"
            mcg.current_state = "ERROR"

        if mcg.current_state == "ERROR":
            print(f"[AgentShell] FSM entered ERROR state. Error: {agent_state.error}")
            break

    print("--- Agent Task Finished ---")
    print(f"Final FSM State: {mcg.current_state}")
    if agent_state.error:
        print(f"Error: {agent_state.error}")

    return agent_state


def main():
    """Main entry point for the agent shell."""
    parser = argparse.ArgumentParser(description="The main entry point for the agent.")
    parser.add_argument(
        "--model",
        choices=["A", "B"],
        default=None,
        help="The CSDC model to run the agent under (A or B).",
    )
    args = parser.parse_args()

    task_description = "Perform a basic self-check and greet the user."
    if args.model:
        task_description = (
            f"Execute a self-improvement task under CSDC Model {args.model}."
        )

    run_agent_loop(task_description, None, model=args.model)


if __name__ == "__main__":
    main()
