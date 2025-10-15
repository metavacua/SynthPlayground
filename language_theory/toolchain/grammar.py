from collections import defaultdict

class Grammar:
    """
    A class to represent a formal grammar. It parses a grammar file
    and provides helpers for analyzing its properties.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.productions = [] # Store rules as (LHS_tuple, RHS_tuple)
        self.start_symbol = None
        self._parse_file()

    def _parse_file(self):
        """Parses the grammar file provided at initialization."""
        with open(self.filepath, 'r') as f:
            for line in f:
                line = line.split('#', 1)[0].strip()
                if not line or '->' not in line:
                    continue

                lhs_str, rhs_str = line.split('->', 1)
                lhs = tuple(lhs_str.strip().split())

                if self.start_symbol is None:
                    self.start_symbol = lhs[0]

                # Handle multiple RHS productions separated by |
                for rhs_part in rhs_str.split('|'):
                    rhs = tuple(rhs_part.strip().split())
                    self.productions.append((lhs, rhs))

    def get_productions_dict(self):
        """Returns productions grouped by LHS, for parser use."""
        prod_dict = defaultdict(list)
        for lhs, rhs in self.productions:
            # Parsers often expect the LHS to be a single symbol string
            prod_dict[" ".join(lhs)].append(rhs)
        return prod_dict

    def get_non_terminals(self):
        """Returns the set of all non-terminal symbols."""
        non_terminals = set()
        for lhs, rhs in self.productions:
            for symbol in lhs:
                if symbol.isupper():
                    non_terminals.add(symbol)
            for symbol in rhs:
                if symbol.isupper():
                    non_terminals.add(symbol)
        return non_terminals

    def get_terminals(self):
        """Returns the set of all terminal symbols."""
        terminals = set()
        for _, rhs in self.productions:
            for symbol in rhs:
                # Any symbol that isn't uppercase is a terminal
                if not symbol.isupper() and symbol:
                    terminals.add(symbol)
        return terminals

    def __str__(self):
        return f"Grammar(start={self.start_symbol}, productions={len(self.productions)})"