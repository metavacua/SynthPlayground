"""
A Linear Bounded Automaton (LBA) for validating Context-Sensitive Development Cycle (CSDC) plans.

This module implements a validator that enforces the context-sensitive rules of the CSDC.
Unlike a simple FSM, an LBA can inspect the entire input "tape" (the plan) to make
validation decisions. This is necessary to enforce rules where the validity of one
command depends on the presence or absence of another command elsewhere in the plan.

The CSDC defines two mutually exclusive models:
- Model A: Permits `define_set_of_names`, but forbids `define_diagonalization_function`.
- Model B: Permits `define_diagonalization_function`, but forbids `define_set_of_names`.

This validator checks for these co-occurrence constraints.
"""
from .plan_parser import parse_plan, Command

class LBAValidator:
    """
    A validator that uses LBA principles to enforce CSDC rules.
    """

    def validate(self, plan_content: str, model: str) -> (bool, str):
        """
        Validates a plan against a given CSDC model.

        Args:
            plan_content: The string content of the plan.
            model: The CSDC model to validate against ('A' or 'B').

        Returns:
            A tuple containing a boolean indicating validity and a string with an error message.
        """
        commands = parse_plan(plan_content)
        tool_names = {cmd.tool_name for cmd in commands}

        if model.upper() == 'A':
            if 'define_diagonalization_function' in tool_names:
                return False, "Validation Error: `define_diagonalization_function` is forbidden in Model A."
        elif model.upper() == 'B':
            if 'define_set_of_names' in tool_names:
                return False, "Validation Error: `define_set_of_names` is forbidden in Model B."
        else:
            return False, f"Unknown model '{model}'."

        # Cross-model check for mutual exclusivity
        if 'define_set_of_names' in tool_names and 'define_diagonalization_function' in tool_names:
            return False, "Validation Error: `define_set_of_names` and `define_diagonalization_function` cannot be used in the same plan."

        return True, ""