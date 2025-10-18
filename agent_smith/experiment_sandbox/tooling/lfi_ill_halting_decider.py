"""
A tool for analyzing the termination of LFI-ILL programs.

This script takes an LFI-ILL file, interprets it in a paraconsistent logic
environment, and reports on its halting status. It does this by setting up
a paradoxical initial state and observing how the program resolves it.
"""
import argparse
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfi_ill import Lexer, Parser, Interpreter, ParaconsistentTruth, ParaconsistentState

class LfiIllHaltingDecider:
    def __init__(self, lfi_ill_file):
        self.lfi_ill_file = lfi_ill_file

    def analyze(self):
        """
        Analyzes the LFI ILL program for termination.
        """
        try:
            with open(self.lfi_ill_file, 'r') as f:
                lfi_ill_code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at {self.lfi_ill_file}")
            return

        lexer = Lexer(lfi_ill_code)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)

        # We need to set up the initial state to be paradoxical.
        # We will do this by setting the 'halt' variable to BOTH.
        # We will create a paradoxical value by creating a state that is both true and false,
        # but with a concrete value that represents the two branches of the paradox.
        interpreter.environment['halt'] = ParaconsistentState(ParaconsistentTruth.BOTH, {"tag": "inl", "value": ParaconsistentState(ParaconsistentTruth.TRUE)})

        result = interpreter.interpret()

        print(f"The final state of the program is: {result}")

        if result.value == ParaconsistentTruth.BOTH:
            print("The program is paradoxical. It both halts and does not halt.")
        elif result.value == ParaconsistentTruth.TRUE:
            print("The program halts.")
        elif result.value == ParaconsistentTruth.FALSE:
            print("The program does not halt.")
        else: # NEITHER
            print("The halting status of the program could not be determined.")

def main():
    parser = argparse.ArgumentParser(description="Analyze an LFI ILL program for termination.")
    parser.add_argument("file", help="The LFI ILL file to analyze.")
    args = parser.parse_args()

    decider = LfiIllHaltingDecider(args.file)
    decider.analyze()

if __name__ == "__main__":
    main()