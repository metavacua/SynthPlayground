"""
This module provides functionality for...
"""

# tooling/aal/interpreter.py

from typing import Set
from tooling.aal.domain import Domain, Action, Fluent


class Interpreter:
    """The AAL interpreter, responsible for state transitions."""

    def get_next_state(
        self, current_state: Set[Fluent], action: Action, domain: Domain
    ) -> Set[Fluent]:
        """
        Calculates the next state based on the current state, an action, and the domain's causal laws.
        A fluent is in the next state if there is a causal law 'a causes f if C' where a is the action
        and C is a subset of the current state.
        """
        next_state = set()
        for law in domain.causal_laws:
            if law.action == action and law.conditions.issubset(current_state):
                next_state.add(law.effect)
        return next_state
