# pLLLU: Paraconsistent and Paracomplete Light Linear Logic

This repository contains a Python implementation of a **P**araconsistent and **P**aracomplete **L**ight **L**inear **L**ogic of **U**ndeterminedness (pLLLU). This logic is designed to handle reasoning in environments with incomplete and contradictory information, while also being sensitive to computational resources.

## Key Features

*   **Paraconsistent:** The logic can tolerate contradictions (gluts) without leading to triviality (explosion). This is managed by a paraconsistent negation (`¬`) and a consistency operator (`∘`).
*   **Paracomplete:** The logic can handle informational gaps (incompleteness). This is managed by a paracomplete/determinedness operator (`~`).
*   **Resource-Sensitive:** Based on Light Linear Logic, the system is designed with computational complexity in mind, aiming for polynomial-time decidability.
*   **Four-Valued Semantics:** The interpreter uses a four-valued logic (TRUE, FALSE, BOTH, NEITHER) based on First-Degree Entailment (FDE) to evaluate formulas.

## Getting Started

### Prerequisites

*   Python 3
*   `ply` (Python Lex-Yacc)

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  Install the required dependency:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Interpreter

The interpreter can be run from the command line using the `run` command in the `Makefile`. You need to provide a path to a file containing a pLLLU formula.

1.  Create a file (e.g., `test.plllu`) with a formula:
    ```
    ~ (a ⊗ ¬ a)
    ```

2.  Run the interpreter:
    ```bash
    make run file=test.plllu
    ```

This will parse the formula, evaluate it using the interpreter, and print the AST and the final truth value.

## Project Structure

*   `plllu/`: Contains the core implementation of the logic.
    *   `lexer.py`: Defines the tokens for the language.
    *   `parser.py`: Defines the grammar and builds the AST.
    *   `ast.py`: Defines the Abstract Syntax Tree nodes.
    *   `interpreter.py`: Implements the four-valued interpreter for the logic.
    *   `run_plllu.py`: A command-line wrapper for the interpreter.
*   `tests/`: Contains unit tests for the interpreter.
*   `Makefile`: Provides simple commands for running tests and the interpreter.
*   `requirements.txt`: Lists the project dependencies.