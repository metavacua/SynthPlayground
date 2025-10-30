"""
Executable Witness for a Proposition in L_V (Self-Referential Language).

This script demonstrates the most direct application of the Curry-Howard
correspondence. The witness for the proposition "`w` is in `L_V`" is the
decider program itself. Its existence is guaranteed by Kleene's Recursion
Theorem, and it can be implemented computationally using a fixed-point
combinator like the Y-combinator (or Z-combinator for strict languages).
"""
import re

# The Z-combinator is a version of the Y-combinator that works in
# strictly-evaluated languages like Python by delaying evaluation.
# It takes a non-recursive function generator and returns a recursive function.
Z = lambda f: (lambda x: f(lambda *args: x(x)(*args)))(lambda x: f(lambda *args: x(x)(*args)))

def decider_generator(self):
    """
    This is the non-recursive core logic of our decider.
    It's a "generator" that describes the recursive logic. It takes `self`
    as an argument, which will be the function to call for the recursive step.
    """
    def decider_logic(input_string):
        """
        The logic for deciding membership in L_V. The proposition being
        proven is "`input_string` is in L_V". This function's execution
        is the proof.

        The language L_V is defined as:
        1. Base case: Any string `w` not of the form `IsInL(<s>)` is in L_V
           if and only if it has an even length.
        2. Recursive case: A string `IsInL(<s>)` is in L_V if and only if
           the inner string `s` is in L_V.
        """
        # Regex to parse strings of the form "IsInL(<s>)"
        match = re.fullmatch(r"IsInL\((.*)\)", input_string)

        if match:
            # Recursive case: The proof requires us to prove the inner string is in L_V.
            # We do this by recursively calling the decider on the inner string.
            inner_string = match.group(1)
            return self(inner_string)
        else:
            # Base case: The proof is a simple check of the string's property.
            return len(input_string) % 2 == 0

    return decider_logic

# Use the Z-combinator to construct the final, recursive decider.
# L_V_Decider is now a recursive function that can call itself without
# needing to be explicitly named within its own body.
L_V_Decider = Z(decider_generator)

if __name__ == "__main__":
    print("--- Constructing Executable Witness for L_V ---")
    print("The witness is the decider function itself. Its execution is the proof.\n")

    # --- Test Cases ---
    test_strings = [
        "aabb",         # Base case, True
        "abc",          # Base case, False
        "IsInL(xy)",    # Recursive case, inner is True
        "IsInL(xyz)",   # Recursive case, inner is False
        "IsInL(IsInL(zz))" # Doubly recursive case, inner is True
    ]

    for s in test_strings:
        # The act of running the function IS the proof. The return value
        # is the result of the proof.
        is_proven = L_V_Decider(s)
        print(f"Proposition: '{s}' is in L_V.")
        print(f"Proof Result: {is_proven}\n")
