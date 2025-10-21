"""
Handles the saving and loading of the agent's session state.
"""

import json
import os
from tooling.state import AgentState, PlanContext
from tooling.plan_parser import Command

SESSION_FILE = 'knowledge_core/session.json'

def save_session(agent_state: AgentState):
    """
    Saves the agent's state to a JSON file.

    Args:
        agent_state: The AgentState object to save.
    """
    with open(SESSION_FILE, 'w') as f:
        json.dump(agent_state.to_json(), f, indent=4)

def load_session() -> AgentState:
    """
    Loads the agent's state from a JSON file.

    If no session file is found, a new AgentState is returned.

    Returns:
        The loaded or new AgentState object.
    """
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            data = json.load(f)
            plan_stack_data = data.get('plan_stack', [])
            plan_stack = [PlanContext(
                plan_path=ctx['plan_path'],
                commands=[Command(tool_name=cmd['tool_name'], args_text=cmd['args_text']) for cmd in ctx['commands']],
                current_step=ctx['current_step']
            ) for ctx in plan_stack_data]

            return AgentState(
                task=data.get('task'),
                plan_path=data.get('plan_path'),
                plan_stack=plan_stack,
                messages=data.get('messages', []),
                orientation_complete=data.get('orientation_complete', False),
                vm_capability_report=data.get('vm_capability_report'),
                research_findings=data.get('research_findings', {}),
                draft_postmortem_path=data.get('draft_postmortem_path'),
                final_report=data.get('final_report'),
                error=data.get('error')
            )
    else:
        return AgentState(task="New Task", plan_path=None)
