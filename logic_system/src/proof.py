from typing import List, Optional
from .sequents import Sequent

class Rule:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

class ProofTree:
    def __init__(self, conclusion: Sequent, rule: Rule, premises: Optional[List['ProofTree']] = None):
        self.conclusion = conclusion
        self.rule = rule
        self.premises = premises if premises is not None else []

    def __repr__(self, level=0):
        indent = "  " * level
        s = f"{indent}{self.conclusion}  ({self.rule})\n"
        for premise in self.premises:
            s += premise.__repr__(level + 1)
        return s