"""
A dummy tool that prints its arguments to simulate the message_user tool.

This script is a simple command-line utility that takes a string as an
argument and prints it to standard output, prefixed with "[Message User]:".
Its purpose is to serve as a stand-in or mock for the actual `message_user`
tool in testing environments where the full agent framework is not required.

This allows for the testing of scripts or workflows that call the
`message_user` tool without needing to invoke the entire agent messaging
subsystem.
"""
import sys

def main():
    """
    Prints the first command-line argument to simulate a user message.
    """
    if len(sys.argv) > 1:
        print(f"[Message User]: {sys.argv[1]}")

if __name__ == "__main__":
    main()