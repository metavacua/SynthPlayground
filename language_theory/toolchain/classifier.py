from .grammar import Grammar

class Classifier:
    """
    Analyzes a Grammar object to determine its classification within the Chomsky Hierarchy.
    """
    def __init__(self, grammar):
        self.grammar = grammar
        self.productions = grammar.productions

    def classify(self):
        """
        Determines the most specific classification for the grammar.
        Follows the hierarchy from Type-3 up to Type-0.
        """
        if not self.productions:
            return "EMPTY"

        is_unrestricted, is_contracting = self._check_type_0()
        if is_contracting:
            return "UNRESTRICTED (TYPE-0, Contracting)"

        is_csg = self._check_type_1(is_unrestricted)
        if is_csg:
            return "CONTEXT-SENSITIVE (TYPE-1)"

        is_cfg, has_empty = self._check_type_2()
        if not is_cfg:
            # This case is rare, implies context-sensitive without being unrestricted
            return "CONTEXT-SENSITIVE (Non-CFG)"

        is_left_reg, is_right_reg = self._check_type_3()

        if is_left_reg and is_right_reg:
            # Both left and right linear rules are present
            return "CONTEXT-FREE (Mixed Regular)"
        if is_left_reg:
            return "LEFT-LINEAR REGULAR (TYPE-3)"
        if is_right_reg:
            return "RIGHT-LINEAR REGULAR (TYPE-3)"

        return "CONTEXT-FREE (TYPE-2)"

    def _check_type_0(self):
        """
        Checks for unrestricted grammar properties.
        - is_unrestricted: True if any LHS has more than one symbol.
        - is_contracting: True if any rule is contracting (|LHS| > |RHS|).
        """
        is_unrestricted = False
        is_contracting = False
        for lhs, rhs in self.productions:
            if len(lhs) > 1:
                is_unrestricted = True
            if len(lhs) > len(rhs):
                # Exception for the rule S -> ε, if S is not on the RHS of any rule.
                if lhs == (self.grammar.start_symbol,) and not rhs:
                    start_on_rhs = any(self.grammar.start_symbol in r for _, r in self.productions)
                    if not start_on_rhs:
                        continue
                is_contracting = True
        return is_unrestricted, is_contracting

    def _check_type_1(self, is_unrestricted):
        """
        Checks if the grammar is context-sensitive.
        A grammar is context-sensitive if it's unrestricted but not contracting.
        """
        return is_unrestricted

    def _check_type_2(self):
        """
        Checks if the grammar is context-free.
        - is_cfg: True if all LHS have exactly one non-terminal.
        - has_empty: True if any rule produces an empty string.
        """
        is_cfg = True
        has_empty = False
        for lhs, rhs in self.productions:
            if len(lhs) != 1 or not list(lhs)[0].isupper():
                is_cfg = False
            if not rhs:
                has_empty = True
        return is_cfg, has_empty

    def _check_type_3(self):
        """
        Checks if the grammar is regular (left or right linear).
        - is_left_reg: True if all rules are of the form A -> Ba or A -> a.
        - is_right_reg: True if all rules are of the form A -> aB or A -> a.
        """
        is_left_reg = True
        is_right_reg = True

        for lhs, rhs in self.productions:
            # All regular grammars must be CFG.
            if len(lhs) != 1 or not list(lhs)[0].isupper():
                is_left_reg = False
                is_right_reg = False
                break

            # Right-linear checks
            if len(rhs) > 2 or (len(rhs) == 2 and not (rhs[0].islower() and rhs[1].isupper())) or (len(rhs) == 1 and not rhs[0].islower()):
                is_right_reg = False

            # Left-linear checks
            if len(rhs) > 2 or (len(rhs) == 2 and not (rhs[0].isupper() and rhs[1].islower())) or (len(rhs) == 1 and not rhs[0].islower()):
                is_left_reg = False

        return is_left_reg, is_right_reg

def main():
    import argparse
    parser = argparse.ArgumentParser(description="A tool to classify a formal grammar.")
    parser.add_argument("grammar_file", help="Path to the grammar file.")
    args = parser.parse_args()
    try:
        grammar = Grammar(args.grammar_file)
        classifier = Classifier(grammar)
        classification = classifier.classify()
        print(f"--- Grammar Classification for: {args.grammar_file} ---")
        print(f"Result: {classification}")
        print("-----------------------------------------------------")
    except FileNotFoundError:
        print(f"Error: Grammar file not found at {args.grammar_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
