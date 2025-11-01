# protocols/chc/verifier.py
import importlib

def verify_protocol(protocol_module_name: str):
    """
    Dynamically loads and verifies a CHC protocol.
    """
    print(f"Verifying protocol: {protocol_module_name}...")
    try:
        protocol_module = importlib.import_module(protocol_module_name)
        protocol = protocol_module.Protocol()

        initial_state = protocol.get_initial_state()

        protocol.check_preconditions(initial_state)

        proof = protocol.get_proof()
        final_state = proof(initial_state)

        protocol.check_postconditions(initial_state, final_state)
        protocol.check_invariants(initial_state, final_state)

        print(f"Protocol {protocol_module_name} is sound.")
        return True
    except Exception as e:
        print(f"Protocol {protocol_module_name} is not sound: {e}")
        return False
