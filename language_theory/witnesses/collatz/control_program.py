# The control program for the Collatz sequence.
# This program is not guaranteed to terminate.

from .collatz_total import collatz_total

def control_program(n, initial_fuel=10):
    """
    This program orchestrates the Collatz sequence computation.
    It is not guaranteed to terminate for all inputs.
    """
    current_n = n
    fuel = initial_fuel

    while current_n != 1:
        current_n = collatz_total(current_n, fuel)
        if current_n != 1:
            # Decide whether to allocate more fuel or give up.
            # For this example, we'll just double the fuel.
            fuel *= 2

    return current_n

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m language_theory.witnesses.collatz.control_program <n>")
        sys.exit(1)
    n = int(sys.argv[1])
    result = control_program(n)
    print(f"Result: {result}")
