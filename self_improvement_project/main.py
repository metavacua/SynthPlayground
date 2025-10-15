def fizzbuzz(n):
    """
    This function implements the FizzBuzz logic.
    For multiples of 3, it returns "Fizz".
    For multiples of 5, it returns "Buzz".
    For multiples of both 3 and 5, it returns "FizzBuzz".
    Otherwise, it returns the number.
    """
    return "Fizz" * (n % 3 == 0) + "Buzz" * (n % 5 == 0) or n

def fibonacci(n):
    """
    Calculates the nth Fibonacci number.
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers.")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

if __name__ == "__main__":
    for i in range(1, 101):
        print(fizzbuzz(i))