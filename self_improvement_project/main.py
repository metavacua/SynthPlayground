def fizzbuzz(n):
    """
    This function implements the FizzBuzz logic.
    For multiples of 3, it returns "Fizz".
    For multiples of 5, it returns "Buzz".
    For multiples of both 3 and 5, it returns "FizzBuzz".
    Otherwise, it returns the number.
    """
    return "Fizz" * (n % 3 == 0) + "Buzz" * (n % 5 == 0) or n

if __name__ == "__main__":
    for i in range(1, 101):
        print(fizzbuzz(i))