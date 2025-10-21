import enum


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

    def __init__(
        self,
        value: ParaconsistentTruth = ParaconsistentTruth.NEITHER,
        concrete_value=None,
    ):
        self.value = value
        self.concrete_value = concrete_value  # For non-boolean values

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
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method for {node}")

    def visit_Int(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, node.value)

    def visit_String(self, node):
        return ParaconsistentState(ParaconsistentTruth.TRUE, node.value)

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

    def visit_Negation(self, node):
        val = self.visit(node.formula)
        # Swaps True and False in the truth value set
        new_value = {not v for v in val.value.value}

        if new_value == {True, False}:
            truth_value = ParaconsistentTruth.BOTH
        elif new_value == {True}:
            truth_value = ParaconsistentTruth.TRUE
        elif new_value == {False}:
            truth_value = ParaconsistentTruth.FALSE
        else:  # NEITHER
            truth_value = ParaconsistentTruth.NEITHER

        return ParaconsistentState(truth_value, val.concrete_value)

    def visit_Consistency(self, node):
        val = self.visit(node.formula)
        # A formula is consistent if it is not BOTH.
        is_consistent = val.value != ParaconsistentTruth.BOTH
        return ParaconsistentState(
            ParaconsistentTruth.TRUE if is_consistent else ParaconsistentTruth.FALSE
        )

    def visit_Completeness(self, node):
        val = self.visit(node.formula)
        # A formula is complete (determined) if it is not NEITHER.
        is_complete = val.value != ParaconsistentTruth.NEITHER
        return ParaconsistentState(
            ParaconsistentTruth.TRUE if is_complete else ParaconsistentTruth.FALSE
        )

    def visit_CoNegation(self, node):
        val = self.visit(node.formula)
        # Swaps True and False in the truth value set, similar to Negation
        new_value = {not v for v in val.value.value}

        if new_value == {True, False}:
            truth_value = ParaconsistentTruth.BOTH
        elif new_value == {True}:
            truth_value = ParaconsistentTruth.TRUE
        elif new_value == {False}:
            truth_value = ParaconsistentTruth.FALSE
        else:  # NEITHER
            truth_value = ParaconsistentTruth.NEITHER

        return ParaconsistentState(truth_value, val.concrete_value)

    def visit_Undeterminedness(self, node):
        val = self.visit(node.formula)
        # A formula is undetermined if it is not BOTH (dual of consistency)
        # This is equivalent to completeness in the FDE model.
        is_undetermined = val.value != ParaconsistentTruth.BOTH
        return ParaconsistentState(
            ParaconsistentTruth.TRUE if is_undetermined else ParaconsistentTruth.FALSE
        )

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

    def visit_Atom(self, node):
        if node.name in self.environment:
            return self.environment[node.name]
        else:
            # Unbound variables are NEITHER
            return ParaconsistentState(ParaconsistentTruth.NEITHER)

    def visit_Inl(self, node):
        return ParaconsistentState(
            ParaconsistentTruth.TRUE, {"tag": "inl", "value": self.visit(node.e)}
        )

    def visit_Inr(self, node):
        return ParaconsistentState(
            ParaconsistentTruth.TRUE, {"tag": "inr", "value": self.visit(node.e)}
        )

    def visit_Case(self, node):
        val_to_match = self.visit(node.e)

        if val_to_match.is_true() and not val_to_match.is_false():  # TRUE
            if val_to_match.concrete_value["tag"] == "inl":
                self.environment[node.v1.name] = val_to_match.concrete_value["value"]
                return self.visit(node.e1)
            else:  # inr
                self.environment[node.v2.name] = val_to_match.concrete_value["value"]
                return self.visit(node.e2)

        elif val_to_match.is_false() and not val_to_match.is_true():  # FALSE
            # If the value is strictly false, the case analysis fails.
            # This represents a logical contradiction in the program.
            return ParaconsistentState(ParaconsistentTruth.FALSE)

        elif val_to_match.is_true() and val_to_match.is_false():  # BOTH
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

        else:  # NEITHER
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
