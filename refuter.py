"""
refuter.py

This module is a Python translation of the RefuterV0.lisp theorem refuter.
It implements a simple theorem refuter for a non-classical logic.

This system uses a non-recursive, fixed-chain dispatch architecture to
ensure termination, and is symmetric to the prover system.
"""

# --- Global Complexity Metrics ---
AXIOM_APPLICATIONS_COUNT = 0
RULE_APPLICATIONS_COUNT = 0

# --- Formula Representation ---

def make_incon():
    """Constructs an 'incon' formula."""
    return ('incon',)

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

def axiom_inconl(formula):
    """
    Refutation Axiom (axiom InconL).
    Refutes ('incon',) and ('ind', A, A).
    """
    global AXIOM_APPLICATIONS_COUNT
    AXIOM_APPLICATIONS_COUNT += 1
    if formula_type(formula) == 'incon':
        return formula
    if formula_type(formula) == 'ind' and len(formula_arguments(formula)) == 2:
        args = formula_arguments(formula)
        if args[0] == args[1]:
            return formula
    return None

# --- Rules ---

def rule_independence_l(formula):
    """
    Independence Left Rule.
    Applies to ('ind', A, B) formulae. Succeeds if either A or B can be refuted.
    """
    global RULE_APPLICATIONS_COUNT
    RULE_APPLICATIONS_COUNT += 1
    if formula_type(formula) == 'ind':
        args = formula_arguments(formula)
        formula1, formula2 = args[0], args[1]
        if run_refuter(formula1) is not None:
            return formula
        if run_refuter(formula2) is not None:
            return formula
    return None

def rule_dependence_l(formula):
    """
    Dependence Left Rule.
    Applies to ('dep', A, B) formulae. Succeeds if both A and B can be refuted.
    """
    global RULE_APPLICATIONS_COUNT
    RULE_APPLICATIONS_COUNT += 1
    if formula_type(formula) == 'dep':
        args = formula_arguments(formula)
        formula1, formula2 = args[0], args[1]
        if run_refuter(formula1) is not None and run_refuter(formula2) is not None:
            return formula
    return None

# --- Refutation Dispatcher ---

def reset_complexity_counters():
    """Resets complexity counters."""
    global AXIOM_APPLICATIONS_COUNT, RULE_APPLICATIONS_COUNT
    AXIOM_APPLICATIONS_COUNT = 0
    RULE_APPLICATIONS_COUNT = 0

def run_refuter(formula):
    """
    Top-level entry point for the refuter.
    Initializes counters and runs the refutation function.
    This function implements the fixed-chain dispatch.
    """
    reset_complexity_counters()

    # 1. Check axiom
    axiom_result = axiom_inconl(formula)
    if axiom_result is not None:
        return axiom_result

    # 2. Fixed chain of rules
    rule_result = rule_independence_l(formula)
    if rule_result is not None:
        return rule_result

    rule_result = rule_dependence_l(formula)
    if rule_result is not None:
        return rule_result

    return None

# --- Main Entry Point for Testing ---

if __name__ == "__main__":
    print("Starting Refuter Tests.")

    incon_formula = make_incon()
    dep_formula = make_dep(incon_formula, incon_formula)
    ind_formula = make_ind(incon_formula, incon_formula)
    self_ind_formula = make_ind(incon_formula, incon_formula)
    complex_formula = make_ind(dep_formula, ind_formula)

    print("\n--- Testing with base refutable formula (incon) ---")
    refuter_result = run_refuter(incon_formula)
    print(f"Refuter Result for formula {incon_formula}: {refuter_result}")
    print(f"EXPECTED: {incon_formula}")

    print("\n--- Testing with (dep incon incon) formula ---")
    refuter_result = run_refuter(dep_formula)
    print(f"Refuter Result for formula {dep_formula}: {refuter_result}")
    print(f"EXPECTED: {dep_formula}")

    print("\n--- Testing with (ind incon incon) formula ---")
    refuter_result = run_refuter(ind_formula)
    print(f"Refuter Result for formula {ind_formula}: {refuter_result}")
    print(f"EXPECTED: {ind_formula}")

    print("\n--- Testing with axiom-applicable formula (ind incon incon) ---")
    refuter_result = run_refuter(self_ind_formula)
    print(f"Refuter Result for formula {self_ind_formula}: {refuter_result}")
    print(f"EXPECTED: {self_ind_formula}")

    print("\n--- Testing with complex formula ---")
    refuter_result = run_refuter(complex_formula)
    print(f"Refuter Result for formula {complex_formula}: {refuter_result}")
    print(f"EXPECTED: {complex_formula}")

    print("\nRefuter Tests Finished.")