import argparse
import sys
from collections import defaultdict
from .grammar import Grammar
from .classifier import Classifier
from .lba import LBASimulator

def recognize_right_linear(grammar_productions, start_symbol, input_string):
    memo = {}
    def _search(symbol, text, path):
        state = (symbol, tuple(text))
        if state in memo: return memo[state]
        if symbol not in grammar_productions: return False
        for rule in grammar_productions[symbol]:
            current_path = path + [f"{symbol} -> {' '.join(rule)}"]
            if len(rule) == 1 and rule[0].islower():
                if text and text[0] == rule[0] and len(text) == 1:
                    print_path(current_path)
                    return True
            elif len(rule) == 2 and rule[0].islower() and rule[1].isupper():
                if text and text[0] == rule[0]:
                    if _search(rule[1], text[1:], current_path):
                        memo[state] = True
                        return True
        memo[state] = False
        return False
    return _search(start_symbol, list(input_string), [])

def reverse_grammar(grammar_productions):
    reversed_g = defaultdict(list)
    for non_terminal, rules in grammar_productions.items():
        for rule in rules:
            reversed_rule = list(reversed(rule))
            reversed_g[non_terminal].append(tuple(reversed_rule))
    return reversed_g

def print_path(path):
    print("\n--- Successful Derivation Path ---")
    for step in path:
        print(step)
    print("---------------------------------")

class EarleyItem:
    def __init__(self, rule, dot_pos, start_idx):
        self.rule = rule
        self.dot_pos = dot_pos
        self.start_idx = start_idx
        self.back_pointers = []
    def __eq__(self, other):
        return (self.rule, self.dot_pos, self.start_idx) == (other.rule, other.dot_pos, other.start_idx)
    def __hash__(self):
        return hash((self.rule, self.dot_pos, self.start_idx))
    def __repr__(self):
        return f"({self.rule[0]} -> {' '.join(self.rule[1][:self.dot_pos])}.{' '.join(self.rule[1][self.dot_pos:])}, {self.start_idx})"

def recognize_earley(grammar_productions, start_symbol, input_tokens):
    chart = [[] for _ in range(len(input_tokens) + 1)]
    for rule_rhs in grammar_productions.get(start_symbol, []):
        item = EarleyItem((start_symbol, rule_rhs), 0, 0)
        chart[0].append(item)
    for i in range(len(input_tokens) + 1):
        item_idx = 0
        while item_idx < len(chart[i]):
            item = chart[i][item_idx]
            item_idx += 1
            if item.dot_pos < len(item.rule[1]):
                next_symbol = item.rule[1][item.dot_pos]
                if next_symbol.isupper():
                    for new_rule_rhs in grammar_productions.get(next_symbol, []):
                        new_item = EarleyItem((next_symbol, new_rule_rhs), 0, i)
                        if new_item not in chart[i]:
                            chart[i].append(new_item)
                elif i < len(input_tokens) and next_symbol == input_tokens[i]:
                    new_item = EarleyItem(item.rule, item.dot_pos + 1, item.start_idx)
                    new_item.back_pointers.append(input_tokens[i])
                    chart[i+1].append(new_item)
            else:
                for prev_item in chart[item.start_idx]:
                    if prev_item.dot_pos < len(prev_item.rule[1]) and prev_item.rule[1][prev_item.dot_pos] == item.rule[0]:
                        new_item = EarleyItem(prev_item.rule, prev_item.dot_pos + 1, prev_item.start_idx)
                        found = False
                        for existing_item in chart[i]:
                            if existing_item == new_item:
                                existing_item.back_pointers.append((prev_item, item))
                                found = True
                                break
                        if not found:
                            new_item.back_pointers.append((prev_item, item))
                            chart[i].append(new_item)
    return chart

def get_parse_count(chart, start_symbol):
    final_items = [item for item in chart[-1] if item.rule[0] == start_symbol and item.dot_pos == len(item.rule[1]) and item.start_idx == 0]
    if not final_items: return 0
    return sum(count_parses(item) for item in final_items)

def count_parses(item):
    if not item.back_pointers: return 1 # Predicted states
    if isinstance(item.back_pointers[0], str): return 1 # Scanned terminal
    if hasattr(item, 'parse_count'): return item.parse_count
    count = 0
    for bp_set in item.back_pointers:
        item1, item2 = bp_set
        count += count_parses(item1) * count_parses(item2)
    item.parse_count = count
    return count

def main():
    parser = argparse.ArgumentParser(description="A grammar recognizer for various formal language classes.")
    parser.add_argument("grammar_file", help="Path to the grammar file.")
    parser.add_argument("input_string", help="The string to recognize.")
    parser.add_argument("--start-symbol", help="Override the default start symbol of the grammar.")
    args = parser.parse_args()
    try:
        grammar = Grammar(args.grammar_file)
        start_symbol = args.start_symbol if args.start_symbol else grammar.start_symbol
        print(f"Grammar loaded from {args.grammar_file}. Start symbol: {start_symbol}")

        classifier = Classifier(grammar)
        classification = classifier.classify()
        print(f"Classification: {classification}")

        productions_dict = grammar.get_productions_dict()

        if "UNRESTRICTED" in classification:
            print("\nWARNING: This grammar may be undecidable. Recognition is not attempted.")
        elif "CONTEXT-SENSITIVE" in classification:
            print("Using LBA simulator for CONTEXT-SENSITIVE grammar.")
            simulator = LBASimulator(grammar)
            if simulator.recognize(args.input_string):
                print(f"\nSUCCESS: String '{args.input_string}' is recognized by the LBA.")
            else:
                print(f"\nFAILURE: String '{args.input_string}' is NOT recognized by the LBA.")
        elif "RIGHT-LINEAR REGULAR" in classification:
            input_tokens = args.input_string.split()
            if recognize_right_linear(productions_dict, start_symbol, input_tokens):
                print(f"\nSUCCESS: String '{args.input_string}' is recognized.")
            else:
                print(f"\nFAILURE: String '{args.input_string}' is not recognized.")
        elif "LEFT-LINEAR REGULAR" in classification:
            reversed_prods = reverse_grammar(productions_dict)
            if recognize_right_linear(reversed_prods, start_symbol, args.input_string[::-1]):
                print(f"\nSUCCESS: String '{args.input_string}' is recognized.")
            else:
                print(f"\nFAILURE: String '{args.input_string}' is not recognized.")
        elif "CONTEXT-FREE" in classification:
            print("Using Earley parser for CONTEXT-FREE grammar.")
            input_tokens = list(args.input_string) if ' ' not in args.input_string else args.input_string.split()
            chart = recognize_earley(productions_dict, start_symbol, input_tokens)
            parse_count = get_parse_count(chart, start_symbol)
            if parse_count > 0:
                 print(f"\nSUCCESS: String '{args.input_string}' is recognized.")
                 print(f"Found {parse_count} valid parse(s).")
                 if parse_count > 1: print("Grammar is AMBIGUOUS for this input.")
                 else: print("Grammar is UNAMBIGUOUS for this input.")
            else:
                 print(f"\nFAILURE: String '{args.input_string}' is not recognized.")
        else:
            print("\nCould not determine a suitable recognition strategy for this grammar.")

    except FileNotFoundError:
        print(f"Error: Grammar file not found at {args.grammar_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
