import json
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

    def _traverse_ast(self, node):
        """Recursively traverses the AST to extract grammar productions."""
        if 'type' not in node:
            return

        lhs = (node['type'],)

        if 'children' in node and node['children']:
            rhs = tuple(child['type'] for child in node['children'] if 'type' in child)
            if rhs: # Only add production if there are children with types
                self.productions.append((lhs, rhs))
            for child in node['children']:
                self._traverse_ast(child)
        elif 'text' in node:
            # Terminal node. Production is from the node type to the text.
            rhs = (node['text'].decode('utf-8') if isinstance(node['text'], bytes) else node['text'],)
            self.productions.append((lhs, rhs))

    def _parse_file(self):
        """Parses the grammar file provided at initialization."""
        if self.filepath.endswith('.json'):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    ast_root = json.load(f)
                if 'type' in ast_root:
                    self.start_symbol = ast_root['type']
                    self._traverse_ast(ast_root)
            except (json.JSONDecodeError, FileNotFoundError):
                # If it's not a valid JSON or not found, productions will be empty.
                pass
        else:
            try:
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
            except FileNotFoundError:
                pass

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
        for lhs, _ in self.productions:
            non_terminals.update(lhs)
        return non_terminals

    def get_terminals(self):
        """Returns the set of all terminal symbols."""
        non_terminals = self.get_non_terminals()
        terminals = set()
        for _, rhs in self.productions:
            for symbol in rhs:
                if symbol not in non_terminals:
                    terminals.add(symbol)
        return terminals

    def __str__(self):
        return f"Grammar(start={self.start_symbol}, productions={len(self.productions)})"
