# Protocol: Dependency Management

This protocol establishes a formal process for managing Python dependencies to ensure a reliable and repeatable execution environment.

## The Problem: Environmental Brittleness

The agent's operating environment previously lacked a formal dependency declaration. This required manual, trial-and-error installation of necessary packages (`jsonschema`, `rdflib`, `requests`) upon encountering `ModuleNotFoundError` exceptions. This process is inefficient, error-prone, and makes the successful execution of tasks dependent on undocumented, ad-hoc environmental setup.

## The Solution: Formal Dependency Declaration and Installation

To solve this, two components are introduced:

1.  **`requirements.txt`:** A standard `requirements.txt` file is added to the repository root. This file serves as the single source of truth for all required Python packages.
2.  **A New Protocol Rule:** A new rule, `dependency-install-on-start`, is established. This rule mandates that upon starting any task, the agent's first action *after* reading `AGENTS.md` should be to install the dependencies listed in `requirements.txt` using `pip`.

This protocol transforms dependency management from an ad-hoc, reactive process into a proactive, automated, and verifiable step in the agent's workflow, significantly improving its robustness and reliability.