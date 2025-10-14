import sys
from logic import Atom, With, Plus, Top, Zero, prove

def parse_prop(s: str):
    s = s.strip()
    if s.startswith('(') and s.endswith(')'):
        balance = 0; is_wrapper = True
        for i, char in enumerate(s):
            if char == '(': balance += 1
            elif char == ')': balance -= 1
            if balance == 0 and i < len(s) - 1: is_wrapper = False; break
        if is_wrapper: s = s[1:-1].strip()

    balance = 0
    for i in range(len(s) - 1, -1, -1):
        char = s[i]
        if char == ')': balance += 1
        elif char == '(': balance -= 1
        elif balance == 0 and char in ['&', '⊕']:
            left = parse_prop(s[:i]); right = parse_prop(s[i+1:])
            return With(left, right) if char == '&' else Plus(left, right)

    if s == '⊤': return Top()
    if s == '0': return Zero()
    if s.isalnum(): return Atom(s)
    raise ValueError(f"Could not parse proposition: '{s}'")

def parse_sequent(s: str):
    parts = s.split('|-')
    if len(parts) != 2: raise ValueError("Sequent must be 'A |- Γ'")
    antecedent = (parse_prop(parts[0]),)
    succedent = tuple(parse_prop(p) for p in parts[1].split(',') if p.strip())
    return antecedent, succedent

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r') as f: program_str = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found."); sys.exit(1)

        print(f"CI Logic Interpreter: Attempting to prove: {program_str}")
        try:
            antecedent, succedent = parse_sequent(program_str)
            if prove(antecedent, succedent):
                print("Provable.")
            else:
                print("Not Provable.")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("No file provided. Please provide a file to test.")