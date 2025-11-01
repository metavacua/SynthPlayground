# protocols/chc/core_protocols/tdd/proof.py
from protocols.chc.protocol import CHCProtocol

class TDDState:
    """A simplified representation of the TDD state for this proof."""
    def __init__(self, has_failing_test=False):
        self.has_failing_test = has_failing_test
        self.code_written = False

def write_code(tdd_state: TDDState) -> TDDState:
    """
    This function is the constructive proof of the TDD-PROTOCOL-001 proposition.
    """
    if not tdd_state.has_failing_test:
        raise AssertionError("Cannot write code without a failing test.")
    tdd_state.code_written = True
    return tdd_state

class Protocol(CHCProtocol):
    def get_proposition(self) -> str:
        return "TDD-PROTOCOL-001"

    def check_preconditions(self, state):
        if state.code_written:
            raise AssertionError("Precondition failed: Code has already been written.")

    def check_postconditions(self, initial_state, final_state):
        if not final_state.code_written:
            raise AssertionError("Postcondition failed: Code was not written.")

    def check_invariants(self, initial_state, final_state):
        pass

    def get_proof(self):
        return write_code

    def get_initial_state(self):
        return TDDState(has_failing_test=True)
