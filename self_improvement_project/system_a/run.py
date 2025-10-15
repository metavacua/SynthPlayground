import hashlib
import time
import os

# This script's working directory is its own location.
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, "history.log")

def diagonalize(input_string):
    """
    This is the DEFINABLE diagonalization function.
    It takes a string and produces a new, unique string.
    The logic is clear and contained entirely within the system.
    """
    timestamp = str(time.time_ns())
    combined = f"{input_string}-{timestamp}"
    return hashlib.sha256(combined.encode()).hexdigest()

def append_to_history(new_element):
    """
    Writes the new element to the history log.
    Crucially, this system NEVER reads this file. Its own history
    is undefinable from its perspective.
    """
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{new_element}\n")

def main():
    """
    System A's main loop. It performs its one function: to create.
    It takes a simple, non-state-aware input (the current time as a string)
    and generates a new element, which it logs but does not understand.
    """
    # The system is stateless, so its input is ephemeral.
    ephemeral_input = str(time.time_ns())

    print("System A: The Creator")
    print(f"  - Received ephemeral input: {ephemeral_input}")

    new_element = diagonalize(ephemeral_input)

    print(f"  - Generated new element: {new_element[:16]}...")

    append_to_history(new_element)

    print(f"  - New element has been logged to history.")
    print("  - The system remains unaware of its own history.")

if __name__ == "__main__":
    main()