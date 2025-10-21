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
import json
import importlib.util

# Add the root directory to the path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.master_control import MasterControlGraph
from tooling.state import AgentState
from utils.logger import Logger
from tooling.udc_orchestrator import UDCOrchestrator


def load_tools_from_manifest(manifest_path="tooling/tool_manifest.json"):
    """Loads tools from the tool manifest."""
    tools = {}
    if not os.path.exists(manifest_path):
        print(f"Warning: Tool manifest not found at {manifest_path}")
        return tools

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    for tool_def in manifest.get("tools", []):
        tool_name = tool_def.get("name")
        module_path = tool_def.get("path")
        function_name = tool_def.get(
            "function_name", tool_name
        )  # Assume function name is tool name if not specified

        if not all([tool_name, module_path, function_name]):
            print(f"Skipping invalid tool definition: {tool_def}")
            continue

        try:
            # Convert file path to a module name that can be imported
            module_name = os.path.splitext(os.path.basename(module_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tool_function = getattr(module, function_name)
            tools[tool_name] = tool_function
            print(f"Successfully loaded tool: '{tool_name}' from {module_path}")
        except Exception as e:
            print(f"Error loading tool '{tool_name}' from '{module_path}': {e}")

    return tools


def find_fsm_transition(fsm, source_state, trigger):
    """Finds the destination state for a given source and trigger."""
    for transition in fsm["transitions"]:
        if transition["source"] == source_state and transition["trigger"] == trigger:
            return transition["dest"]
    return None


import argparse


def run_agent_loop(
    task_description: str, tools: dict, model: str = None, plan_content: str = None
):
    """
    The main loop that drives the agent's lifecycle via the FSM.
    """
    # 1. Initialize State and Logger
    task_id = f"task-{uuid.uuid4()}"
    agent_state = AgentState(task=task_id, task_description=task_description)
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
            # If a plan is provided directly, use it.
            if plan_content:
                trigger = mcg.do_planning(agent_state, plan_content, logger)
            # If a CSDC model is specified, load the corresponding plan
            elif model:
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
                tool_name = step_to_execute.tool_name
                tool_args = step_to_execute.args_text
                print(f"[AgentShell] Agent must now execute: {tool_name} {tool_args}")

                tool_function = tools.get(tool_name)
                if tool_function:
                    try:
                        # This is a simplified approach to argument parsing.
                        # A more robust solution would inspect the tool's signature.
                        if tool_args:
                            step_result = tool_function(tool_args)
                        else:
                            step_result = tool_function()
                        trigger = mcg.do_execution(
                            agent_state, str(step_result) if step_result else "", logger
                        )
                    except Exception as e:
                        agent_state.error = f"Error executing tool '{tool_name}': {e}"
                        mcg.current_state = "ERROR"
                        continue
                else:
                    agent_state.error = f"Tool '{tool_name}' not found."
                    mcg.current_state = "ERROR"
                    continue
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
    parser.add_argument(
        "--udc-plan",
        type=str,
        default=None,
        help="Run the UDC orchestrator with the specified plan file.",
    )
    parser.add_argument(
        "--plan-file",
        type=str,
        default=None,
        help="Run the agent with a specific plan file.",
    )
    args = parser.parse_args()

    # If a UDC plan is specified, run the UDC orchestrator directly.
    if args.udc_plan:
        print(f"--- Running in UDC Mode with plan: {args.udc_plan} ---")
        if not os.path.exists(args.udc_plan):
            print(f"Error: UDC plan file not found at '{args.udc_plan}'")
            sys.exit(1)

        orchestrator = UDCOrchestrator(plan_path=args.udc_plan)
        orchestrator.run()
        return

    # If a plan file is specified, run the agent with that plan.
    if args.plan_file:
        print(f"--- Running in Plan File Mode with plan: {args.plan_file} ---")
        if not os.path.exists(args.plan_file):
            print(f"Error: Plan file not found at '{args.plan_file}'")
            sys.exit(1)

        with open(args.plan_file, "r") as f:
            plan_content = f.read()

        tools = load_tools_from_manifest()
        run_agent_loop("Executing plan from file.", tools, plan_content=plan_content)
        return

    # Otherwise, proceed with the normal agent loop.
    task_description = "Perform a basic self-check and greet the user."
    if args.model:
        task_description = (
            f"Execute a self-improvement task under CSDC Model {args.model}."
        )

    tools = load_tools_from_manifest()
    run_agent_loop(task_description, tools, model=args.model)


if __name__ == "__main__":
    main()
