import enum
from .ast import *

class Truth(enum.Enum):
    """
    Represents the four truth values in a First-Degree Entailment (FDE) logic,
    which is both paraconsistent and paracomplete. The values are based on the
    Belnap-Dunn logic, representing states of information:
    - TRUE: Told True only
    - FALSE: Told False only
    - BOTH: Told True and False (a glut, inconsistent)
    - NEITHER: Told nothing (a gap, incomplete)
    """
    FALSE = 0
    TRUE = 1
    BOTH = 2
    NEITHER = 3

class Interpreter:
    def __init__(self, environment=None):
        self.environment = environment if environment is not None else {}

    def _eval(self, node, env):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def eval(self, node):
        return self._eval(node, self.environment)

    def generic_visit(self, node, env):
        raise NotImplementedError(f'No visit_{type(node).__name__} method')

    # Basic Formulas
    def visit_Atom(self, node, env):
        # Atoms are looked up in the environment. If not found, it's NEITHER.
        # Linear negation A^bot is handled semantically by swapping TRUE/FALSE.
        val = env.get(node.name, Truth.NEITHER)
        if node.negated:
            if val == Truth.TRUE: return Truth.FALSE
            if val == Truth.FALSE: return Truth.TRUE
        return val

    # Multiplicative Connectives
    def visit_Tensor(self, node, env): # Multiplicative AND (fusion)
        l = self._eval(node.left, env)
        r = self._eval(node.right, env)
        if l == Truth.FALSE or r == Truth.FALSE: return Truth.FALSE
        if l == Truth.NEITHER or r == Truth.NEITHER: return Truth.NEITHER
        if l == Truth.BOTH or r == Truth.BOTH: return Truth.BOTH
        return Truth.TRUE

    def visit_Par(self, node, env): # Multiplicative OR (fission)
        l = self._eval(node.left, env)
        r = self._eval(node.right, env)
        if l == Truth.TRUE or r == Truth.TRUE: return Truth.TRUE
        if l == Truth.BOTH or r == Truth.BOTH: return Truth.BOTH
        if l == Truth.NEITHER or r == Truth.NEITHER: return Truth.NEITHER
        return Truth.FALSE

    # Additive Connectives
    def visit_With(self, node, env): # Additive AND (internal choice)
        l = self._eval(node.left, env)
        r = self._eval(node.right, env)
        if l == Truth.FALSE or r == Truth.FALSE: return Truth.FALSE
        if l == Truth.NEITHER and r == Truth.NEITHER: return Truth.NEITHER
        if l == Truth.NEITHER: return r
        if r == Truth.NEITHER: return l
        if l == Truth.BOTH or r == Truth.BOTH: return Truth.BOTH
        return Truth.TRUE

    def visit_Plus(self, node, env): # Additive OR (external choice)
        l = self._eval(node.left, env)
        r = self._eval(node.right, env)
        if l == Truth.TRUE or r == Truth.TRUE: return Truth.TRUE
        if l == Truth.BOTH and r == Truth.BOTH: return Truth.BOTH
        if l == Truth.BOTH: return r
        if r == Truth.BOTH: return l
        if l == Truth.NEITHER or r == Truth.NEITHER: return Truth.NEITHER
        return Truth.FALSE

    # Modal and Paraconsistent/Paracomplete Operators
    def visit_Negation(self, node, env): # Paraconsistent Negation (¬)
        val = self._eval(node.formula, env)
        if val == Truth.TRUE: return Truth.FALSE
        if val == Truth.FALSE: return Truth.TRUE
        return val # BOTH stays BOTH, NEITHER stays NEITHER

    def visit_Consistency(self, node, env): # Consistency Operator (∘)
        val = self._eval(node.formula, env)
        # A formula is consistent if it is not a glut (i.e., not BOTH).
        return Truth.TRUE if val != Truth.BOTH else Truth.FALSE

    def visit_Paracomplete(self, node, env): # Completeness/Determinedness Operator (~)
        val = self._eval(node.formula, env)
        # A formula is complete/determined if it is not a gap (i.e., not NEITHER).
        return Truth.TRUE if val != Truth.NEITHER else Truth.FALSE

    # Units
    def visit_One(self, node, env): # Unit for Tensor
        return Truth.TRUE
    def visit_Bottom(self, node, env): # Unit for Par
        return Truth.FALSE
    def visit_Zero(self, node, env): # Unit for Plus
        return Truth.FALSE
    def visit_Top(self, node, env): # Unit for With
        return Truth.TRUE

    # Light Logic Modalities (simplified interpretation)
    def visit_OfCourse(self, node, env): # !A
        # For evaluation, we treat this as just evaluating the inner formula.
        # A full proof-theoretic interpreter would handle resource duplication.
        return self._eval(node.formula, env)

    def visit_WhyNot(self, node, env): # ?A
        # Dually, we just evaluate the inner formula.
        return self._eval(node.formula, env)

    def visit_Section(self, node, env): # §A
        # The section modality is for complexity control, not truth-functional.
        # We pass through the evaluation.
        return self._eval(node.formula, env)