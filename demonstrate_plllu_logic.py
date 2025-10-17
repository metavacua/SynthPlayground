import sys
import os
import subprocess

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def run_evaluator(sequent_string):
    """
    Runs the plllu_evaluator.py script as a subprocess and captures its output.
    """
    process = subprocess.run(
        ['python', 'tooling/plllu_evaluator.py', sequent_string],
        capture_output=True,
        text=True
    )
    # Extract the final result line
    result_line = ""
    if process.returncode == 0:
        # The final line of stdout should contain the result
        last_line = process.stdout.strip().split('\n')[-1]
        if last_line.startswith("--- Result:"):
            result_line = last_line.replace("--- Result:", "").strip()

    return process.returncode, result_line, process.stdout, process.stderr

def main():
    """
    Runs a suite of tests against the pLLLU evaluator pipeline.
    """
    test_cases = [
        # --- PDA Rejections (Syntax) ---
        {"desc": "PDA Reject: Unbalanced parenthesis", "sequent": "A:T |- (A & B", "should_fail": True},

        # --- Interpreter Rejections (Linearity) ---
        {"desc": "Linearity Reject: Atom not consumed", "sequent": "A:T, B:T |- A", "should_fail": True},
        {"desc": "Linearity Reject: Additive branches consume different resources", "sequent": "A:T, B:T |- A & B", "should_fail": True},

        # --- Four-Valued Logic & Linearity Success ---
        {"desc": "Logic: T & T -> T (with shared context)", "sequent": "A:T |- A & A", "expected_result": "TRUE"},
        {"desc": "Logic: T | F -> T (with shared context)", "sequent": "A:T, B:F |- A | B", "should_fail": True}, # Fails linearity
        {"desc": "Logic: T | N -> T", "sequent": "A:T |- A | A", "expected_result": "TRUE"},
        {"desc": "Logic: F | N -> N", "sequent": "A:F, B:N |- A", "should_fail": True}, # Fails linearity

        # --- LFI/LFU Operator Tests ---
        {"desc": "LFI: ∘(T) -> T", "sequent": "A:T |- ∘A", "expected_result": "TRUE"},
        {"desc": "LFI: ∘(F) -> T", "sequent": "A:F |- ∘A", "expected_result": "TRUE"},
        {"desc": "LFI: ∘(B) -> F", "sequent": "A:B |- ∘A", "expected_result": "FALSE"},
        {"desc": "LFI: ∘(N) -> F", "sequent": "A:N |- ∘A", "expected_result": "FALSE"},
        {"desc": "LFU: ~(T) -> F", "sequent": "A:T |- ~A", "expected_result": "FALSE"},
        {"desc": "LFU: ~(F) -> T", "sequent": "A:F |- ~A", "expected_result": "TRUE"},
        {"desc": "LFU: ~(B) -> B", "sequent": "A:B |- ~A", "expected_result": "BOTH"},
        {"desc": "LFU: ~(N) -> N", "sequent": "A:N |- ~A", "expected_result": "NEITHER"},

        # --- Paraconsistent Evaluation ---
        {"desc": "Paraconsistency: A & ~A with A=B", "sequent": "A:B |- A & ~A", "expected_result": "BOTH"},
    ]

    print("--- Demonstrating the pLLLU Logic Evaluator ---")

    all_passed = True
    for i, case in enumerate(test_cases):
        print(f"\n--- Test {i+1}: {case['desc']} ---")
        print(f"Input: \"{case['sequent']}\"")

        return_code, result, stdout, stderr = run_evaluator(case['sequent'])

        is_pass = False
        if case.get('should_fail'):
            if return_code != 0:
                is_pass = True
                print("  --> RESULT: SUCCESS (Correctly failed)")
            else:
                print(f"  --> RESULT: FAILURE (Should have failed but passed, got {result})")
        else:
            if return_code == 0 and result == case['expected_result']:
                is_pass = True
                print(f"  --> RESULT: SUCCESS (Returned {result})")
            else:
                print(f"  --> RESULT: FAILURE (Expected {case.get('expected_result')}, got {result})")

        if not is_pass:
            all_passed = False
            print("--- STDOUT ---")
            print(stdout)
            print("--- STDERR ---")
            print(stderr)

    print("\n-----------------------------------------")
    if all_passed:
        print("All demonstration cases passed successfully!")
    else:
        print("One or more demonstration cases failed.")

if __name__ == '__main__':
    main()