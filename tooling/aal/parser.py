"""
This module provides functionality for...
"""

# tooling/aal/parser.py

import re
from tooling.aal.domain import Domain, Fluent, Action, CausalLaw


def parse_aal(aal_string: str) -> Domain:
    """Parses an AAL string and returns a Domain object."""
    domain = Domain()
    # Correctly split by newline characters.
    lines = aal_string.strip().split("\n")

    # Correctly match whitespace.
    fluent_pattern = re.compile(r"fluent\s+(\w+)")
    action_pattern = re.compile(r"action\s+(\w+)")
    causal_law_pattern = re.compile(r"(\w+)\s+causes\s+(\w+)(?:\s+if\s+(.*))?")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Try to match each pattern
        fluent_match = fluent_pattern.match(line)
        if fluent_match:
            fluent_name = fluent_match.group(1)
            domain.fluents.add(Fluent(name=fluent_name))
            continue

        action_match = action_pattern.match(line)
        if action_match:
            action_name = action_match.group(1)
            domain.actions.add(Action(name=action_name))
            continue

        causal_law_match = causal_law_pattern.match(line)
        if causal_law_match:
            action_name = causal_law_match.group(1)
            effect_name = causal_law_match.group(2)
            conditions_str = causal_law_match.group(3)

            action = Action(name=action_name)
            effect = Fluent(name=effect_name)

            conditions = frozenset()
            if conditions_str:
                condition_names = [c.strip() for c in conditions_str.split(",")]
                conditions = frozenset(Fluent(name=name) for name in condition_names)

            domain.causal_laws.add(
                CausalLaw(action=action, effect=effect, conditions=conditions)
            )
            continue

    return domain
