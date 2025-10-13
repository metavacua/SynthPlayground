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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.master_control import MasterControlGraph
from tooling.state import AgentState
from utils.logger import Logger

def find_fsm_transition(fsm, source_state, trigger):
    """Finds the destination state for a given source and trigger."""
    for transition in fsm["transitions"]:
        if transition["source"] == source_state and transition["trigger"] == trigger:
            return transition["dest"]
    return None

def run_agent_loop(task_description: str):
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

    while mcg.current_state not in mcg.fsm["final_states"]:
        current_state = mcg.current_state
        print(f"[AgentShell] FSM State: {current_state}")

        trigger = None
        if current_state == "START":
            mcg.current_state = "ORIENTING"
            continue

        if current_state == "ORIENTING":
            trigger = mcg.do_orientation(agent_state, logger)

        elif current_state == "PLANNING":
            print("[AgentShell] Agent is now responsible for creating a plan.")
            plan_content = """\
# FSM: tooling/fsm.json
set_plan
This is a multi-step test plan.
---
message_user
This is the first step.
---
message_user
This is the second step, verifying the loop works.
"""
            trigger = mcg.do_planning(agent_state, plan_content, logger)


        elif current_state == "EXECUTING":
            step_to_execute = mcg.get_current_step(agent_state)
            if step_to_execute:
                print(f"[AgentShell] Agent must now execute: {step_to_execute.tool_name} {step_to_execute.args_text}")
                step_result = f"Successfully executed {step_to_execute.tool_name}."
                trigger = mcg.do_execution(agent_state, step_result, logger)
            else:
                trigger = mcg.do_execution(agent_state, None, logger) # Signals end of plan


        elif current_state == "FINALIZING":
            print("[AgentShell] Agent must now perform post-mortem analysis.")
            analysis_content = "The task was a test run to verify the new logging and artifact generation. It completed successfully."
            trigger = mcg.do_finalizing(agent_state, analysis_content, logger)

        else:
            agent_state.error = f"Unknown state encountered in AgentShell: {current_state}"
            mcg.current_state = "ERROR"
            break

        # Transition the FSM to the next state
        next_state = find_fsm_transition(mcg.fsm, current_state, trigger)
        if next_state:
            mcg.current_state = next_state
        else:
            agent_state.error = f"No transition found for state '{current_state}' with trigger '{trigger}'"
            mcg.current_state = "ERROR"
            break


    print(f"--- Agent Task Finished ---")
    print(f"Final FSM State: {mcg.current_state}")
    if agent_state.error:
        print(f"Error: {agent_state.error}")

    return agent_state

def main():
    """Main entry point for the agent shell."""
    task_description = "Perform a basic self-check and greet the user."
    run_agent_loop(task_description)

if __name__ == "__main__":
    main()