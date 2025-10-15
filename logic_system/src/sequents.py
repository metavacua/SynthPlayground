from typing import Set
from .formulas import Formula

class Sequent:
    def __init__(self, antecedent: Set[Formula], succedent: Set[Formula]):
        self.antecedent = frozenset(antecedent)
        self.succedent = frozenset(succedent)

    def __repr__(self):
        ant_str = ", ".join(map(str, self.antecedent))
        suc_str = ", ".join(map(str, self.succedent))
        return f"{ant_str} ⊢ {suc_str}"

    def __eq__(self, other):
        return self.antecedent == other.antecedent and self.succedent == other.succedent

    def __hash__(self):
        return hash((self.antecedent, self.succedent))