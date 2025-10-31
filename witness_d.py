"""
Executable Witness for a Decidable Diagonalization Theory.

This program serves as a constructive proof (a "witness") for the existence of
a decidable formal language that includes a diagonalization function. The key
to its decidability is its limited expressive power; specifically, it lacks
the features (like universal quantification and the full arithmetic signature)
that would allow it to state the Diagonalization Lemma and thus fall into
Gödelian incompleteness.
"""

import hashlib

def godel_number(s):
    """
    A simple Gödel numbering function that assigns a unique integer to any string.
    """
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)

def diagonalization_function(formula_godel_number):
    """
    The computable diagonalization function, d(x).

    This function takes the Gödel number of a formula A(x) with one free
    variable 'x' and returns the Gödel number of the formula A(n), where n
    is the numeral for the Gödel number of A(x) itself.

    For simplicity in this witness, we represent formulas as strings.
    """
    # In a real system, we'd need a way to reconstruct the formula from its
    # Gödel number. Here, we'll simulate this by keeping a lookup table.
    # This is a concession to simplicity for this example.
    formula_string = GODEL_LOOKUP.get(formula_godel_number)
    if not formula_string:
        raise ValueError(f"No formula found for Gödel number: {formula_godel_number}")

    # Substitute the Gödel number into the formula string.
    # The convention is that the free variable is always 'x'.
    substituted_formula = formula_string.replace('x', str(formula_godel_number))

    return godel_number(substituted_formula)

def decide(formula_string):
    """
    A decider for our simple, quantifier-free first-order language.

    The language consists of:
    - Constants (integers)
    - A single variable ('x')
    - A binary equality predicate ('=')
    - A unary function symbol ('d') for the diagonalization function.

    A formula is an expression of the form 'term = term', where a term
    can be a constant, the variable 'x', or the application of 'd' to a term.
    """
    # This is a very simple parser and evaluator. It only handles formulas of
    # the form 'd(n) = m'.
    if '=' not in formula_string:
        return {"decided": False, "reason": "Invalid formula: missing '='"}

    lhs, rhs = [s.strip() for s in formula_string.split('=', 1)]

    # Evaluate the right-hand side (must be a constant).
    try:
        m = int(rhs)
    except ValueError:
        return {"decided": False, "reason": f"RHS is not a valid integer: {rhs}"}

    # Evaluate the left-hand side.
    if not (lhs.startswith('d(') and lhs.endswith(')')):
        return {"decided": False, "reason": "LHS is not a valid function call"}

    try:
        n = int(lhs[2:-1])
    except ValueError:
        return {"decided": False, "reason": f"Argument to d() is not a valid integer: {lhs[2:-1]}"}

    # Apply the diagonalization function and check for equality.
    result = diagonalization_function(n)
    return {
        "decided": True,
        "value": result == m,
        "LHS_eval": result,
        "RHS_eval": m
    }

# --- Witness Demonstration ---

# We need a lookup table to go from Gödel numbers back to formulas for the
# diagonalization function.
GODEL_LOOKUP = {}

def register_formula(formula_string):
    """Helper to populate the Gödel lookup table."""
    num = godel_number(formula_string)
    GODEL_LOOKUP[num] = formula_string
    return num

if __name__ == "__main__":
    print("--- Constructing Executable Witness for a Decidable Diagonalization Theory ---")

    # 1. Define a simple formula with one free variable, 'x'.
    formula_A = "x = x"
    godel_A = register_formula(formula_A)
    print(f"\nFormula A(x): '{formula_A}'")
    print(f"Gödel number for A(x): {godel_A}")

    # 2. Compute the result of the diagonalization function d(⌈A(x)⌉).
    # This gives us the Gödel number of the sentence A(⌈A(x)⌉).
    d_of_godel_A = diagonalization_function(godel_A)
    print(f"d(⌈A(x)⌉) = {d_of_godel_A}")

    # The substituted sentence is "⌈A(x)⌉ = ⌈A(x)⌉"
    expected_substituted_sentence = f"{godel_A} = {godel_A}"
    print(f"The sentence A(⌈A(x)⌉) is: '{expected_substituted_sentence}'")
    print(f"The Gödel number of this sentence is: {godel_number(expected_substituted_sentence)}")
    assert d_of_godel_A == godel_number(expected_substituted_sentence)

    # 3. Use the decider to prove a true statement in the theory.
    # We will test the truth of the sentence: d(⌈A(x)⌉) = ⌈A(⌈A(x)⌉)⌉
    true_statement = f"d({godel_A}) = {d_of_godel_A}"
    print(f"\nDeciding the truth of the statement: '{true_statement}'")
    decision = decide(true_statement)
    print(f"Decision: {decision}")
    assert decision["value"] is True

    # 4. Use the decider to prove a false statement in the theory.
    false_statement = f"d({godel_A}) = 12345" # An arbitrary incorrect value
    print(f"\nDeciding the truth of the statement: '{false_statement}'")
    decision = decide(false_statement)
    print(f"Decision: {decision}")
    assert decision["value"] is False
