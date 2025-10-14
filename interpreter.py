import collections

# --- Data Structures for Propositions ---

class Prop:
    """Base class for propositions."""
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((self.__class__.__name__, frozenset(self.__dict__.items())))

class Atom(Prop):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class Neg(Prop):
    def __init__(self, prop):
        self.prop = prop
    def __repr__(self):
        return f"{self.prop}⊥"

class With(Prop): # Additive Conjunction: A & B
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} & {self.right})"

class Plus(Prop): # Additive Disjunction: A ⊕ B
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} ⊕ {self.right})"

class Top(Prop): # Unit of &
    def __repr__(self):
        return "⊤"

class Zero(Prop): # Unit of ⊕
    def __repr__(self):
        return "0"

# --- De Morgan Negation Helper ---

def negate(prop):
    """Applies negation using De Morgan's laws."""
    if isinstance(prop, Neg):
        return prop.prop
    if isinstance(prop, Atom):
        return Neg(prop)
    if isinstance(prop, With):
        return Plus(negate(prop.left), negate(prop.right))
    if isinstance(prop, Plus):
        return With(negate(prop.left), negate(prop.right))
    if isinstance(prop, Top):
        return Zero()
    if isinstance(prop, Zero):
        return Top()
    if isinstance(prop, Neg): # double negation
        return prop.prop
    return Neg(prop)


# --- The Proof Searcher ---

# Use a cache to handle cycles and repeated proofs
proof_cache = {}

def prove(gamma, delta, depth=0):
    """
    Attempts to find a proof for the sequent Γ ⊢ Δ.
    gamma and delta are tuples of propositions.
    """
    sequent = (gamma, delta)
    if sequent in proof_cache:
        return proof_cache[sequent]

    indent = "  " * depth
    # print(f"{indent}Trying: {list(gamma)} ⊢ {list(delta)}") # Uncomment for debugging

    # Axiom Rule: A ⊢ A
    if len(gamma) == 1 and len(delta) == 1 and gamma[0] == delta[0]:
        # print(f"{indent}Axiom: {gamma[0]} ⊢ {delta[0]}")
        proof_cache[sequent] = True
        return True

    # --- Right Rules ---
    if delta:
        last_prop = delta[-1]
        rest_delta = delta[:-1]

        # (&R)
        if isinstance(last_prop, With):
            if prove(gamma, (*rest_delta, last_prop.left), depth + 1) and \
               prove(gamma, (*rest_delta, last_prop.right), depth + 1):
                proof_cache[sequent] = True
                return True

        # (⊕R₁)
        if isinstance(last_prop, Plus):
            if prove(gamma, (*rest_delta, last_prop.left), depth + 1):
                proof_cache[sequent] = True
                return True
        # (⊕R₂)
        if isinstance(last_prop, Plus):
            if prove(gamma, (*rest_delta, last_prop.right), depth + 1):
                proof_cache[sequent] = True
                return True

        # (⊤R)
        if isinstance(last_prop, Top):
            proof_cache[sequent] = True
            return True

        # (⊥R)
        if isinstance(last_prop, Neg):
            if prove((last_prop.prop, *gamma), rest_delta, depth + 1):
                proof_cache[sequent] = True
                return True


    # --- Left Rules ---
    if gamma:
        first_prop = gamma[0]
        rest_gamma = gamma[1:]

        # (&L₁)
        if isinstance(first_prop, With):
            if prove((first_prop.left, *rest_gamma), delta, depth + 1):
                proof_cache[sequent] = True
                return True
        # (&L₂)
        if isinstance(first_prop, With):
             if prove((first_prop.right, *rest_gamma), delta, depth + 1):
                proof_cache[sequent] = True
                return True

        # (⊕L)
        if isinstance(first_prop, Plus):
            if prove((first_prop.left, *rest_gamma), delta, depth + 1) and \
               prove((first_prop.right, *rest_gamma), delta, depth + 1):
                proof_cache[sequent] = True
                return True

        # (0L)
        if isinstance(first_prop, Zero):
            proof_cache[sequent] = True
            return True

        # (⊥L)
        if isinstance(first_prop, Neg):
            if prove(rest_gamma, (first_prop.prop, *delta), depth + 1):
                proof_cache[sequent] = True
                return True

    # If no rule applies, the sequent is unprovable
    proof_cache[sequent] = False
    # print(f"{indent}Failed: {list(gamma)} ⊢ {list(delta)}")
    return False

