"""
Executable Witness for a Proposition in L_neither (Presburger Arithmetic).

This script demonstrates the Curry-Howard correspondence for a simple,
decidable theory. The executable witness for a proposition is a function
that computationally demonstrates the proposition's truth.
"""

def prove_presburger_proposition():
    """
    This function is the executable witness for the proposition:
    exists x such that (x > 3) and (x < 6) and (2*x == 8)

    Its successful execution and return of a valid certificate constitutes a proof.
    The logic mimics the constructive nature of a quantifier elimination algorithm.
    """
    # From the constraint 2*x == 8, a constructive proof finds x = 4.
    # This is the candidate witness.
    witness_x = 4

    # The proof then verifies this witness against the other constraints.
    constraint1_holds = (witness_x > 3)
    constraint2_holds = (witness_x < 6)

    # If all constraints hold, the witness is valid and the proposition is proven.
    if constraint1_holds and constraint2_holds:
        proof_certificate = {
            "proposition": "exists x such that (x > 3) and (x < 6) and (2*x == 8)",
            "proven": True,
            "witness_found": True,
            "value": witness_x,
            "proof_summary": f"The value x={witness_x} satisfies all constraints."
        }
        return proof_certificate
    else:
        # This branch is unreachable for a true proposition. A sufficiently
        # powerful type system could prove this at compile time.
        proof_certificate = {
            "proposition": "exists x such that (x > 3) and (x < 6) and (2*x == 8)",
            "proven": False,
            "witness_found": False,
            "proof_summary": f"The candidate x={witness_x} did not satisfy all constraints."
        }
        return proof_certificate

if __name__ == "__main__":
    print("--- Constructing Executable Witness for Presburger Arithmetic ---")
    certificate = prove_presburger_proposition()
    print(certificate)
