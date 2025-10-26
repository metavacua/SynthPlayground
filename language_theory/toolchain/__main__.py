import argparse
import sys

def main():
    """
    Main entry point for the Language Theory Toolchain.
    This script dispatches commands to the various tools in the toolchain.
    """
    parser = argparse.ArgumentParser(
        description="A unified toolchain for language theory analysis and refactoring.",
        usage="python -m language_theory.toolchain <command> [<args>]"
    )
    parser.add_argument("command", help="The tool to run (classify, recognize, complexity, refactor, equivalence).")

    # This is a bit of a trick to parse the command and then pass the rest
    # of the arguments to the subcommand's own parser.
    args = parser.parse_args(sys.argv[1:2])

    if not hasattr(sys.modules[__name__], f'run_{args.command}'):
        print(f"Unrecognized command: {args.command}")
        parser.print_help()
        sys.exit(1)

    # Call the appropriate run function
    getattr(sys.modules[__name__], f'run_{args.command}')(sys.argv[2:])

def run_classify(argv):
    from . import classifier
    sys.argv = ['-m language_theory.toolchain.classifier'] + argv
    classifier.main()

def run_recognize(argv):
    from . import recognizer
    sys.argv = ['-m language_theory.toolchain.recognizer'] + argv
    recognizer.main()

def run_complexity(argv):
    from . import complexity
    sys.argv = ['-m language_theory.toolchain.complexity'] + argv
    complexity.main()

def run_refactor(argv):
    from . import refactor
    sys.argv = ['-m language_theory.toolchain.refactor'] + argv
    refactor.main()

def run_equivalence(argv):
    from . import equivalence
    sys.argv = ['-m language_theory.toolchain.equivalence'] + argv
    equivalence.main()

if __name__ == "__main__":
    main()
