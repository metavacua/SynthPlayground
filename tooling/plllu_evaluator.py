import sys
import os
import argparse

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.pda_parser import parse_formula
from tooling.plllu_interpreter import FourValuedInterpreter, LogicValue, InterpretationError

def parse_context(context_string):
    """
    Parses a context string like "A:T, B:B, C:F" into a dictionary
    mapping atoms to LogicValue enums.
    """
    context = {}
    if not context_string:
        return context

    value_map = {
        'T': LogicValue.TRUE,
        'F': LogicValue.FALSE,
        'B': LogicValue.BOTH,
        'N': LogicValue.NEITHER,
    }

    parts = [part.strip() for part in context_string.split(',')]
    for part in parts:
        if ':' not in part:
            raise ValueError(f"Invalid context part: '{part}'. Expected format 'ATOM:VALUE'.")
        atom, value_char = part.split(':', 1)
        if value_char not in value_map:
            raise ValueError(f"Invalid logic value '{value_char}' for atom '{atom}'. Must be T, F, B, or N.")
        context[atom] = value_map[value_char]

    return context

def parse_sequent(sequent_string):
    """
    Parses a full sequent string into a context dictionary and a formula string.
    """
    if '|-' not in sequent_string:
        # Support formulas without a context for simple evaluation
        return {}, sequent_string.strip()

    context_str, formula_str = sequent_string.split('|-', 1)

    context = parse_context(context_str.strip())
    formula = formula_str.strip()

    return context, formula

def main():
    """
    The main entry point for the pLLLU evaluator pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Evaluate a pLLLU sequent using a four-valued logic."
    )
    parser.add_argument(
        "sequent",
        type=str,
        help="The pLLLU sequent to evaluate, e.g., 'A:T, B:B |- A & B'"
    )
    args = parser.parse_args()

    print(f"--- Evaluating Sequent: \"{args.sequent}\" ---")

    try:
        # 1. Parse the raw sequent string
        context, formula = parse_sequent(args.sequent)
        print(f"Context: { {k: v.name for k, v in context.items()} }, Formula: '{formula}'")

        # 2. PDA Layer: Parse the formula into an AST
        print("Step 1: Running PDA Parser...")
        ast = parse_formula(formula)
        print(f"  -> PDA Check PASSED.")

        # 3. Interpreter Layer: Evaluate the AST
        print("Step 2: Running Four-Valued Interpreter...")
        interpreter = FourValuedInterpreter(context)
        result = interpreter.interpret(ast)
        print(f"  -> Interpretation Complete.")

        # 4. Final Result
        print(f"\n--- Result: {result.name}")

    except (ValueError, SyntaxError, InterpretationError, NotImplementedError) as e:
        print(f"\n--- Evaluation Failed ---")
        print(f"Reason: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n--- An Unexpected Error Occurred ---")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # To run this from the command line:
    # python tooling/plllu_evaluator.py "A:T, B:F |- A & B"
    # python tooling/plllu_evaluator.py "A:B |- ∘A"
    main()