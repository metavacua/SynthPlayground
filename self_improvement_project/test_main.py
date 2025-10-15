import unittest
import main

class TestFizzBuzz(unittest.TestCase):

    def test_fizz(self):
        self.assertEqual(main.fizzbuzz(3), "Fizz")
        self.assertEqual(main.fizzbuzz(6), "Fizz")

    def test_buzz(self):
        self.assertEqual(main.fizzbuzz(5), "Buzz")
        self.assertEqual(main.fizzbuzz(10), "Buzz")

    def test_fizzbuzz(self):
        self.assertEqual(main.fizzbuzz(15), "FizzBuzz")
        self.assertEqual(main.fizzbuzz(30), "FizzBuzz")

    def test_number(self):
        self.assertEqual(main.fizzbuzz(1), 1)
        self.assertEqual(main.fizzbuzz(2), 2)
        self.assertEqual(main.fizzbuzz(4), 4)

    def test_fibonacci(self):
        self.assertEqual(main.fibonacci(0), 0)
        self.assertEqual(main.fibonacci(1), 1)
        self.assertEqual(main.fibonacci(10), 55)

if __name__ == '__main__':
    unittest.main()