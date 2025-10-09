# System Documentation

---

## `tooling/` Directory

### `tooling/dependency_graph_generator.py`

_No module-level docstring found._

### `tooling/doc_generator.py`

_No module-level docstring found._

### `tooling/environmental_probe.py`

_No module-level docstring found._

### `tooling/fdc_cli.py`

Provides the command-line interface for the Finite Development Cycle (FDC).

This script is a core component of the agent's protocol, offering tools to ensure
that all development work is structured, verifiable, and safe. It is used by both
the agent to signal progress and the `master_control.py` orchestrator to
validate the agent's plans before execution.

The CLI provides several key commands:
- `close`: Logs the formal end of a task, signaling to the orchestrator that
  execution is complete.
- `validate`: Performs a deep validation of a plan file against the FDC's Finite
  State Machine (FSM) definition. It checks for both syntactic correctness (Is
  the sequence of operations valid?) and semantic correctness (Does the plan try
  to use a file before creating it?).
- `analyze`: Reads a plan and provides a high-level analysis of its
  characteristics, such as its computational complexity and whether it is a
  read-only or read-write plan.
- `lint`: A comprehensive "linter" that runs a full suite of checks on a plan
  file, including `validate`, `analyze`, and checks for disallowed recursion.

### `tooling/knowledge_compiler.py`

_No module-level docstring found._

### `tooling/master_control.py`

_No module-level docstring found._

### `tooling/protocol_auditor.py`

_No module-level docstring found._

### `tooling/protocol_compiler.py`

_No module-level docstring found._

### `tooling/research.py`

_No module-level docstring found._

### `tooling/research_planner.py`

_No module-level docstring found._

### `tooling/self_improvement_cli.py`

_No module-level docstring found._

### `tooling/state.py`

_No module-level docstring found._

### `tooling/symbol_map_generator.py`

_No module-level docstring found._

### `tooling/test_dependency_graph_generator.py`

_No module-level docstring found._

### `tooling/test_knowledge_compiler.py`

_No module-level docstring found._

### `tooling/test_master_control.py`

_No module-level docstring found._

### `tooling/test_self_improvement_cli.py`

_No module-level docstring found._

### `tooling/test_symbol_map_generator.py`

_No module-level docstring found._

---

## `utils/` Directory

### `utils/logger.py`

_No module-level docstring found._

### `utils/test_logger.py`

_No module-level docstring found._