# A total function that computes one step of the Collatz sequence.
# This function is guaranteed to terminate.

def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def collatz_total(n, fuel):
    """
    Computes the Collatz sequence for a given n, with a 'fuel' limit.
    This function is a total function, guaranteed to terminate.
    """
    if fuel <= 0:
        return n

    current_n = n
    for _ in range(fuel):
        if current_n == 1:
            break
        current_n = collatz_step(current_n)
    return current_n

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m language_theory.witnesses.collatz.collatz_total <n> <fuel>")
        sys.exit(1)
    n = int(sys.argv[1])
    fuel = int(sys.argv[2])
    result = collatz_total(n, fuel)
    print(f"Result: {result}")
