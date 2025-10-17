import enum
from lfi_ill.ast import *

class ParaconsistentTruth(enum.Enum):
    """
    Represents the four truth values in a first-degree entailment logic (FDE).
    """
    FALSE = {False}
    TRUE = {True}
    BOTH = {True, False}
    NEITHER = set()

class Interpreter:
    def __init__(self, environment=None):
        if environment is None:
            self.environment = {}
        else:
            self.environment = environment

    def eval(self, node, env=None):
        if env is None:
            env = self.environment

        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, env):
        raise Exception(f'No visit_{type(node).__name__} method for {node}')

    def visit_Atom(self, node, env):
        return env.get(node.name, ParaconsistentTruth.TRUE)

    def visit_Tensor(self, node, env):
        left = self.eval(node.left, env)
        right = self.eval(node.right, env)
        # Tensor (logical AND) is TRUE only if both are TRUE.
        if left == ParaconsistentTruth.TRUE and right == ParaconsistentTruth.TRUE:
            return ParaconsistentTruth.TRUE
        return ParaconsistentTruth.FALSE

    def visit_Par(self, node, env):
        left = self.eval(node.left, env)
        right = self.eval(node.right, env)
        # Par (logical OR) is TRUE if at least one is TRUE.
        if left == ParaconsistentTruth.TRUE or right == ParaconsistentTruth.TRUE:
            return ParaconsistentTruth.TRUE
        return ParaconsistentTruth.FALSE

    def visit_Plus(self, node, env):
        # For Plus (internal choice), we can non-deterministically choose one.
        # For now, we'll just evaluate the left side.
        return self.eval(node.left, env)

    def visit_With(self, node, env):
        # For With (external choice), both must be valid.
        # We'll evaluate both and if they are the same, that's the result.
        left = self.eval(node.left, env)
        right = self.eval(node.right, env)
        if left == right:
            return left
        return ParaconsistentTruth.NEITHER # Or some other combination logic

    def visit_OfCourse(self, node, env):
        # !A means A can be used multiple times.
        # In this interpreter, this means we can evaluate it in an empty environment.
        return self.eval(node.formula, {})

    def visit_WhyNot(self, node, env):
        # ?A means A is a resource that can be discarded.
        # For now, we just evaluate the formula.
        return self.eval(node.formula, env)

    def visit_Section(self, node, env):
        # §A is for polynomial time computation.
        # This is a complex topic, for now we will just evaluate the formula.
        return self.eval(node.formula, env)

    def visit_Negation(self, node, env):
        val = self.eval(node.formula, env)
        if val == ParaconsistentTruth.TRUE:
            return ParaconsistentTruth.FALSE
        elif val == ParaconsistentTruth.FALSE:
            return ParaconsistentTruth.TRUE
        elif val == ParaconsistentTruth.BOTH:
            return ParaconsistentTruth.BOTH
        else: # NEITHER
            return ParaconsistentTruth.NEITHER

    def visit_Consistency(self, node, env):
        val = self.eval(node.formula, env)
        if val == ParaconsistentTruth.TRUE or val == ParaconsistentTruth.FALSE:
            return ParaconsistentTruth.TRUE
        elif val == ParaconsistentTruth.BOTH:
            return ParaconsistentTruth.FALSE
        else: # NEITHER
            return ParaconsistentTruth.NEITHER

    def visit_Paracomplete(self, node, env):
        val = self.eval(node.formula, env)
        if val == ParaconsistentTruth.TRUE or val == ParaconsistentTruth.FALSE:
            return ParaconsistentTruth.TRUE
        elif val == ParaconsistentTruth.NEITHER:
            return ParaconsistentTruth.FALSE
        else: # BOTH
            return ParaconsistentTruth.BOTH

    def visit_One(self, node, env):
        return ParaconsistentTruth.TRUE

    def visit_Bottom(self, node, env):
        return ParaconsistentTruth.FALSE

    def visit_Zero(self, node, env):
        return ParaconsistentTruth.FALSE

    def visit_Top(self, node, env):
        return ParaconsistentTruth.TRUE