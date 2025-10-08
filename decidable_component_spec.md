# Decidable Component Specification v1.0

## 1. Overview

A "Decidable Component" is a self-contained, verifiable implementation of a feature or module. It is "decidable" because it provides all the necessary metadata for an automated system to verify its integrity and understand its properties without human intervention. This specification defines the structure of the `manifest.json` file, which is the core of a decidable component.

Every decidable component **MUST** contain a `manifest.json` file at its root.

## 2. `manifest.json` Structure

The `manifest.json` file is a JSON object with the following required fields:

### 2.1. `stance`

-   **Type:** `String`
-   **Description:** Declares the primary meta-property that the component embodies. This is the key property used by the "Decider" engine to resolve contradictions based on a resolution policy.
-   **Example:** `"Safety"`, `"Completeness"`, `"Performance"`, `"Security"`

### 2.2. `provides`

-   **Type:** `String`
-   **Description:** A path, relative to the component's root, to the primary artifact that this component provides. In a code context, this would typically be the main source file that should be used if this component is chosen as the winner of a resolution.
-   **Example:** `"logic.py"`, `"bin/app.jar"`

### 2.3. `verification_command`

-   **Type:** `String`
-   **Description:** A shell command that, when executed from the component's root directory, verifies the component's integrity. A successful verification **MUST** exit with a status code of `0`. Any other exit code signifies that the component is invalid, has failed its tests, or is otherwise refuted.
-   **Example:** `"bash verify.sh"`, `"npm test"`, `"mvn clean install"`

## 3. Example `manifest.json`

```json
{
  "stance": "Safety",
  "provides": "logic.py",
  "verification_command": "python3 -m unittest discover tests"
}
```

This manifest declares that the component embodies the "Safety" stance, its primary artifact is `logic.py`, and it can be verified by running the `unittest` command. An automated "Decider" engine can now use this information to process this component as part of a finite paraconsistent development cycle.