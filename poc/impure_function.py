"""
This file contains an impure function that will be used to test the
'prove_purity' capability of the Sentinel Agent.
"""

def add_and_log(a, b):
    """
    This function is impure because it has a side effect: writing to a file.
    """
    result = a + b
    with open("log.txt", "a") as f:
        f.write(f"{a} + {b} = {result}\n")
    return result
