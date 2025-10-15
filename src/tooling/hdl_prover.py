"""
A command-line tool for proving logical sequents in Intuitionistic Linear Logic.

This script provides a basic interface to the underlying logic system, allowing
users to check the provability of a given sequent. It includes a simple parser
and a placeholder proof search algorithm.
"""
import argparse
import sys
from pathlib import Path

# Add the parent directory to the path to allow imports
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

def main(args=None):
    parser = argparse.ArgumentParser(description="Prove a sequent in Intuitionistic Linear Logic.")
    parser.add_argument("sequent", type=str, help="The sequent to prove, e.g., 'A, A -> B |- B'")
    args = parser.parse_args(args)

    try:
        sequent = parse_sequent(args.sequent)
        if prove_sequent(sequent):
            result = "Provable"
        else:
            result = "Not provable"
        print(result)
        return result
    except Exception as e:
        print(f"Error proving sequent: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()