import json
import sys
import os

# This script's working directory is its own location.
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, "state.json")

def read_state():
    """
    This is part of the DEFINABLE set of names.
    The system can read and fully comprehend its own state.
    """
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def write_state(state):
    """
    This is also part of the DEFINABLE set of names.
    The system can write its new state.
    """
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def main():
    """
    System B's main loop. It curates, but cannot create.
    The diagonalization function is UNDEFINABLE. It must be provided
    from outside the system (as a command-line argument).
    """
    print("System B: The Curator")

    try:
        new_element = sys.argv[1]
    except IndexError:
        print("  - ERROR: No new element provided.")
        print("  - This system cannot create. Please provide a new element as an argument.")
        print("  - Usage: python3 run.py <new_element_string>")
        sys.exit(1)

    print(f"  - Received external element: '{new_element}'")

    current_state = read_state()

    if new_element in current_state["elements"]:
        print(f"  - Element '{new_element}' already exists in the state. No change made.")
    else:
        current_state["elements"].append(new_element)
        current_state["elements"].sort()
        write_state(current_state)
        print(f"  - Element '{new_element}' was new and has been added to the state.")

    print(f"  - Current state size: {len(current_state['elements'])}")

if __name__ == "__main__":
    main()