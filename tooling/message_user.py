import sys

def main():
    """
    A dummy tool that prints its arguments.
    This is to simulate the message_user tool for testing purposes.
    """
    if len(sys.argv) > 1:
        print(f"[Message User]: {sys.argv[1]}")

if __name__ == "__main__":
    main()