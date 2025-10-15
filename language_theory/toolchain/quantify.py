import argparse
import sys
from grammar import Grammar

def main():
    """
    Main function to run the grammar quantifier.
    This tool computes and reports various metrics for a given grammar.
    """
    parser = argparse.ArgumentParser(description="A tool to quantify properties of a formal grammar.")
    parser.add_argument("grammar_file", help="Path to the grammar file.")
    args = parser.parse_args()

    try:
        grammar = Grammar(args.grammar_file)
        print(f"--- Quantitative Analysis for: {args.grammar_file} ---")

        # Get alphabet sizes
        non_terminals = grammar.get_non_terminals()
        terminals = grammar.get_terminals()
        print(f"\n1. Alphabet Sizes:")
        print(f"   - Non-Terminals ({len(non_terminals)}): {sorted(list(non_terminals))}")
        print(f"   - Terminals ({len(terminals)}): {sorted(list(terminals))}")

        # Get rule counts
        total_rules = sum(len(rules) for rules in grammar.productions.values())
        print(f"\n2. Rule Metrics:")
        print(f"   - Total Production Rules: {total_rules}")

        # Calculate average rule length (RHS)
        if total_rules > 0:
            total_rhs_length = sum(len(rule) for rules in grammar.productions.values() for rule in rules)
            avg_rhs_length = total_rhs_length / total_rules
            print(f"   - Average RHS Length: {avg_rhs_length:.2f}")

        print("\n-------------------------------------------------")

    except FileNotFoundError:
        print(f"Error: Grammar file not found at {args.grammar_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()