"""
A simple, local simulation of the `message_user` tool.

In a real agent execution environment, the `message_user` tool would be a
special function provided by the environment to communicate with the end-user.
This script provides a lightweight, standalone equivalent for local testing
and development.

Its sole purpose is to take a string as a command-line argument and print it
to standard output, prefixed with "[Message User]:". This allows developers to
test plans and scripts that involve user communication without needing the full
agent framework.
"""
import sys

def main():
    if len(sys.argv) > 1:
        print(f"[Message User]: {sys.argv[1]}")

if __name__ == "__main__":
    main()