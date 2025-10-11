# Contributing to Project Chimera

Thank you for your interest in contributing to Project Chimera! This document outlines the key guidelines and procedures for contributing to this project.

## Core Philosophy: Protocol as Code

This project operates on a "protocol as code" philosophy. This means that the agent's behavior, our development processes, and our standards are all defined in machine-readable files located in the `protocols/` directory. These are compiled into the `AGENTS.md` file, which serves as the single source of truth.

**Do not edit `AGENTS.md`, `README.md`, or `SECURITY.md` directly.** These are build artifacts. All changes must be made to the source files.

## Getting Started

1.  **Install Dependencies:**
    ```bash
    make install
    ```

2.  **Build All Artifacts:**
    To ensure your environment is up-to-date, run the main build command. This will generate the `AGENTS.md`, `README.md`, and other documentation.
    ```bash
    make build
    ```

## Making Changes

1.  **Modify Source Files:** Make your changes to the relevant source files (e.g., Python files in `tooling/` or protocol files in `protocols/`).
2.  **Format Your Code:**
    ```bash
    make format
    ```
3.  **Lint Your Code:**
    ```bash
    make lint
    ```
4.  **Run Tests:**
    Ensure all existing tests pass before submitting your changes.
    ```bash
    make test
    ```
5.  **Rebuild Artifacts:**
    After making changes, always rebuild the documentation and protocol artifacts to reflect your changes.
    ```bash
    make build
    ```

## Submitting a Pull Request

Before submitting a pull request, please ensure you have:
- Read and understood the protocols in `AGENTS.md`.
- Followed the coding and style conventions.
- Run all formatters, linters, and tests.
- Updated any relevant documentation or protocol source files.
- Ensured that `make build` runs successfully with your changes.