# Curry-Howard Correspondence (CHC) Protocols

This directory contains a generalized framework for defining and verifying CHC protocols.

## Protocol Structure

Each CHC protocol is defined as a Python module that implements the `CHCProtocol` interface defined in `protocols/chc/protocol.py`.

A CHC protocol must implement the following methods:

- `get_proposition()`: Returns a string representation of the protocol's proposition.
- `check_preconditions(state)`: Checks if the preconditions for the protocol are met.
- `check_postconditions(initial_state, final_state)`: Checks if the postconditions for the protocol are met.
- `check_invariants(initial_state, final_state)`: Checks if the invariants of the protocol are maintained.
- `get_proof()`: Returns the proof of the protocol.
- `get_initial_state()`: Returns an initial state for the protocol.

## Verification

To verify a protocol, use the `verify_protocol` function in `protocols/chc/verifier.py`, passing the name of the protocol module as an argument.
