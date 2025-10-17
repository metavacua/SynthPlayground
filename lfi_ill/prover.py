from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Tuple, List, Dict, Iterator
from collections import Counter
from lfi_ill.ast import *

def split_context(context: Tuple[Formula, ...]) -> Iterator[Tuple[Tuple[Formula, ...], Tuple[Formula, ...]]]:
    """
    Iterates through all possible ways to split a context (multiset) into two sub-contexts.
    This is a correct, if inefficient, way to handle multiset splits.
    """
    if not context:
        yield ((), ())
        return

    first = context[0]
    rest = context[1:]

    for left, right in split_context(rest):
        yield ((first,) + left, right)
        yield (left, (first,) + right)

@dataclass(frozen=True, eq=True)
class Sequent:
    antecedent: Tuple[Formula, ...] = field(default_factory=tuple)
    consequent: Tuple[Formula, ...] = field(default_factory=tuple)

    def __repr__(self) -> str:
        ant_str = ", ".join(map(str, self.antecedent))
        con_str = ", ".join(map(str, self.consequent))
        return f"{ant_str} ⊢ {con_str}"

def prove(sequent: Sequent, history: Set[Sequent] = None, depth: int = 10) -> bool:
    """
    Attempts to prove a given sequent using the rules of pLLL.
    """
    if depth <= 0:
        return False

    if history is None:
        history = set()

    # Using a tuple of sorted tuples for the key to handle multiset equivalence
    key = (tuple(sorted(sequent.antecedent, key=str)), tuple(sorted(sequent.consequent, key=str)))
    if key in history:
        return True # Loop detected

    history.add(key)

    # --- Identity Group ---
    if len(sequent.antecedent) == 1 and len(sequent.consequent) == 1:
        if sequent.antecedent[0] == sequent.consequent[0]:
            return True

    if not sequent.antecedent and len(sequent.consequent) == 2:
        if sequent.consequent[0] == sequent.consequent[1].neg():
            return True

    # --- Paraconsistent Explosion Rule ---
    ant_counter = Counter(sequent.antecedent)
    for f in ant_counter:
        if isinstance(f, Atom):
            neg_f = Negation(f)
            cons_f = Consistency(f)
            if ant_counter[neg_f] > 0 and ant_counter[cons_f] > 0:
                return True

    # --- Right Rules ---
    for i, formula in enumerate(sequent.consequent):
        rest_consequent = sequent.consequent[:i] + sequent.consequent[i+1:]

        if isinstance(formula, Tensor):
            for ant_split1, ant_split2 in split_context(sequent.antecedent):
                for con_split1, con_split2 in split_context(rest_consequent):
                    premise1 = Sequent(ant_split1, con_split1 + (formula.left,))
                    premise2 = Sequent(ant_split2, con_split2 + (formula.right,))
                    if prove(premise1, history.copy(), depth - 1) and prove(premise2, history.copy(), depth - 1):
                        return True
        elif isinstance(formula, Par):
            premise = Sequent(sequent.antecedent, rest_consequent + (formula.left, formula.right))
            if prove(premise, history.copy(), depth - 1):
                return True
        elif isinstance(formula, With):
            premise1 = Sequent(sequent.antecedent, rest_consequent + (formula.left,))
            premise2 = Sequent(sequent.antecedent, rest_consequent + (formula.right,))
            if prove(premise1, history.copy(), depth - 1) and prove(premise2, history.copy(), depth - 1):
                return True
        elif isinstance(formula, Plus):
            premise_left = Sequent(sequent.antecedent, rest_consequent + (formula.left,))
            if prove(premise_left, history.copy(), depth - 1):
                return True
            premise_right = Sequent(sequent.antecedent, rest_consequent + (formula.right,))
            if prove(premise_right, history.copy(), depth - 1):
                return True
        elif isinstance(formula, OfCourse):
            if all(isinstance(f, OfCourse) for f in sequent.antecedent) and \
               all(isinstance(f, WhyNot) for f in rest_consequent):
                premise = Sequent(
                    antecedent=tuple(f.formula for f in sequent.antecedent),
                    consequent=tuple(f.formula for f in rest_consequent) + (formula.formula,)
                )
                if prove(premise, history.copy(), depth - 1):
                    return True
        elif isinstance(formula, Section):
            bang_gamma = tuple(f.formula for f in sequent.antecedent if isinstance(f, OfCourse))
            sec_delta = tuple(f.formula for f in sequent.antecedent if isinstance(f, Section))
            if len(bang_gamma) + len(sec_delta) == len(sequent.antecedent):
                 premise = Sequent(antecedent=bang_gamma + sec_delta, consequent=(formula.formula,))
                 if prove(premise, history.copy(), depth - 1):
                     return True
        elif isinstance(formula, WhyNot): # WhyNot Right
            premise = Sequent(sequent.antecedent, rest_consequent + (formula.formula,))
            if prove(premise, history.copy(), depth - 1):
                return True

    # --- Left Rules ---
    for i, formula in enumerate(sequent.antecedent):
        rest_antecedent = sequent.antecedent[:i] + sequent.antecedent[i+1:]

        if isinstance(formula, Tensor):
            premise = Sequent(rest_antecedent + (formula.left, formula.right), sequent.consequent)
            if prove(premise, history.copy(), depth - 1):
                return True
        elif isinstance(formula, Par):
            for con_split1, con_split2 in split_context(sequent.consequent):
                premise1 = Sequent(rest_antecedent + (formula.left,), con_split1)
                premise2 = Sequent(rest_antecedent + (formula.right,), con_split2)
                if prove(premise1, history.copy(), depth - 1) and prove(premise2, history.copy(), depth - 1):
                    return True
        elif isinstance(formula, With):
            premise_left = Sequent(rest_antecedent + (formula.left,), sequent.consequent)
            if prove(premise_left, history.copy(), depth - 1):
                return True
            premise_right = Sequent(rest_antecedent + (formula.right,), sequent.consequent)
            if prove(premise_right, history.copy(), depth - 1):
                return True
        elif isinstance(formula, Plus):
            premise1 = Sequent(rest_antecedent + (formula.left,), sequent.consequent)
            premise2 = Sequent(rest_antecedent + (formula.right,), sequent.consequent)
            if prove(premise1, history.copy(), depth - 1) and prove(premise2, history.copy(), depth - 1):
                return True
        elif isinstance(formula, OfCourse): # Dereliction, Weakening, Contraction
            # Dereliction
            premise_d = Sequent(rest_antecedent + (formula.formula,), sequent.consequent)
            if prove(premise_d, history.copy(), depth - 1):
                return True
            # Weakening
            premise_w = Sequent(rest_antecedent, sequent.consequent)
            if prove(premise_w, history.copy(), depth - 1):
                return True
            # Contraction
            premise_c = Sequent(sequent.antecedent + (formula,), sequent.consequent)
            if prove(premise_c, history.copy(), depth - 1):
                return True
        elif isinstance(formula, WhyNot): # WhyNot Left (Promotion)
             if all(isinstance(f, OfCourse) for f in rest_antecedent) and \
               all(isinstance(f, WhyNot) for f in sequent.consequent):
                premise = Sequent(
                    antecedent=tuple(f.formula for f in rest_antecedent) + (formula.formula,),
                    consequent=tuple(f.formula for f in sequent.consequent)
                )
                if prove(premise, history.copy(), depth - 1):
                    return True
        elif isinstance(formula, Section): # Section Left
            bang_gamma = tuple(f.formula for f in rest_antecedent if isinstance(f, OfCourse))
            sec_delta = tuple(f.formula for f in rest_antecedent if isinstance(f, Section))
            if len(bang_gamma) + len(sec_delta) == len(rest_antecedent):
                 premise = Sequent(antecedent=bang_gamma + sec_delta + (formula.formula,), consequent=())
                 if prove(premise, history.copy(), depth - 1):
                     return True

    return False