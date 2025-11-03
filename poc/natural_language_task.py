"""
This file represents a task that cannot be solved by a formal refactoring.
It requires natural language understanding to interpret the TODO comment
and creative code generation to implement the requested feature.
"""

# TODO: Refactor this function to be more efficient by using a memoization cache.
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
