# Known Issues

This document lists known issues in the repository that are not currently being addressed.

## `test_aura_executor.py` Test Failure

-   **Issue:** The test `test_integration_demo_end_to_end_subprocess` in `tests/test_aura_executor.py` is failing.
-   **Description:** This test runs the `aura_executor.py` script as a subprocess to verify its end-to-end functionality. After the major refactoring that moved all source code into a `src/` directory, this test began to fail. The root cause appears to be a `ModuleNotFoundError` within the `aura_lang` package when the script is run as a subprocess, which indicates an issue with Python's import system in that specific context.
-   **Attempts to Fix:**
    -   Converted all imports in the `aura_lang` package to be relative.
    -   Attempted various methods of capturing the subprocess output, including redirecting stderr.
    -   Verified that all other tests, including those for the `hdl_prover` that is called by the `aura` script, are passing.
-   **Status:** As per user guidance, this issue is being documented and will not be addressed at this time to avoid getting stuck on a complex, isolated problem. The test has been left in its failing state to serve as a record of this issue.