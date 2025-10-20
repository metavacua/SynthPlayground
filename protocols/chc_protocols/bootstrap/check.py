# check.py
import os
from proof import bootstrap, AgentState

def check_proof():
    """
    This function is the proof checker for the AGENT-BOOTSTRAP-001 proposition.

    It verifies that the `bootstrap` function in `proof.py` is a valid
    constructive proof of the proposition defined in `README.md`.
    """
    print("Running proof checker for AGENT-BOOTSTRAP-001...")

    # 1. Create a valid initial state.
    initial_state = AgentState()

    # 2. Execute the proof.
    try:
        contextualized_state = bootstrap(initial_state)
    except Exception as e:
        print(f"Proof failed with an exception: {e}")
        return False

    # 3. Verify postconditions.
    if contextualized_state.state != "contextualized":
        print("Postcondition failed: Agent is not in contextualized state.")
        return False
    if "AGENTS.md" not in contextualized_state.protocols:
        print("Postcondition failed: AGENTS.md was not loaded.")
        return False
    if contextualized_state.plan is not None:
        print("Postcondition failed: Plan is not empty.")
        return False

    # 4. Verify invariants (already done in the proof, but we could add more checks here)

    print("Proof is valid.")
    return True

if __name__ == "__main__":
    if check_proof():
        print("AGENT-BOOTSTRAP-001 protocol is sound.")
    else:
        print("AGENT-BOOTSTRAP-001 protocol is not sound.")
        exit(1)
