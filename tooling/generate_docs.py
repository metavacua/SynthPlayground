"""
This script generates comprehensive Markdown documentation for the agent's
architecture, including the FSM, the agent shell, and the master control script.
"""
import json
import os
import inspect
import sys

# Add the root directory to the path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.master_control import MasterControlGraph

def get_fsm_details():
    """Extracts FSM states and transitions from fsm.json."""
    with open("tooling/fsm.json", "r") as f:
        fsm = json.load(f)
    return fsm["states"], fsm["transitions"]

def get_master_control_details():
    """Extracts details about the master control script's state handlers."""
    details = {}
    for name, method in inspect.getmembers(MasterControlGraph, inspect.isfunction):
        if name.startswith("do_"):
            state_name = name.replace("do_", "").upper()
            docstring = inspect.getdoc(method)
            details[state_name] = docstring.strip() if docstring else "No description available."
    return details

def generate_documentation():
    """Generates the final Markdown documentation."""
    states, transitions = get_fsm_details()
    mc_details = get_master_control_details()

    doc = "# Agent Architecture Documentation\n\n"
    doc += "This document provides a detailed overview of the agent's architecture, including the Finite State Machine (FSM) that governs its behavior.\n\n"

    doc += "## Finite State Machine (FSM)\n\n"
    doc += "The agent's lifecycle is managed by a strict FSM. Below are the defined states and the transitions between them.\n\n"

    doc += "### States\n\n"
    for state in states:
        doc += f"- **{state}**: {mc_details.get(state, 'No description available.')}\n"

    doc += "\n### Transitions\n\n"
    doc += "| Source State      | Trigger             | Destination State |\n"
    doc += "|-------------------|---------------------|-------------------|\n"
    for t in transitions:
        doc += f"| {t['source']:<17} | {t['trigger']:<19} | {t['dest']:<17} |\n"

    doc += "\n## Agent Shell (`tooling/agent_shell.py`)\n\n"
    doc += "The `agent_shell.py` script is the primary entry point for all agent tasks. It is responsible for initializing the agent's state, running the MasterControlGraph, and driving the FSM through its lifecycle.\n"

    os.makedirs("docs", exist_ok=True)
    with open("docs/agent_shell.md", "w") as f:
        f.write(doc)

    print("Documentation generated successfully in `docs/agent_shell.md`.")

if __name__ == "__main__":
    generate_documentation()