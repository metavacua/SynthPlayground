import json
from collections import defaultdict
import os

class Grammar:
    """
    A class to represent a formal grammar. It can parse a grammar from a
    traditional text file or from a JSON AST file.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.productions = []  # Store rules as (LHS_tuple, RHS_tuple)
        self.start_symbol = None
        self._non_terminals = None
        self._terminals = None
        self._parse_file()

    def _traverse_ast(self, node):
        """Recursively traverses the AST to extract grammar productions."""
        if 'type' not in node:
            return

        lhs = (node['type'],)
        rhs_parts = []

        if node.get('children'):
            for child in node['children']:
                if 'type' in child:
                    rhs_parts.append(child['type'])
                    self._traverse_ast(child)

        # Only add a production if it has a right-hand side.
        # This treats leaf nodes (terminals) correctly as they won't form new productions here.
        if rhs_parts:
            self.productions.append((lhs, tuple(rhs_parts)))

    def _parse_file(self):
        """Parses the grammar file provided at initialization."""
        if self.filepath.endswith('.json'):
            if not os.path.exists(self.filepath):
                print(f"Warning: AST file not found at {self.filepath}", file=sys.stderr)
                return
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    ast_root = json.load(f)
                if 'type' in ast_root:
                    self.start_symbol = ast_root['type']
                    self._traverse_ast(ast_root)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error parsing AST file {self.filepath}: {e}", file=sys.stderr)
                pass
        else:
            # Legacy grammar file parsing
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
                        for rhs_part in rhs_str.split('|'):
                            rhs = tuple(rhs_part.strip().split() or ((),)) # Handle empty production
                            self.productions.append((lhs, rhs))
            except FileNotFoundError:
                pass

    def get_non_terminals(self):
        """
        Returns the set of all non-terminal symbols.
        A non-terminal is any symbol that appears on the left-hand side of a production.
        """
        if self._non_terminals is None:
            non_terminals = set()
            for lhs, _ in self.productions:
                non_terminals.update(lhs)
            self._non_terminals = non_terminals
        return self._non_terminals

    def get_terminals(self):
        """
        Returns the set of all terminal symbols.
        A terminal is any symbol that appears on the right-hand side of a production
        but never on the left-hand side.
        """
        if self._terminals is None:
            non_terminals = self.get_non_terminals()
            terminals = set()
            for _, rhs in self.productions:
                for symbol in rhs:
                    if symbol not in non_terminals:
                        terminals.add(symbol)
            self._terminals = terminals
        return self._terminals

    def __str__(self):
        return f"Grammar(start={self.start_symbol}, productions={len(self.productions)})"
