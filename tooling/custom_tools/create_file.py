import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description="Create a file with the given content."
    )
    parser.add_argument(
        "--filename", required=True, help="The name of the file to create."
    )
    parser.add_argument(
        "--content", required=True, help="The content to write to the file."
    )
    args = parser.parse_args()

    with open(args.filename, "w") as f:
        f.write(args.content)

    print(json.dumps({"filename": args.filename}))


if __name__ == "__main__":
    main()
