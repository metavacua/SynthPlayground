"""
A command-line tool for proving sequents in Intuitionistic Linear Logic.

This script provides a basic interface to a simple logic prover. It takes a
sequent as a command-line argument, parses it into a logical structure, and
then attempts to prove it using a rudimentary proof search algorithm.

The primary purpose of this tool is to allow the agent to perform formal
reasoning and verification tasks by checking the validity of logical entailments.
For example, it can be a used to verify that a certain conclusion follows from a
set of premises according to the rules of linear logic.

The current implementation uses a very basic parser and proof algorithm,
serving as a placeholder and demonstration for a more sophisticated, underlying
logic engine.
"""

import argparse
import sys
from pathlib import Path

# Add the parent directory to the path to allow imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from logic_system.src.formulas import LinImplies
from logic_system.src.sequents import Sequent
from tooling.hdl_parser import parse_sequent


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
            if (
                formula.left in sequent.antecedent
                and formula.right in sequent.succedent
            ):
                return True

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Prove a sequent in Intuitionistic Linear Logic."
    )
    parser.add_argument(
        "sequent", type=str, help="The sequent to prove, e.g., 'A, A -> B |- B'"
    )
    args = parser.parse_args()

    try:
        sequent = parse_sequent(args.sequent)
        if prove_sequent(sequent):
            print("Provable")
            return True
        else:
            print("Not provable")
            return False
    except Exception as e:
        print(f"Error proving sequent: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
