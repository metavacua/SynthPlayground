# --- Data Structures for Propositions ---

class Prop:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
    def __hash__(self):
        return hash((self.__class__.__name__, frozenset(self.__dict__.items())))
    def __repr__(self):
        return self.__class__.__name__

class Atom(Prop):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class With(Prop):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} & {self.right})"

class Plus(Prop):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} ⊕ {self.right})"

class Top(Atom):
    def __init__(self):
        super().__init__("⊤")

class Zero(Atom):
    def __init__(self):
        super().__init__("0")

# --- The Core Logic: Recursive Proof Search ---

proof_cache = {}

def prove(gamma, delta, depth=0):
    """
    Performs a full proof search for structural equivalence in a non-commutative logic
    without weakening, contraction, or exchange.
    gamma and delta are tuples of propositions.
    """
    sequent = (gamma, delta)
    if sequent in proof_cache:
        return proof_cache[sequent]

    # Axiom: An identical sequent is proven.
    if gamma == delta:
        proof_cache[sequent] = True
        return True

    # --- Left Rules ---
    for i, prop in enumerate(gamma):
        prefix, suffix = gamma[:i], gamma[i+1:]

        if isinstance(prop, With):
            # To prove Γ, A&B, Δ ⊢ Θ, we can prove Γ, A, Δ ⊢ Θ or Γ, B, Δ ⊢ Θ
            if prove(prefix + (prop.left,) + suffix, delta, depth + 1):
                proof_cache[sequent] = True
                return True
            if prove(prefix + (prop.right,) + suffix, delta, depth + 1):
                proof_cache[sequent] = True
                return True

        if isinstance(prop, Plus):
            # To prove Γ, A⊕B, Δ ⊢ Θ, we must prove both Γ, A, Δ ⊢ Θ and Γ, B, Δ ⊢ Θ
            if prove(prefix + (prop.left,) + suffix, delta, depth + 1) and \
               prove(prefix + (prop.right,) + suffix, delta, depth + 1):
                proof_cache[sequent] = True
                return True

        if isinstance(prop, Zero):
            # A sequent with 0 on the left is provable.
            proof_cache[sequent] = True
            return True

    # --- Right Rules ---
    for i, prop in enumerate(delta):
        prefix, suffix = delta[:i], delta[i+1:]

        if isinstance(prop, With):
            # To prove Γ ⊢ Δ, A&B, Θ, we must prove both Γ ⊢ Δ, A, Θ and Γ ⊢ Δ, B, Θ
            if prove(gamma, prefix + (prop.left,) + suffix, depth + 1) and \
               prove(gamma, prefix + (prop.right,) + suffix, depth + 1):
                proof_cache[sequent] = True
                return True

        if isinstance(prop, Plus):
            # To prove Γ ⊢ Δ, A⊕B, Θ, we can prove Γ ⊢ Δ, A, Θ or Γ ⊢ Δ, B, Θ
            if prove(gamma, prefix + (prop.left,) + suffix, depth + 1):
                proof_cache[sequent] = True
                return True
            if prove(gamma, prefix + (prop.right,) + suffix, depth + 1):
                proof_cache[sequent] = True
                return True

        if isinstance(prop, Top):
            # A sequent with ⊤ on the right is provable.
            proof_cache[sequent] = True
            return True

    proof_cache[sequent] = False
    return False