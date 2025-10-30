# Protocol: Comprehensive Testing

This protocol mandates a comprehensive testing strategy to ensure code quality and stability.

## The Problem: Inadequate Testing

Without a formal testing protocol, it's easy for bugs to slip through, for code quality to degrade, and for regressions to occur. This can lead to a fragile and unreliable system.

## The Solution: A Multi-Layered Testing Approach

This protocol requires a multi-layered testing approach, including unit, integration, and end-to-end tests.

**Rule `testing-protocol-001`**: Before any code is submitted, the following conditions must be met:
1.  **Unit Tests**: All new functions and classes must have corresponding unit tests.
2.  **Integration Tests**: All new modules must have integration tests that verify their interactions with other modules.
3.  **End-to-End Tests**: All new features must have end-to-end tests that verify their functionality from the user's perspective.
4.  **All Tests Pass**: All tests in the test suite must pass.
