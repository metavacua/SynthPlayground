# Protocol: Test-Driven Development (TDD)

This protocol mandates the use of Test-Driven Development for all new code.

## The Problem: Untested Code

Writing code without first writing a test can lead to several problems:
*   **Bugs:** Code is more likely to have bugs if it's not tested from the start.
*   **Unclear Requirements:** Writing a test first forces you to think through the requirements and design of the code.
*   **Difficult to Refactor:** Code without tests is difficult to refactor safely, as there's no way to know if you've broken something.

## The Solution: Test First

This protocol requires that a test is written before any new code.

**Rule `tdd-writing-new-code`**: When writing any new function or class, a corresponding test must be written first. The test should fail before the new code is implemented, and pass after.

This ensures that:
1.  All new code is testable by design.
2.  The codebase maintains a high level of test coverage.
3.  The development process is more robust and less prone to regressions.