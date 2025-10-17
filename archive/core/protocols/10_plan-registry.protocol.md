# Protocol: The Plan Registry

This protocol introduces a Plan Registry to create a more robust, modular, and discoverable system for hierarchical plans. It decouples the act of calling a plan from its physical file path, allowing plans to be referenced by a logical name.

## The Problem with Path-Based Calls

The initial implementation of the Context-Free Development Cycle (CFDC) relied on direct file paths (e.g., `call_plan path/to/plan.txt`). This is brittle:
- If a registered plan is moved or renamed, all plans that call it will break.
- It is difficult for an agent to discover and reuse existing, validated plans.

## The Solution: A Central Registry

The Plan Registry solves this by creating a single source of truth that maps logical, human-readable plan names to their corresponding file paths.

- **Location:** `knowledge_core/plan_registry.json`
- **Format:** A simple JSON object of key-value pairs:
  ```json
  {
    "logical-name-1": "path/to/plan_1.txt",
    "run-all-tests": "plans/common/run_tests.txt"
  }
  ```

## Updated `call_plan` Logic

The `call_plan` directive is now significantly more powerful. When executing `call_plan <argument>`, the system will follow a **registry-first** approach:

1.  **Registry Lookup:** The system will first treat `<argument>` as a logical name and look it up in `knowledge_core/plan_registry.json`.
2.  **Path Fallback:** If the name is not found in the registry, the system will fall back to treating `<argument>` as a direct file path. This ensures full backward compatibility with existing plans.

## Management

A new tool, `tooling/plan_manager.py`, will be introduced to manage the registry with simple commands like `register`, `deregister`, and `list`, making it easy to maintain the library of reusable plans.