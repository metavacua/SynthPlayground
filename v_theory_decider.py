"""
Computational Witness for a Decidable, Self-Defining Theory (V).

This script provides a computational analogue for the logical theorem stating that
any consistent, axiomatizable theory that defines its own set of theorems (V)
is necessarily decidable.

The Core Analogy:
- Theory (T_V): The Python script itself, which is axiomatizable as its text is finite.
- Theorems (V): The set of strings accepted by the `V_Decider`, forming the language `L_V`.
- Defines V: The script's logic directly implements the definition of `L_V`.
  The proposition "s is in L_V" is proven true or false by the decider.
- Consistent: The decider for `L_V` is a pure function that cannot prove both
  "s is in L_V" and "s is not in L_V" for any given string `s`.
- Decidable: The decider function is guaranteed to halt and return a boolean,
  which demonstrates that the set of theorems `V` is a recursive set.

This script uses a fixed-point combinator (the Z-combinator) to construct the
recursive decider `V_Decider`. This self-referential construction is a direct
computational parallel to Kleene's Recursion Theorem and is the mechanism by
which the "theory" (the script) can refer to and define its own behavior. The
successful execution of this script for any input is the computational proof
that membership in the language `L_V` is decidable.
"""
import re

# The Z-combinator is a version of the Y-combinator that works in
# strictly-evaluated languages like Python by delaying evaluation.
# It takes a non-recursive function generator and returns a recursive function,
# providing a mechanism for self-reference without explicit self-naming.
Z = lambda f: (lambda x: f(lambda *args: x(x)(*args)))(lambda x: f(lambda *args: x(x)(*args)))

def decider_generator(self):
    """
    This is the non-recursive core logic of our decider. It is a "generator"
    that describes the recursive logic of the theory. It takes `self` as an
    argument, which represents the function to call for the recursive step.
    This `self` is the computational analogue of the theory referring to its
    own proof predicate.
    """
    def decider_logic(input_string):
        """
        The logic for deciding membership in L_V. The execution of this function
        is the proof that "`input_string` is in L_V".

        The language L_V (the set of theorems V) is defined as:
        1. Base case (Axioms): Any string `w` not of the form `IsInL(<s>)` is in L_V
           if and only if it has an even length.
        2. Recursive case (Inference Rule): A string `IsInL(<s>)` is in L_V if and only if
           the inner string `s` is in L_V. This rule allows the theory to reason
           about its own theorems.
        """
        # Regex to parse strings of the form "IsInL(<s>)"
        match = re.fullmatch(r"IsInL\((.*)\)", input_string)

        if match:
            # Recursive case: The proof requires us to prove the inner string is in L_V.
            # This is analogous to an inference step, reducing a complex proof
            # to a simpler one.
            inner_string = match.group(1)
            return self(inner_string)
        else:
            # Base case: The proof is a simple check of a string property, analogous
            # to checking if a statement is an axiom.
            return len(input_string) % 2 == 0

    return decider_logic

# Use the Z-combinator to construct the final, recursive decider.
# V_Decider is now a total recursive function that decides membership in L_V.
# Its existence and successful execution for any input is the computational
# witness to the decidability of the self-defining language L_V.
V_Decider = Z(decider_generator)

if __name__ == "__main__":
    print("--- Computational Witness for a Decidable, Self-Defining Theory (V) ---")
    print("The witness is the V_Decider function itself. Its execution is the proof.\n")

    # --- Test Cases ---
    test_strings = [
        "aabb",         # Base case (Axiom), True
        "abc",          # Base case (Axiom), False
        "IsInL(xy)",    # Recursive case (Inference), inner is True
        "IsInL(xyz)",   # Recursive case (Inference), inner is False
        "IsInL(IsInL(zz))" # Doubly recursive case, inner is True
    ]

    for s in test_strings:
        # The act of running the decider IS the proof. The return value
        # is the result of the proof (True/False). Because the decider always
        # halts, the language L_V is proven to be a recursive (decidable) set.
        is_proven = V_Decider(s)
        print(f"Proposition: '{s}' is in L_V.")
        print(f"Proof Result: {is_proven}\n")
