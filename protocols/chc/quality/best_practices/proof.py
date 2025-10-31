# protocols/chc/quality/best_practices/proof.py
from protocols.chc.protocol import CHCProtocol

class BestPracticesState:
    """A simplified representation of the best practices state."""
    def __init__(self):
        self.write_action_occurred = False
        self.is_verified = False

def verify_write(state: BestPracticesState) -> BestPracticesState:
    """
    This function is the constructive proof of the BEST-PRACTICES-001 proposition,
    representing the 'verify-after-write' rule.
    """
    if not state.write_action_occurred:
        raise AssertionError("A write action must occur before it can be verified.")
    state.is_verified = True
    return state

class Protocol(CHCProtocol):
    def get_proposition(self) -> str:
        return "BEST-PRACTICES-001"

    def check_preconditions(self, state):
        if not state.write_action_occurred:
            raise AssertionError("Precondition failed: No write action has occurred.")
        if state.is_verified:
            raise AssertionError("Precondition failed: Write action has already been verified.")

    def check_postconditions(self, initial_state, final_state):
        if not final_state.is_verified:
            raise AssertionError("Postcondition failed: Write action was not verified.")

    def check_invariants(self, initial_state, final_state):
        pass

    def get_proof(self):
        return verify_write

    def get_initial_state(self):
        # To run the proof, we start in a state where a write has just happened.
        initial_state = BestPracticesState()
        initial_state.write_action_occurred = True
        return initial_state
