# protocols/chc/tooling/external_apis/proof.py
from protocols.chc.protocol import CHCProtocol

class ExternalApiState:
    """A simplified representation of the external API state."""
    def __init__(self):
        self.api_key_set = False
        self.api_called = False
        self.api_succeeded = False

def call_api(state: ExternalApiState) -> ExternalApiState:
    """
    This function is the constructive proof of the EXTERNAL-APIS-001 proposition.
    """
    if not state.api_key_set:
        raise AssertionError("Cannot call API without an API key.")
    state.api_called = True
    state.api_succeeded = True # In a real implementation, this would make a network request.
    return state

class Protocol(CHCProtocol):
    def get_proposition(self) -> str:
        return "EXTERNAL-APIS-001"

    def check_preconditions(self, state):
        if not state.api_key_set:
            raise AssertionError("Precondition failed: API key not set.")
        if state.api_called:
            raise AssertionError("Precondition failed: API has already been called.")

    def check_postconditions(self, initial_state, final_state):
        if not final_state.api_succeeded:
            raise AssertionError("Postcondition failed: API call did not succeed.")

    def check_invariants(self, initial_state, final_state):
        pass

    def get_proof(self):
        return call_api

    def get_initial_state(self):
        # We start in a state where the API key has been set.
        initial_state = ExternalApiState()
        initial_state.api_key_set = True
        return initial_state
