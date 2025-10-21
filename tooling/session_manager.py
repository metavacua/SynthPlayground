"""
This module provides a simple way to save and load the agent's session.
"""

import json
import os
from tooling.state import AgentState

SESSION_FILE = "agent_session.json"

def save_session(agent_state: AgentState):
    """
    Saves the agent's session to a file.
    """
    with open(SESSION_FILE, "w") as f:
        json.dump(agent_state.to_dict(), f)

def load_session() -> AgentState:
    """
    Loads the agent's session from a file.
    """
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return AgentState.from_dict(json.load(f))
    return AgentState()
