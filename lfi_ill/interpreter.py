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

class ParaconsistentState:
    """
    A variable whose truth value is modeled paraconsistently.
    """
    def __init__(self, value: ParaconsistentTruth = ParaconsistentTruth.NEITHER, concrete_value=None):
        self.value = value
        self.concrete_value = concrete_value # For non-boolean values

    def is_true(self) -> bool:
        return True in self.value.value

    def is_false(self) -> bool:
        return False in self.value.value

    def __repr__(self):
        return f"ParaconsistentState({self.value}, {self.concrete_value})"

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.environment = {}

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method for {node}')

    def visit_Int(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, node.value)

    def visit_String(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, node.value)

    def visit_Atom(self, node):
        # The semantics of linear negation on atoms (e.g., p^⊥) is not fully
        # specified in the research paper for an FDE-style evaluation.
        # This implementation provides a basic interpretation.
        if node.negated:
            if node.name == "True":
                return ParaconsistentState(ParaconsistentTruth.FALSE, False)
            elif node.name == "False":
                return ParaconsistentState(ParaconsistentTruth.TRUE, True)
            # For negated Both/Neither or other atoms, the semantics are
            # undefined. We'll treat them as NEITHER.
            else:
                return ParaconsistentState(ParaconsistentTruth.NEITHER, None)

        if node.name == "True":
            return ParaconsistentState(ParaconsistentTruth.TRUE, True)
        elif node.name == "False":
            return ParaconsistentState(ParaconsistentTruth.FALSE, False)
        elif node.name == "Both":
            return ParaconsistentState(ParaconsistentTruth.BOTH, None)
        elif node.name == "Neither":
            return ParaconsistentState(ParaconsistentTruth.NEITHER, None)

        # Fallback for other atoms, treat as NEITHER
        return ParaconsistentState(ParaconsistentTruth.NEITHER, node.name)

    def visit_Bool(self, node):
        if node.value == "Both":
            return ParaconsistentState(ParaconsistentTruth.BOTH)
        elif node.value == "Neither":
            return ParaconsistentState(ParaconsistentTruth.NEITHER)
        elif node.value:
            return ParaconsistentState(ParaconsistentTruth.TRUE)
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)

    def visit_WithPair(self, node):
        e1 = self.visit(node.e1)
        e2 = self.visit(node.e2)
        return ParaconsistentState(ParaconsistentTruth.TRUE, (e1, e2))

    def visit_Fst(self, node):
        pair = self.visit(node.e)
        if pair.is_true():
            return pair.concrete_value[0]
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)

    def visit_Snd(self, node):
        pair = self.visit(node.e)
        if pair.is_true():
            return pair.concrete_value[1]
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)

    def visit_Promotion(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, self.visit(node.e))

    def visit_Dereliction(self, node):
        promoted_val = self.visit(node.e1)
        if promoted_val.is_true():
            self.environment[node.v.name] = promoted_val.concrete_value
            return self.visit(node.e2)
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)

    def visit_Section(self, node):
        # Placeholder Implementation:
        # The § modality from Light Linear Logic has complex semantics related
        # to proof structure and complexity bounds, which are not captured in this
        # simple FDE-style evaluator. For now, we treat it as an identity
        # function to allow for syntactic compatibility with the formal grammar.
        return ParaconsistentState(ParaconsistentTruth.TRUE, self.visit(node.formula))

    def visit_Negation(self, node):
        val = self.visit(node.formula)
        negated_value = None
        if val.value == ParaconsistentTruth.TRUE:
            negated_value = ParaconsistentTruth.FALSE
        elif val.value == ParaconsistentTruth.FALSE:
            negated_value = ParaconsistentTruth.TRUE
        else:
            # BOTH and NEITHER remain unchanged under paraconsistent negation
            negated_value = val.value

        return ParaconsistentState(negated_value, val.concrete_value)

    def visit_Consistency(self, node):
        val = self.visit(node.formula)
        consistency_value = None
        concrete_result = None

        if val.value == ParaconsistentTruth.TRUE or val.value == ParaconsistentTruth.FALSE:
            # If the value is classically true or false, it's consistent.
            consistency_value = ParaconsistentTruth.TRUE
            concrete_result = True
        elif val.value == ParaconsistentTruth.BOTH:
            # If the value is BOTH, it's inconsistent.
            consistency_value = ParaconsistentTruth.FALSE
            concrete_result = False
        else: # NEITHER
            # If the value is NEITHER, its consistency is also NEITHER.
            consistency_value = ParaconsistentTruth.NEITHER
            concrete_result = None

        return ParaconsistentState(consistency_value, concrete_result)

    def visit_WhyNot(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, self.visit(node.e))

    def visit_LetWhyNot(self, node):
        why_not_val = self.visit(node.e1)
        if why_not_val.is_true():
            self.environment[node.v.name] = why_not_val.concrete_value
            return self.visit(node.e2)
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)

    def visit_Par(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, self.visit(node.e))

    def visit_LetPar(self, node):
        par_val = self.visit(node.e1)
        if par_val.is_true():
            self.environment[node.v.name] = par_val.concrete_value
            return self.visit(node.e2)
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)

    def visit_Fun(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, node)

    def visit_App(self, node):
        fun = self.visit(node.f)
        arg = self.visit(node.arg)
        if fun.is_true():
            fun_node = fun.concrete_value
            self.environment[fun_node.var.name] = arg
            return self.visit(fun_node.body)
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)

    def visit_Var(self, node):
        if node.name in self.environment:
            return self.environment[node.name]
        else:
            # Unbound variables are NEITHER
            return ParaconsistentState(ParaconsistentTruth.NEITHER)

    def visit_Inl(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, {"tag": "inl", "value": self.visit(node.e)})

    def visit_Inr(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, {"tag": "inr", "value": self.visit(node.e)})

    def visit_Case(self, node):
        val_to_match = self.visit(node.e)

        if val_to_match.is_true() and not val_to_match.is_false(): # TRUE
            if val_to_match.concrete_value["tag"] == "inl":
                self.environment[node.v1.name] = val_to_match.concrete_value["value"]
                return self.visit(node.e1)
            else: # inr
                self.environment[node.v2.name] = val_to_match.concrete_value["value"]
                return self.visit(node.e2)

        elif val_to_match.is_false() and not val_to_match.is_true(): # FALSE
            # If the value is strictly false, the case analysis fails.
            # This represents a logical contradiction in the program.
            return ParaconsistentState(ParaconsistentTruth.FALSE)

        elif val_to_match.is_true() and val_to_match.is_false(): # BOTH
            # If the value is BOTH, we must explore both paths.
            # This is the core of the paraconsistent evaluation.

            # Path 1: Assume inl
            self.environment[node.v1.name] = val_to_match.concrete_value["value"]
            res1 = self.visit(node.e1)

            # Path 2: Assume inr
            self.environment[node.v2.name] = val_to_match.concrete_value["value"]
            res2 = self.visit(node.e2)

            # Combine the results.
            # If the results are the same, the result is that result.
            # If they are different, the result is BOTH.
            if res1 == res2:
                return res1
            else:
                # This is a simplification. A more robust implementation
                # would combine the concrete values as well.
                return ParaconsistentState(ParaconsistentTruth.BOTH)

        else: # NEITHER
            # If the value is NEITHER, we cannot proceed.
            return ParaconsistentState(ParaconsistentTruth.NEITHER)

    def visit_TensorPair(self, node):
        e1 = self.visit(node.e1)
        e2 = self.visit(node.e2)
        return ParaconsistentState(ParaconsistentTruth.TRUE, (e1, e2))

    def visit_LetTensor(self, node):
        pair = self.visit(node.e1)
        if pair.is_true():
            self.environment[node.v1.name] = pair.concrete_value[0]
            self.environment[node.v2.name] = pair.concrete_value[1]
            return self.visit(node.e2)
        else:
            return ParaconsistentState(ParaconsistentTruth.FALSE)