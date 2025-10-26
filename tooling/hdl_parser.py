from logic_system.src.formulas import Formula, Prop, LinImplies, Tensor
from logic_system.src.sequents import Sequent
from collections import Counter


def parse_formula(s: str):
    """A very basic parser for formulas."""
    s = s.strip()
    if "->" in s:
        parts = s.split("->", 1)
        return LinImplies(parse_formula(parts[0]), parse_formula(parts[1]))
    if "*" in s:
        parts = s.split("*", 1)
        return Tensor(parse_formula(parts[0]), parse_formula(parts[1]))
    return Prop(s)


def parse_sequent(s: str):
    """A very basic parser for sequents."""
    parts = s.split("|-")
    antecedent = {parse_formula(f) for f in parts[0].split(",")}
    succedent = {parse_formula(parts[1])}
    return Sequent(antecedent, succedent)
