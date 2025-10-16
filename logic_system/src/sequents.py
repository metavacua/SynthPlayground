from collections import Counter
from typing import Iterable
from .formulas import Formula


class Sequent:
    def __init__(self, antecedent: Iterable[Formula], succedent: Iterable[Formula]):
        self.antecedent = Counter(antecedent)
        self.succedent = Counter(succedent)

    def __repr__(self):
        def format_multiset(multiset):
            items = []
            for item, count in sorted(multiset.items(), key=lambda x: str(x[0])):
                if count > 1:
                    items.append(f"{count}*({item})")
                else:
                    items.append(str(item))
            return ", ".join(items)

        ant_str = format_multiset(self.antecedent)
        suc_str = format_multiset(self.succedent)
        return f"{ant_str} ⊢ {suc_str}"

    def __eq__(self, other):
        return self.antecedent == other.antecedent and self.succedent == other.succedent

    def __hash__(self):
        # Counter is not hashable, so we convert to a frozenset of items
        ant_items = frozenset(self.antecedent.items())
        suc_items = frozenset(self.succedent.items())
        return hash((ant_items, suc_items))
