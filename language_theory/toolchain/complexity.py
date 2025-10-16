import sys
import argparse
import importlib.util
import os


class ComplexityTracer:
    """A tracer to count Python instructions executed."""

    def __init__(self):
        self.instruction_count = 0

    def trace_dispatch(self, frame, event, arg):
        # We are interested in the 'line' event, which occurs for each line of code.
        if event == "line":
            self.instruction_count += 1
        return self.trace_dispatch

    def run_and_trace(self, target_module_str, script_args):
        """Runs a target module with tracing enabled using runpy."""
        # Store original sys.argv and replace it for the target script
        original_argv = sys.argv
        sys.argv = [target_module_str] + script_args

        try:
            # Set the tracer just before running the module
            sys.settrace(self.trace_dispatch)

            # Use runpy to execute the module in a way that respects packages
            import runpy

            runpy.run_module(target_module_str, run_name="__main__")

        finally:
            # Crucially, turn off tracing and restore the system state
            sys.settrace(None)
            sys.argv = original_argv

        return self.instruction_count


def main():
    """
    Main function for the complexity analyzer.
    This script takes another Python script and its arguments as input,
    runs it, and reports the number of instructions executed.
    """
    parser = argparse.ArgumentParser(
        description="A Blum-compliant complexity analyzer that measures instruction counts.",
        epilog="Example: python -m language_theory.toolchain.complexity language_theory.toolchain.recognizer language_theory/witnesses/regular/right_linear_grammar.txt aabb",
    )
    parser.add_argument(
        "target_module",
        help="The Python module to analyze (e.g., my_package.my_module).",
    )
    parser.add_argument(
        "script_args", nargs=argparse.REMAINDER, help="Arguments for the target module."
    )

    args = parser.parse_args()

    print(
        f"--- Complexity Analysis for: python -m {args.target_module} {' '.join(args.script_args)} ---"
    )

    tracer = ComplexityTracer()
    try:
        # Suppress the output of the target script to keep the analysis clean
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

        total_instructions = tracer.run_and_trace(args.target_module, args.script_args)

        sys.stdout = original_stdout  # Restore stdout
        print("\n--- Analysis Complete ---")
        print(f"Φ_instr (Instruction Count): {total_instructions}")
        print("-------------------------")

    except Exception as e:
        print(f"\nAn error occurred during traced execution: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
