"""
Executable Witness for a Proposition in Skolem Arithmetic.

This script demonstrates the Curry-Howard correspondence for a simple,
decidable theory. The executable witness for a proposition is a function
that computationally demonstrates the proposition's truth.
"""

def prove_skolem_proposition():
    """
    This function is the executable witness for the proposition:
    exists x such that x = S(S(0)) where S is the successor function.

    Its successful execution and return of a valid certificate constitutes a proof.
    """
    # In Skolem Arithmetic, we can constructively find the witness.
    witness_x = "S(S(0))" # Representing the number 2

    # The proof is the construction itself.
    proof_certificate = {
        "logic_system": "Skolem Arithmetic",
        "proposition": "exists x such that x = S(S(0))",
        "proven": True,
        "witness_found": True,
        "value": witness_x,
        "proof_summary": f"The value x={witness_x} satisfies the proposition."
    }
    return proof_certificate

if __name__ == "__main__":
    print("--- Constructing Executable Witness for Skolem Arithmetic ---")
    certificate = prove_skolem_proposition()
    print(certificate)
