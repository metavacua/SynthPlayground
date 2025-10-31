# protocols/chc/core/standing_orders/proof.py
from protocols.chc.protocol import CHCProtocol

class StandingOrdersState:
    """A simplified representation of the standing orders state."""
    def __init__(self):
        self.orders_followed = False
        self.fdc_started = False

def follow_orders(state: StandingOrdersState) -> StandingOrdersState:
    """
    This function is the constructive proof of the STANDING-ORDERS-001 proposition.
    """
    state.fdc_started = True
    state.orders_followed = True
    return state

class Protocol(CHCProtocol):
    def get_proposition(self) -> str:
        return "STANDING-ORDERS-001"

    def check_preconditions(self, state):
        if state.orders_followed:
            raise AssertionError("Precondition failed: Orders have already been followed.")

    def check_postconditions(self, initial_state, final_state):
        if not final_state.orders_followed:
            raise AssertionError("Postcondition failed: Orders were not followed.")
        if not final_state.fdc_started:
            raise AssertionError("Postcondition failed: FDC was not started.")

    def check_invariants(self, initial_state, final_state):
        pass

    def get_proof(self):
        return follow_orders

    def get_initial_state(self):
        return StandingOrdersState()
