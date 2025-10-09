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

### `tooling/execution_wrapper.py`

**Purpose:**
This script is the **single point of entry** for executing all tool actions within the agent's environment. It acts as a centralized wrapper that ensures every action is robustly logged before and after execution. This is the core component of the enforced logging protocol.

**Core Function:**
- `execute_and_log_action(tool_name, args_list, task_id, plan_step)`: The main function that orchestrates the execution and logging of a single tool call.

**Workflow:**
1.  **Instantiate Logger:** It creates an instance of the `Logger` from `utils/logger.py`.
2.  **Log `IN_PROGRESS`:** It immediately logs that a tool execution is starting.
3.  **Dispatch and Execute:** It looks up the requested `tool_name` in its `TOOL_DISPATCHER` dictionary and calls the corresponding internal function (e.g., `_list_files`, `_read_file`).
4.  **Safe Execution:** The tool call is wrapped in a `try...except` block to gracefully handle any errors.
5.  **Log Final Outcome:**
    -   On success, it logs a `SUCCESS` event, including any return value from the tool as a JSON string.
    -   On failure, it logs a `FAILURE` event, including the exception message and a full stack trace.

**Usage:**
This script is not intended to be run directly by a user. It is called as a subprocess by `tooling/master_control.py` for every step in an agent's plan.
```bash
python3 tooling/execution_wrapper.py --tool <tool_name> --args '[arg1, arg2]' --task-id <task_id> --plan-step <step_num>
```

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