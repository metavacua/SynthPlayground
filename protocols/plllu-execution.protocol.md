# Protocol: pLLLU Execution

This protocol establishes the `plllu_runner.py` script as the official entry point for executing pLLLU (`.plllu`) files.

## The Problem: Lack of a Standard Runner

The pLLLU language provides a powerful way to define complex logic, but without a standardized execution tool, there is no reliable way to integrate these files into the agent's workflow.

## The Solution: A Dedicated Runner

This protocol mandates the use of `tooling/plllu_runner.py` for all pLLLU file executions.

**Rule `plllu-runner-is-entry-point`**: All pLLLU files must be executed through the `plllu_runner.py` script.

This ensures that every pLLLU file is executed in a controlled, programmatic environment.