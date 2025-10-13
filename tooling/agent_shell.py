"""
The new, interactive, API-driven entry point for the agent.

This script replaces the old file-based signaling system with a direct,
programmatic interface to the MasterControlGraph FSM. It is responsible for:
1.  Initializing the agent's state.
2.  Instantiating and running the MasterControlGraph.
3.  Driving the FSM by calling its methods and passing data directly.
4.  Containing the core "agent logic" (e.g., an LLM call) to generate plans
    and respond to requests for action.
"""
import sys
import uuid

# Add tooling directory to path to import other tools
sys.path.insert(0, "./tooling")

from master_control import MasterControlGraph
from state import AgentState

def run_agent_loop(task_description: str):
    """
    The main loop that drives the agent's lifecycle via the FSM.
    """
    # 1. Initialize State
    agent_state = AgentState(task=task_description)
    mcg = MasterControlGraph()

    print(f"--- Starting Agent Task: {task_description} ---")

    while mcg.current_state not in mcg.fsm["final_states"]:
        current_state = mcg.current_state
        print(f"[AgentShell] FSM State: {current_state}")

        if current_state == "START":
            mcg.current_state = "ORIENTING"
            continue

        if current_state == "ORIENTING":
            # The FSM handles this state transition internally
            trigger = mcg.do_orientation(agent_state)

        elif current_state == "PLANNING":
            # TODO: Replace this with a real call to the agent's brain (e.g., LLM)
            print("[AgentShell] Agent is now responsible for creating a plan.")
            plan_content = """\
# FSM: tooling/fsm.json
# This is a placeholder plan.
message_user
Hello! I am ready to begin.
"""
            # Pass the plan content directly to the FSM
            trigger = mcg.do_planning(agent_state, plan_content)

        elif current_state == "EXECUTING":
            # The FSM will now tell us which step to execute.
            # In this new model, the shell is responsible for "executing" the step
            # and signaling completion.
            step_to_execute = mcg.get_current_step(agent_state)
            if step_to_execute:
                print(f"[AgentShell] Agent must now execute: {step_to_execute.tool_name} {step_to_execute.args_text}")
                # TODO: Add logic to actually execute the tool call
                step_result = "Placeholder result from tool execution."
                trigger = mcg.do_execution(agent_state, step_result)
            else:
                # No more steps in the current plan(s)
                trigger = mcg.do_execution(agent_state, None)


        elif current_state == "FINALIZING":
            # TODO: Add agent logic for post-mortem analysis
            print("[AgentShell] Agent must now perform post-mortem analysis.")
            analysis_content = "This was a successful task."
            trigger = mcg.do_finalizing(agent_state, analysis_content)

        else:
            agent_state.error = f"Unknown state encountered in AgentShell: {current_state}"
            mcg.current_state = "ERROR"
            break

        # Transition the FSM to the next state
        mcg.current_state = mcg.fsm["transitions"][mcg.current_state][trigger]

    print(f"--- Agent Task Finished ---")
    print(f"Final FSM State: {mcg.current_state}")
    if agent_state.error:
        print(f"Error: {agent_state.error}")

    return agent_state

def main():
    """Main entry point for the agent shell."""
    task_id = f"task-{uuid.uuid4()}"
    # In a real scenario, this would come from user input
    task_description = "Perform a basic self-check and greet the user."
    run_agent_loop(task_description)

if __name__ == "__main__":
    main()