# --- Simple Parser and Main Execution ---
def parse_prop(s: str):
    """A simple parser for our propositional language."""
    s = s.strip()

    # Handle parenthesized expressions
    if s.startswith('(') and s.endswith(')'):
        s = s[1:-1].strip()

    # Find the main connective by scanning from right to left
    balance = 0
    for i in range(len(s) - 1, -1, -1):
        char = s[i]
        if char == ')':
            balance += 1
        elif char == '(':
            balance -= 1
        elif balance == 0 and char in ['&', '⊕']:
            left = parse_prop(s[:i])
            right = parse_prop(s[i+1:])
            if char == '&':
                return With(left, right)
            else: # char == '⊕'
                return Plus(left, right)

    # Handle negation, which has the highest precedence after parentheses
    if s.endswith('⊥'):
        # This can be tricky if the part before it is parenthesized, e.g. (A&B)⊥
        base = s[:-1].strip()
        return negate(parse_prop(base))

    # Handle atomic propositions and units
    if s == '⊤':
        return Top()
    if s == '0':
        return Zero()
    if s.isalnum():
        return Atom(s)

    raise ValueError(f"Could not parse proposition: '{s}'")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # If a filename is provided, read from it
        try:
            with open(sys.argv[1], 'r') as f:
                program_str = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found.")
            sys.exit(1)
    else:
        # Default test cases
        print("Running internal test cases...")

        # Test 1: A ⊢ A (Axiom)
        a = Atom("A")
        print(f"\nTesting: {a} ⊢ {a}")
        result = prove((a,), (a,))
        print(f"Result: {'Provable' if result else 'Not Provable'} (Expected: Provable)")

        # Test 2: ⊢ A ⊕ A⊥ (Law of Excluded Middle - should fail)
        a_plus_a_perp = Plus(Atom("A"), Neg(Atom("A")))
        print(f"\nTesting: ⊢ {a_plus_a_perp}")
        proof_cache.clear()
        result = prove((), (a_plus_a_perp,))
        print(f"Result: {'Provable' if result else 'Not Provable'} (Expected: Not Provable)")

        # Test 3: A, A⊥ ⊢ (Explosion - should fail for arbitrary B)
        a = Atom("A")
        a_perp = Neg(Atom("A"))
        b = Atom("B")
        print(f"\nTesting: {a}, {a_perp} ⊢ {b}")
        proof_cache.clear()
        result = prove((a, a_perp), (b,))
        print(f"Result: {'Provable' if result else 'Not Provable'} (Expected: Not Provable)")

        # Test 4: A & B ⊢ A
        a_and_b = With(Atom("A"), Atom("B"))
        print(f"\nTesting: {a_and_b} ⊢ {Atom('A')}")
        proof_cache.clear()
        result = prove((a_and_b, ), (Atom("A"),))
        print(f"Result: {'Provable' if result else 'Not Provable'} (Expected: Provable)")

        # Test 5: A ⊢ A & A
        print(f"\nTesting: {Atom('A')} ⊢ {With(Atom('A'), Atom('A'))}")
        proof_cache.clear()
        result = prove((Atom("A"), ), (With(Atom("A"), Atom("A")),))
        print(f"Result: {'Provable' if result else 'Not Provable'} (Expected: Provable)")

        sys.exit(0)

    # --- Run program from file ---
    print(f"Attempting to prove: ⊢ {program_str}")
    try:
        prop = parse_prop(program_str)
        proof_cache.clear()
        is_provable = prove((), (prop,))

        if is_provable:
            print("\nProvable.")
        else:
            print("\nNot Provable.")
    except Exception as e:
        print(f"An error occurred during parsing or proving: {e}")
        print("Note: The parser is very basic. Ensure syntax is correct, e.g., '(A & B)'.")