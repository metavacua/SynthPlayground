import sys
from .grammar import Grammar

class Classifier:
    """
    Analyzes a Grammar object to determine its classification within the Chomsky Hierarchy.
    This version is adapted to work with grammars derived from ASTs, where the
    distinction between terminals and non-terminals is based on production rules,
    not on character casing.
    """
    def __init__(self, grammar):
        self.grammar = grammar
        self.productions = grammar.productions
        self.non_terminals = self.grammar.get_non_terminals()
        self.terminals = self.grammar.get_terminals()

    def is_non_terminal(self, symbol):
        """Checks if a symbol is a non-terminal."""
        return symbol in self.non_terminals

    def is_terminal(self, symbol):
        """Checks if a symbol is a terminal."""
        return symbol in self.terminals

    def classify(self):
        """
        Determines the most specific classification for the grammar.
        """
        if not self.productions:
            return "EMPTY"

        # Check from the most restrictive (Type-3) to the least (Type-0)
        if self._is_regular():
            return "REGULAR (TYPE-3)"

        if self._is_context_free():
            return "CONTEXT-FREE (TYPE-2)"

        if self._is_context_sensitive():
            return "CONTEXT-SENSITIVE (TYPE-1)"

        return "UNRESTRICTED (TYPE-0)"

    def _is_regular(self):
        """
        Checks if the grammar is regular (right-linear).
        A -> aB or A -> a
        """
        for lhs, rhs in self.productions:
            if len(lhs) != 1 or not self.is_non_terminal(lhs[0]):
                return False

            if not rhs: # Empty production
                continue

            if len(rhs) == 1 and not self.is_terminal(rhs[0]):
                return False
            if len(rhs) == 2 and not (self.is_terminal(rhs[0]) and self.is_non_terminal(rhs[1])):
                return False
            if len(rhs) > 2:
                return False
        return True

    def _is_context_free(self):
        """
        Checks if the grammar is context-free.
        A -> γ (where γ is any string of terminals and/or non-terminals)
        """
        for lhs, _ in self.productions:
            if len(lhs) != 1 or not self.is_non_terminal(lhs[0]):
                return False
        return True

    def _is_context_sensitive(self):
        """
        Checks if the grammar is context-sensitive (non-contracting).
        |LHS| <= |RHS|.
        """
        for lhs, rhs in self.productions:
            if len(lhs) > len(rhs):
                # Exception for S -> ε, if S is the start symbol and doesn't appear on the RHS.
                if self.grammar.start_symbol in lhs and not rhs:
                    start_on_rhs = any(self.grammar.start_symbol in r for _, r in self.productions)
                    if not start_on_rhs:
                        continue
                return False
        return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="A tool to classify a formal grammar from an AST.")
    parser.add_argument("grammar_file", help="Path to the grammar file (AST JSON).")
    args = parser.parse_args()
    try:
        grammar = Grammar(args.grammar_file)
        classifier = Classifier(grammar)
        classification = classifier.classify()
        print(f"--- Grammar Classification for: {args.grammar_file} ---")
        print(f"Result: {classification}")
        print("-----------------------------------------------------")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
