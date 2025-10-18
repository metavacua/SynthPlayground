# Protocol: pLLLU Execution

This protocol establishes `tooling/plllu_runner.py` as the official entry point for executing pLLLU (`.plllu`) files.

**Rule `plllu-runner-is-entry-point`**: All pLLLU files must be executed through the `plllu_runner.py` script to ensure they are run in a controlled, programmatic environment.