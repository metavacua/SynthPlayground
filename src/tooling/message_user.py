"""
A dummy tool that prints its arguments.
This is to simulate the message_user tool for testing purposes.
"""
import sys

def main():
    """
    Prints the first command-line argument to stdout, simulating a message
    to the user.
    """
    if len(sys.argv) > 1:
        print(f"[Message User]: {sys.argv[1]}")

if __name__ == "__main__":
    main()