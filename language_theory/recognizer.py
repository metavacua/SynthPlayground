import argparse
import sys
from collections import defaultdict

def recognize_right_linear(grammar, start_symbol, input_string):
    """
    Attempts to recognize a string using a right-linear grammar with tracing.
    Returns True if the string is recognized, False otherwise.
    """
    memo = {}

    def _search(symbol, text, path):
        """Inner recursive search function with memoization."""
        state = (symbol, tuple(text))
        if state in memo:
            return memo[state]

        indent = "  " * len(path)
        print(f"{indent}Attempting to match '{symbol}' with input '{"".join(text)}'")

        if symbol not in grammar:
            return False

        for rule in grammar[symbol]:
            current_path = path + [f"{symbol} -> {' '.join(rule)}"]

            # Rule is terminal-only (A -> t)
            if len(rule) == 1 and rule[0].islower():
                terminal = rule[0]
                if text and text[0] == terminal and len(text) == 1:
                    print(f"{indent}  Matched terminal rule. End of string.")
                    print_path(current_path)
                    return True
                continue # Rule doesn't match or there's leftover input

            # Rule is terminal + non-terminal (A -> tB)
            if len(rule) == 2 and rule[0].islower() and rule[1].isupper():
                terminal, non_terminal = rule
                if text and text[0] == terminal:
                    print(f"{indent}  Matched terminal '{terminal}', recursing on '{non_terminal}'")
                    if _search(non_terminal, text[1:], current_path):
                        memo[state] = True
                        return True

        memo[state] = False
        return False

    return _search(start_symbol, list(input_string), [])

def reverse_grammar(grammar):
    """Reverses a left-linear grammar into a right-linear one."""
    reversed_g = defaultdict(list)
    for non_terminal, rules in grammar.items():
        for rule in rules:
            # Reverse the parts of the rule
            # e.g., A -> Bb becomes A -> bB
            reversed_rule = list(reversed(rule))
            reversed_g[non_terminal].append(reversed_rule)
    return reversed_g

def print_path(path):
    """Prints the final successful derivation path."""
    print("\n--- Successful Derivation Path ---")
    for step in path:
        print(step)
    print("---------------------------------")

def parse_grammar(filepath):
    """
    Parses a grammar file into a dictionary.
    Format: S -> aA | b
    Comments starting with # are ignored.
    """
    grammar = defaultdict(list)
    with open(filepath, 'r') as f:
        for line in f:
            line = line.split('#', 1)[0].strip()
            if not line:
                continue

            if '->' not in line:
                raise ValueError(f"Invalid rule format: {line}")

            lhs, rhs_str = line.split('->', 1)
            lhs = lhs.strip()

            # RHS can have multiple productions separated by |
            # Each production is a sequence of symbols separated by spaces.
            parsed_rhs = [r.strip().split() for r in rhs_str.split('|')]

            # LHS is a sequence of symbols separated by spaces.
            # We represent it as a single string key in the grammar dict.
            grammar[lhs].extend(parsed_rhs)

    return grammar

def recognize_earley(grammar, start_symbol, input_string):
    """
    Recognizes a string using the Earley parsing algorithm for any CFG.
    """
    # An Earley item is a tuple: (rule, dot_position, start_chart_index)
    # The chart is a list of sets of Earley items.
    chart = [set() for _ in range(len(input_string) + 1)]

    # Add initial items for the start symbol
    for rule in grammar[start_symbol]:
        chart[0].add(( (start_symbol, tuple(rule)), 0, 0))

    for i in range(len(input_string) + 1):
        queue = list(chart[i])
        item_idx = 0
        while item_idx < len(queue):
            item = queue[item_idx]
            item_idx += 1

            rule, dot_pos, start_idx = item

            # Completion
            if dot_pos == len(rule[1]):
                for prev_item in chart[start_idx]:
                    prev_rule, prev_dot_pos, prev_start_idx = prev_item
                    if prev_dot_pos < len(prev_rule[1]) and prev_rule[1][prev_dot_pos] == rule[0]:
                        new_item = (prev_rule, prev_dot_pos + 1, prev_start_idx)
                        if new_item not in chart[i]:
                            chart[i].add(new_item)
                            queue.append(new_item)
            else:
                next_symbol = rule[1][dot_pos]
                # Prediction
                if next_symbol.isupper():
                    for new_rule in grammar.get(next_symbol, []):
                        new_item = ((next_symbol, tuple(new_rule)), 0, i)
                        if new_item not in chart[i]:
                            chart[i].add(new_item)
                            queue.append(new_item)
                # Scanning
                elif i < len(input_string) and next_symbol == input_string[i]:
                    new_item = (rule, dot_pos + 1, start_idx)
                    if new_item not in chart[i + 1]:
                        chart[i + 1].add(new_item)


    # Check for successful parse
    for item in chart[len(input_string)]:
        rule, dot_pos, start_idx = item
        if rule[0] == start_symbol and dot_pos == len(rule[1]) and start_idx == 0:
            return True

    return False

def main():
    """Main function to run the recognizer."""
    parser = argparse.ArgumentParser(description="A grammar recognizer for regular and context-free grammars.")
    parser.add_argument("grammar_file", help="Path to the grammar file.")
    parser.add_argument("input_string", help="The string to recognize.")
    parser.add_argument("--start-symbol", default="S", help="The start symbol of the grammar (default: S).")
    args = parser.parse_args()

    try:
        grammar = parse_grammar(args.grammar_file)
        print(f"Grammar loaded successfully from {args.grammar_file}")

        # Heuristics to determine grammar type
        is_csg = any(len(non_terminal) > 1 for non_terminal in grammar.keys())
        is_right_reg = all(len(r) <= 2 and (len(r) < 2 or r[1].isupper()) for rules in grammar.values() for r in rules) and not is_csg
        is_left_reg = all(len(r) <= 2 and (len(r) < 2 or r[0].isupper()) for rules in grammar.values() for r in rules) and not is_csg

        if is_csg:
            print("Heuristic determined grammar to be CONTEXT-SENSITIVE.")
            print("Recognition of context-sensitive languages is not implemented.")
            print("This is a PSPACE-complete problem and requires a different parsing approach (e.g., a Linear Bounded Automaton).")

        elif is_right_reg and not is_left_reg:
            print("Heuristic determined grammar to be RIGHT-LINEAR.")
            if recognize_right_linear(grammar, args.start_symbol, args.input_string):
                print(f"\nSUCCESS: The string '{args.input_string}' can be generated by the grammar.")
            else:
                print(f"\nFAILURE: The string '{args.input_string}' cannot be generated by the grammar.")

        elif is_left_reg and not is_right_reg:
            print("Heuristic determined grammar to be LEFT-LINEAR.")
            print("Reversing grammar and input string for right-linear recognizer.")
            reversed_grammar = reverse_grammar(grammar)
            reversed_string = args.input_string[::-1]
            if recognize_right_linear(reversed_grammar, args.start_symbol, reversed_string):
                print(f"\nSUCCESS: The string '{args.input_string}' can be generated by the grammar.")
            else:
                print(f"\nFAILURE: The string '{args.input_string}' cannot be generated by the grammar.")

        else:
            print("Heuristic determined grammar to be CONTEXT-FREE. Using Earley parser.")
            if recognize_earley(grammar, args.start_symbol, args.input_string):
                 print(f"\nSUCCESS: The string '{args.input_string}' is recognized by the CFG.")
            else:
                 print(f"\nFAILURE: The string '{args.input_string}' is not recognized by the CFG.")

    except FileNotFoundError:
        print(f"Error: Grammar file not found at {args.grammar_file}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing grammar file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()