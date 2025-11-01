# protocols/chc/quality/compliance/proof.py
from protocols.chc.protocol import CHCProtocol

class ComplianceState:
    """A simplified representation of the compliance state."""
    def __init__(self, has_direct_edits=False, has_untested_changes=False):
        self.has_direct_edits = has_direct_edits
        self.has_untested_changes = has_untested_changes
        self.is_compliant = False

def check_compliance(state: ComplianceState) -> ComplianceState:
    """
    This function is the constructive proof of the COMPLIANCE-001 proposition.
    """
    if state.has_direct_edits:
        raise AssertionError("Compliance check failed: Direct edits to build artifacts are not allowed.")
    if state.has_untested_changes:
        raise AssertionError("Compliance check failed: All changes must be tested.")
    state.is_compliant = True
    return state

class Protocol(CHCProtocol):
    def get_proposition(self) -> str:
        return "COMPLIANCE-001"

    def check_preconditions(self, state):
        if state.is_compliant:
            raise AssertionError("Precondition failed: Compliance has already been checked.")

    def check_postconditions(self, initial_state, final_state):
        if not final_state.is_compliant:
            raise AssertionError("Postcondition failed: System is not compliant.")

    def check_invariants(self, initial_state, final_state):
        pass

    def get_proof(self):
        return check_compliance

    def get_initial_state(self):
        # We start in a state where no violations have been detected.
        return ComplianceState()
