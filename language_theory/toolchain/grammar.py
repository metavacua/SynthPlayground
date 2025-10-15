from collections import defaultdict

class Grammar:
    """
    A class to represent a formal grammar. It parses a grammar file
    and provides helpers for analyzing its properties.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.productions = defaultdict(list)
        self.start_symbol = "S" # Default, can be changed.
        self._parse_file()

    def _parse_file(self):
        """Parses the grammar file provided at initialization."""
        with open(self.filepath, 'r') as f:
            for line in f:
                line = line.split('#', 1)[0].strip()
                if not line:
                    continue

                if '->' not in line:
                    continue # Or raise error

                lhs, rhs_str = line.split('->', 1)
                lhs = lhs.strip()

                # The first rule's LHS is often the start symbol.
                if not self.productions:
                    self.start_symbol = lhs.split()[0]

                rhs_productions = [tuple(r.strip().split()) for r in rhs_str.split('|')]
                self.productions[lhs].extend(rhs_productions)

    def get_non_terminals(self):
        """Returns the set of non-terminal symbols."""
        non_terminals = set(self.productions.keys())
        for rules in self.productions.values():
            for rule in rules:
                for symbol in rule:
                    if symbol.isupper():
                        non_terminals.add(symbol)
        return non_terminals

    def get_terminals(self):
        """Returns the set of terminal symbols."""
        terminals = set()
        for rules in self.productions.values():
            for rule in rules:
                for symbol in rule:
                    if not symbol.isupper() and symbol:
                        terminals.add(symbol)
        return terminals

    def __str__(self):
        return f"Grammar(start={self.start_symbol}, productions={len(self.productions)})"