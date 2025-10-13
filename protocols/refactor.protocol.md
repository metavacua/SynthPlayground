# Protocol: Code Refactoring

This protocol defines the use of the `refactor.py` tool, which provides a simple way to perform automated refactoring of Python code.

## Rule: `refactor-rename-symbol`

The `refactor.py` tool can be used to rename a symbol (a function or class) and all of its references within a given search path.

**Usage:**
```
python tooling/refactor.py --filepath <path_to_file> --old-name <old_symbol_name> --new-name <new_symbol_name> [--search-path <path>]
```

The tool will generate a plan file containing a series of `replace_with_git_merge_diff` commands to perform the renaming. This plan can then be executed by the agent's master controller.