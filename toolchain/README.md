# Paraconsistent Resolver Toolchain

This directory contains the tools for programmatically resolving a "Constructive Contradiction" between different versions of source code based on a declared meta-semantic `Stance`.

## Components

### `resolver.py`

This is the core script of the toolchain. It is responsible for selecting and generating the final, resolved version of the code.

**Logic:**
1.  It reads a `config.json` file to determine the paths to the contradictory code versions (`version-A`, `version-B`, etc.).
2.  It determines the resolution `Stance` by first checking for a command-line `--stance` argument. If none is provided, it falls back to the `resolve_with_stance` key in the `config.json` file.
3.  It reads the source code of the version corresponding to the chosen `Stance`.
4.  Crucially, it parses this source code into an **Abstract Syntax Tree (AST)** using Python's `ast` module.
5.  It then "unparses" this AST back into syntactically valid Python code. This AST-based process is more robust than simple file copying and ensures the output is always well-formed.
6.  Finally, it writes the regenerated code to the output path specified in `config.json`.

### `config.json`

This file configures the behavior of the resolver.

-   `versions`: An object mapping a version identifier (e.g., "version-A") to the file path of that version.
-   `resolved_path`: The file path where the final, resolved code will be written.
-   `resolve_with_stance`: The default `Stance` to use if one is not provided via the command line.

## Automation

This toolchain is designed to be run from CI/CD. The `.github/workflows/trigger-resolution.yml` workflow automates this process by:
1.  Allowing a user to specify a `Stance` when triggering the workflow.
2.  Checking out the correct branch.
3.  Executing `resolver.py` with the chosen `Stance` as a command-line argument.
4.  Committing the resulting `resolved/logic.py` file back to the branch.