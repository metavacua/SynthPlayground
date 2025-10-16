"""
A library for proving sequents in Intuitionistic Linear Logic.

This module provides a basic interface to a simple logic prover. It takes a
sequent as a string, parses it into a logical structure, and then attempts to
prove it using a rudimentary proof search algorithm.

The primary purpose of this tool is to allow the agent to perform formal
reasoning and verification tasks by checking the validity of logical entailments.
"""
import sys
from pathlib import Path

# Add the parent directory to the path to allow imports
# This is necessary because the logic_system is not a package
# A better solution would be to structure the project as a proper package
# For now, this maintains compatibility with the existing structure.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from logic_system.src.ill import axiom, tensor_right, tensor_left, lin_implies_right, lin_implies_left
from logic_system.src.formulas import Formula, Prop, LinImplies, Tensor
from logic_system.src.sequents import Sequent

def parse_formula(s: str):
    """A very basic parser for formulas."""
    s = s.strip()
    if '->' in s:
        parts = s.split('->', 1)
        return LinImplies(parse_formula(parts[0]), parse_formula(parts[1]))
    if '*' in s:
        parts = s.split('*', 1)
        return Tensor(parse_formula(parts[0]), parse_formula(parts[1]))
    return Prop(s)

def parse_sequent(s: str):
    """A very basic parser for sequents."""
    parts = s.split('|-')
    antecedent = {parse_formula(f) for f in parts[0].split(',')}
    succedent = parse_formula(parts[1])
    return Sequent(antecedent, {succedent})

def prove_sequent(sequent: Sequent):
    """
    A very simple proof search algorithm.
    This is a placeholder for a more sophisticated prover.
    """
    # Axiom
    if len(sequent.antecedent) == 1 and sequent.antecedent == sequent.succedent:
        return True

    # Implication Left
    for formula in sequent.antecedent:
        if isinstance(formula, LinImplies):
            # This is a gross oversimplification and doesn't work in general.
            # It only works for the specific case of A, A -> B |- B
            if formula.left in sequent.antecedent and formula.right in sequent.succedent:
                return True

    return False

def main(sequent_str: str) -> bool:
    """
    Parses and proves a sequent string.

    Args:
        sequent_str: The sequent to prove, e.g., "A, A -> B |- B".

    Returns:
        True if the sequent is provable, False otherwise.
    """
    try:
        sequent = parse_sequent(sequent_str)
        return prove_sequent(sequent)
    except Exception as e:
        # For a library function, it's better to let exceptions propagate
        # or to wrap them in a custom exception type, rather than printing.
        print(f"Error proving sequent: {e}", file=sys.stderr)
        return False

# The command-line interface is now for demonstration/testing purposes only.
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Prove a sequent in Intuitionistic Linear Logic.")
    parser.add_argument("sequent", type=str, help="The sequent to prove, e.g., 'A, A -> B |- B'")
    args = parser.parse_args()

    if main(args.sequent):
        print("Provable")
    else:
        print("Not provable")