import argparse
import subprocess
import re

def prove_sequent(sequent_string):
    """
    Calls the HDL Lisp prover to determine if a sequent is provable.

    Args:
        sequent_string: A string representing the sequent in Lisp format,
                      e.g., "'(() (con))'".

    Returns:
        A boolean indicating whether the sequent is provable, or None on error.
    """
    lisp_executable = "sbcl"  # Or "clisp", depending on the environment
    prover_script = "HDLProvev7.lsp"

    # Construct the Lisp expression to execute.
    # We wrap everything in a `progn` block to treat it as a single expression.
    lisp_code = f"""
    (progn
        (load "{prover_script}")
        (if (entails {sequent_string})
            (format t "FINAL_RESULT_PROVABLE")
            (format t "FINAL_RESULT_NOT_PROVABLE"))
        (quit))
    """

    try:
        # Execute the Lisp interpreter as a subprocess
        result = subprocess.run(
            [lisp_executable, "--non-interactive", "--eval", lisp_code],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"Lisp interpreter error:\n{result.stderr}")
            return None

        # The output is messy because of the prints in the Lisp script.
        # We look for the unique final tag.
        if "FINAL_RESULT_PROVABLE" in result.stdout:
            return True
        elif "FINAL_RESULT_NOT_PROVABLE" in result.stdout:
            return False
        else:
            print(f"Could not parse prover output:\n{result.stdout}")
            return None

    except FileNotFoundError:
        print(f"Error: Lisp interpreter '{lisp_executable}' not found.")
        print("Please ensure Common Lisp is installed and in the system's PATH.")
        return None
    except subprocess.TimeoutExpired:
        print("Error: Lisp prover timed out.")
        return None

def main():
    """
    Provides a command-line interface for the HDL prover tool.
    """
    parser = argparse.ArgumentParser(description="HDL Prover Tool")
    parser.add_argument("sequent", type=str, help="The sequent to prove, in Lisp format (e.g., \"'(() (con))\").")
    args = parser.parse_args()

    is_provable = prove_sequent(args.sequent)

    if is_provable is True:
        print("Result: The sequent is PROVABLE.")
    elif is_provable is False:
        print("Result: The sequent is NOT PROVABLE.")
    else:
        print("Result: An error occurred during proof checking.")

if __name__ == "__main__":
    main()