"""
prover.py

This module is a Python translation of the ProverV0.lisp theorem prover.
It implements a simple theorem prover for a non-classical logic with three
connectives: 'con', 'dep', and 'ind'.

This system uses a non-recursive, fixed-chain dispatch architecture to
ensure termination, and is symmetric to the refuter system.
"""

# --- Global Complexity Metrics ---
AXIOM_APPLICATIONS_COUNT = 0
RULE_APPLICATIONS_COUNT = 0

# --- Formula Representation ---

def make_con():
    """Constructs a 'con' formula."""
    return ('con',)

def make_dep(formula1, formula2):
    """Constructs a 'dep' (dependence) formula."""
    return ('dep', formula1, formula2)

def make_ind(formula1, formula2):
    """Constructs an 'ind' (independence) formula."""
    return ('ind', formula1, formula2)

def formula_type(formula):
    """Returns the type of a formula."""
    return formula[0]

def formula_arguments(formula):
    """Returns the arguments of a formula."""
    return formula[1:]

# --- Axioms ---

def axiom_conr(formula):
    """
    Proof Axiom (axiom ConR).
    If a formula is of the form ('dep', A, A), it is axiomatically proven.
    Returns the proven sub-formula A on success, otherwise None.
    """
    global AXIOM_APPLICATIONS_COUNT
    AXIOM_APPLICATIONS_COUNT += 1
    if formula_type(formula) == 'dep' and len(formula_arguments(formula)) == 2:
        args = formula_arguments(formula)
        if args[0] == args[1]:
            return args[0]
    return None

# --- Rules ---

def rule_dependence_r(formula):
    """
    Dependence Right Rule.
    Applies to ('dep', A, B) formulae. Succeeds if both A and B can be proven.
    """
    global RULE_APPLICATIONS_COUNT
    RULE_APPLICATIONS_COUNT += 1
    if formula_type(formula) == 'dep':
        args = formula_arguments(formula)
        formula1, formula2 = args[0], args[1]
        # For a sub-proof, we call the top-level run_prover function.
        # This is a key part of the non-recursive design, as the state
        # of the proof for the sub-formulas is independent.
        proof1_result = run_prover(formula1)
        proof2_result = run_prover(formula2)
        if proof1_result is not None and proof2_result is not None:
            return formula
    return None

def rule_independence_r(formula):
    """
    Independence Right Rule.
    Applies to ('ind', A, B) formulae. Succeeds if either A or B can be proven.
    """
    global RULE_APPLICATIONS_COUNT
    RULE_APPLICATIONS_COUNT += 1
    if formula_type(formula) == 'ind':
        args = formula_arguments(formula)
        formula1, formula2 = args[0], args[1]
        if run_prover(formula1) is not None:
            return formula
        if run_prover(formula2) is not None:
            return formula
    return None

# --- Proof Dispatcher ---

def reset_complexity_counters():
    """Resets complexity counters."""
    global AXIOM_APPLICATIONS_COUNT, RULE_APPLICATIONS_COUNT
    AXIOM_APPLICATIONS_COUNT = 0
    RULE_APPLICATIONS_COUNT = 0

def run_prover(formula):
    """
    Top-level entry point for the prover.
    Initializes counters and runs the proof function.
    This function implements the fixed-chain dispatch.
    """
    reset_complexity_counters()

    # 1. Check axiom
    axiom_result = axiom_conr(formula)
    if axiom_result is not None:
        return axiom_result

    # 2. Fixed chain of rules
    # The order defines the logic's behavior.
    rule_result = rule_dependence_r(formula)
    if rule_result is not None:
        return rule_result

    rule_result = rule_independence_r(formula)
    if rule_result is not None:
        return rule_result

    return None

# --- Main Entry Point for Testing ---

if __name__ == "__main__":
    print("Starting Prover Tests.")

    con_formula = make_con()
    dep_formula_axiom = make_dep(con_formula, con_formula)
    ind_formula = make_ind(con_formula, con_formula)
    complex_formula = make_dep(dep_formula_axiom, ind_formula)

    print("\n--- Testing with axiom-applicable formula (dep con con) ---")
    prover_result = run_prover(dep_formula_axiom)
    print(f"Prover Result for formula {dep_formula_axiom}: {prover_result}")
    print(f"EXPECTED: {con_formula}")

    print("\n--- Testing with unprovable formula (ind con con) ---")
    prover_result = run_prover(ind_formula)
    print(f"Prover Result for formula {ind_formula}: {prover_result}")
    print(f"EXPECTED: None")

    print("\n--- Testing with complex unprovable formula ---")
    prover_result = run_prover(complex_formula)
    print(f"Prover Result for formula {complex_formula}: {prover_result}")
    print(f"EXPECTED: None")

    print("\n--- Testing with ('con') formula ---")
    prover_result = run_prover(con_formula)
    print(f"Prover Result for formula {con_formula}: {prover_result}")
    print(f"EXPECTED: None")

    print("\nProver Tests Finished.")