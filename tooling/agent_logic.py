"""
This module provides functionality for...
"""

def find_fsm_transition(fsm, source_state, trigger):
    """Finds the destination state for a given source and trigger."""
    for transition in fsm["transitions"]:
        if transition["source"] == source_state and transition["trigger"] == trigger:
            return transition["dest"]
    return None
