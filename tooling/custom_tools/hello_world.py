def hello_world(message: str):
    """Prints a message to the console."""
    print(f"Hello, {message}!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="The message to print.")
    args = parser.parse_args()
    hello_world(args.message)
