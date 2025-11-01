import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(
        description="Detects and removes unused imports from Python files."
    )
    parser.add_argument(
        "file",
        nargs="*",
        help="The file to process.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply the changes to the files.",
    )
    args = parser.parse_args()

    command = ["autoflake", "--remove-all-unused-imports"]
    if args.fix:
        command.append("--in-place")

    command.extend(args.file)

    subprocess.run(command)


if __name__ == "__main__":
    main()
