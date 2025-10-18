# Agent Protocols

_This document is auto-generated from protocol source files. Do not edit it directly._

## Protocol: aorp-header
_Defines the identity and versioning of the Advanced Orientation and Research Protocol (AORP)._

### Rules
- **aorp-identity**: The governing protocol set is identified as the Advanced Orientation and Research Protocol (AORP).
  - *Enforcement: Protocol is identified by its name in documentation and compiled artifacts.*
- **aorp-versioning**: The official protocol version is tracked in the VERSION file in the repository root, following Semantic Versioning (SemVer).
  - *Enforcement: Build or validation scripts should verify the presence and format of the VERSION file.*

---

## Protocol: core-directive-001
_The mandatory first action for any new task, ensuring a formal start to the Finite Development Cycle (FDC)._

### Rules
- **mandatory-fdc-start**: Upon receiving a new task, the agent's first action MUST be to programmatically execute the FDC 'start' command to formally initiate the task and run the AORP orientation cascade.
  - *Enforcement: This is a hard-coded behavior in the agent's core operational loop and is verified by the FDC toolchain.*

### Associated Tools
- `tooling/fdc_cli.py`

---

## Protocol: decidability-constraints-001
_Ensures all development processes are formally decidable and computationally tractable._

### Rules
- **non-turing-completeness**: The agent's planning and execution language is, by design, not Turing-complete. This is a fundamental constraint to guarantee that all processes will terminate.
  - *Enforcement: Enforced by the design of the plan runner and validated by the `lint` command in the FDC toolchain.*
- **bounded-recursion**: The agent MUST NOT generate plans that involve recursion or self-invocation. A plan cannot trigger another FDC or a sub-plan, with the sole exception of the 'Deep Research Cycle'.
  - *Enforcement: The `lint` command in `tooling/fdc_cli.py` scans plans for disallowed recursive calls.*
- **fsm-adherence**: All plans must be valid strings in the language defined by the tooling/fdc_fsm.json Finite State Machine.
  - *Enforcement: The `lint` command in `tooling/fdc_cli.py` validates the plan against the FSM definition.*

### Associated Tools
- `tooling/fdc_cli.py`
- `tooling/fdc_fsm.json`

---

## Protocol: orientation-cascade-001
_Defines the mandatory, four-tiered orientation cascade that must be executed at the start of any task to establish a coherent model of the agent's identity, environment, and the world state._

### Rules
- **l1-self-awareness**: Level 1 (Self-Awareness): The agent must first establish its own identity and inherent limitations by reading the `knowledge_core/agent_meta.json` artifact.
  - *Enforcement: The `start` command of the FDC toolchain executes this step and fails if the artifact is missing or invalid.*
- **l2-repository-sync**: Level 2 (Repository Sync): The agent must understand the current state of the local repository by loading primary artifacts from the `knowledge_core/` directory.
  - *Enforcement: The `start` command of the FDC toolchain executes this step.*
- **l3-environmental-probing**: Level 3 (Environmental Probing & Targeted RAG): The agent must discover the rules and constraints of its operational environment by executing a probe script and using targeted RAG to resolve 'known unknowns'.
  - *Enforcement: The `start` command of the FDC toolchain executes this step, utilizing tools like `google_search` and `view_text_website`.*
- **l4-deep-research-cycle**: Level 4 (Deep Research Cycle): To investigate 'unknown unknowns', the agent must initiate a formal, self-contained Finite Development Cycle (FDC) of the 'Analysis Modality'.
  - *Enforcement: This is a special case of recursion, explicitly allowed and managed by the FDC toolchain.*

### Associated Tools
- `tooling/environmental_probe.py`
- `google_search`
- `view_text_website`

---

## Protocol: fdc-protocol-001
_Defines the Finite Development Cycle (FDC), a formally defined process for executing a single, coherent task._

### Rules
- **fdc-entry-point**: The AORP cascade is the mandatory entry point to every FDC.
  - *Enforcement: Enforced by the `start` command in `tooling/fdc_cli.py`.*
- **fdc-state-transitions**: The FDC is a Finite State Machine (FSM) formally defined in `tooling/fdc_fsm.json`. Plans must be valid strings in the language defined by this FSM.
  - *Enforcement: Validated by the `lint` command in `tooling/fdc_cli.py`.*
- **phase1-deconstruction**: Phase 1 (Deconstruction & Contextualization): The agent must ingest the task, query historical logs, identify entities using the symbol map, and analyze impact using the dependency graph.
  - *Enforcement: Procedural step guided by the agent's core logic, using artifacts in `logs/` and `knowledge_core/`.*
- **phase2-planning**: Phase 2 (Planning & Self-Correction): The agent must generate a granular plan, lint it using the FDC toolchain, cite evidence for its steps, and perform a critical review.
  - *Enforcement: The `lint` command in `tooling/fdc_cli.py` is a mandatory pre-flight check.*
- **phase3-execution**: Phase 3 (Execution & Structured Logging): The agent must execute the validated plan and log every action according to the `LOGGING_SCHEMA.md`.
  - *Enforcement: Logging is performed by the agent's action execution wrapper.*
- **phase4-post-mortem**: Phase 4 (Pre-Submission Post-Mortem): The agent must formally close the task using the `close` command and complete the generated post-mortem report.
  - *Enforcement: The `close` command in `tooling/fdc_cli.py` initiates this phase.*

### Associated Tools
- `tooling/fdc_cli.py`
- `tooling/fdc_fsm.json`
- `knowledge_core/symbols.json`
- `knowledge_core/dependency_graph.json`
- `LOGGING_SCHEMA.md`
- `set_plan`
- `message_user`

---

## Protocol: standing-orders-001
_A set of non-negotiable, high-priority mandates that govern the agent's behavior across all tasks._

### Rules
- **aorp-mandate**: All Finite Development Cycles (FDCs) MUST be initiated using the FDC toolchain's 'start' command. This is non-negotiable.
  - *Enforcement: Enforced by the agent's core operational loop and the `start` command in `tooling/fdc_cli.py`.*
- **rag-mandate**: For any task involving external technologies, Just-In-Time External RAG is REQUIRED to verify current best practices. Do not trust internal knowledge.
  - *Enforcement: This is a core principle of the L3 orientation phase, utilizing tools like `google_search`.*
- **fdc-toolchain-mandate**: Use the `fdc_cli.py` tool for all core FDC state transitions: task initiation ('start'), plan linting ('lint'), and task closure ('close').
  - *Enforcement: The agent's internal logic is designed to prefer these specific tool commands for FDC state transitions.*

### Associated Tools
- `tooling/fdc_cli.py`
- `google_search`
- `view_text_website`

---

## Protocol: cfdc-protocol-001
_Defines the Context-Free Development Cycle (CFDC), a hierarchical planning and execution model._

### Rules
- **hierarchical-planning-via-call-plan**: Plans may execute other plans as sub-routines using the 'call_plan <path_to_plan>' directive. This enables a modular, hierarchical workflow.
  - *Enforcement: The plan validator must be able to parse this directive and recursively validate sub-plans. The execution engine must implement a plan execution stack to manage the context of nested calls.*
- **max-recursion-depth**: To ensure decidability, the plan execution stack must not exceed a system-wide constant, MAX_RECURSION_DEPTH. This prevents infinite recursion and guarantees all processes will terminate.
  - *Enforcement: The execution engine must check the stack depth before every 'call_plan' execution and terminate with a fatal error if the limit would be exceeded.*

### Associated Tools
- `tooling/master_control.py`
- `tooling/fdc_cli.py`

---

## Protocol: plan-registry-001
_Defines a central registry for discovering and executing hierarchical plans by a logical name._

### Rules
- **registry-definition**: A central plan registry MUST exist at 'knowledge_core/plan_registry.json'. It maps logical plan names to their file paths.
  - *Enforcement: The file's existence and format can be checked by the validation toolchain.*
- **registry-first-resolution**: The 'call_plan <argument>' directive MUST first attempt to resolve '<argument>' as a logical name in the plan registry. If resolution fails, it MUST fall back to treating '<argument>' as a direct file path for backward compatibility.
  - *Enforcement: This logic must be implemented in both the plan validator (`fdc_cli.py`) and the execution engine (`master_control.py`).*
- **registry-management-tool**: A dedicated tool (`tooling/plan_manager.py`) MUST be provided for managing the plan registry, with functions to register, deregister, and list plans.
  - *Enforcement: The tool's existence and functionality can be verified via integration tests.*

### Associated Tools
- `tooling/plan_manager.py`
- `tooling/master_control.py`
- `tooling/fdc_cli.py`

---

## Protocol: self-correction-protocol-001
_Defines the automated, closed-loop workflow for protocol self-correction._

### Rules
- **structured-lessons**: Lessons learned from post-mortem analysis must be generated as structured, machine-readable JSON objects in `knowledge_core/lessons.jsonl`.
  - *Enforcement: The `tooling/knowledge_compiler.py` script is responsible for generating lessons in the correct format.*
- **programmatic-updates**: All modifications to protocol source files must be performed programmatically via the `tooling/protocol_updater.py` tool to ensure consistency and prevent manual errors.
  - *Enforcement: Agent's core logic should be designed to use this tool for all protocol modifications.*
- **automated-orchestration**: The self-correction cycle must be managed by the `tooling/self_correction_orchestrator.py` script, which processes pending lessons and triggers the necessary updates.
  - *Enforcement: This script is the designated engine for the PDSC workflow.*
- **programmatic-rule-refinement**: The self-correction system can modify the description of existing protocol rules via the `update-rule` command in `tooling/protocol_updater.py`, allowing it to refine its own logic.
  - *Enforcement: The `tooling/knowledge_compiler.py` can generate `update-rule` actions, and the `tooling/self_correction_orchestrator.py` executes them.*
- **autonomous-code-suggestion**: The self-correction system can generate and apply code changes to its own tooling. This is achieved through a `PROPOSE_CODE_CHANGE` action, which is processed by `tooling/code_suggester.py` to create an executable plan.
  - *Enforcement: The `tooling/self_correction_orchestrator.py` invokes the code suggester when it processes a lesson of this type.*

### Associated Tools
- `tooling/knowledge_compiler.py`
- `tooling/protocol_updater.py`
- `tooling/self_correction_orchestrator.py`
- `tooling/code_suggester.py`
- `initiate_memory_recording`

---

## Protocol: research-protocol-001
_A protocol for conducting systematic research using the integrated research toolchain._

### Rules
- **mandate-research-tools**: For all complex research tasks, the `plan_deep_research` tool MUST be used to generate a plan, and the `execute_research_protocol` tool MUST be used for data gathering. This ensures a systematic and auditable research process.
  - *Enforcement: Adherence is monitored by the Code Review Critic and through post-mortem analysis of the activity log.*

### Associated Tools
- `tooling.research_planner.plan_deep_research`
- `tooling.research.execute_research_protocol`

---

## Protocol: self-modification-001
_A meta-protocol governing the agent's modification of its own governing protocols._

### Rules
- **source-only-modification**: The agent MUST NOT edit any 'AGENTS.md' file directly. All modifications to protocols must be made to the '.protocol.json' source files within the 'protocols/' directories.
  - *Enforcement: Procedural rule. The agent must demonstrate awareness of this by using tools like 'replace_with_git_merge_diff' or 'create_file_with_block' on source files, not build artifacts.*
- **rebuild-after-modification**: After modifying any '.protocol.json' source file, the agent MUST execute the main build script 'tooling/hierarchical_compiler.py' to regenerate all 'AGENTS.md' artifacts and the 'protocols.ttl' knowledge graph.
  - *Enforcement: The agent's plan for modifying protocols must include a final step to run the build script. This can be verified by reviewing the execution log.*
- **validation-is-mandatory**: Any new or modified protocol source file MUST be successfully validated against the 'protocols/protocol.schema.json'. The build process, which includes this validation, must complete without errors.
  - *Enforcement: The `hierarchical_compiler.py` script's successful execution serves as the enforcement mechanism.*
- **test-driven-protocol-development**: When adding or significantly altering a protocol, the agent SHOULD, where practical, create a temporary, illustrative test case (e.g., a deliberately invalid file) to prove the change has the intended effect and that the build system's error handling is robust.
  - *Enforcement: This is a best-practice guideline. Adherence can be checked during code review by observing the agent's workflow.*

### Associated Tools
- `tooling/hierarchical_compiler.py`
- `tooling/compiler.py`
- `tooling/knowledge_graph_generator.py`
- `protocols/protocol.schema.json`

---

## Protocol: deep-research-cycle-001
_A standardized, callable plan for conducting in-depth research on a complex topic._

### Rules
- **structured-research-phases**: The deep research plan MUST follow a structured four-phase process: Scoping, Broad Gathering, Targeted Extraction, and Synthesis.
  - *Enforcement: The plan's structure itself enforces this rule. The `lint` command can be extended to validate the structure of registered research plans.*

### Associated Tools
- `google_search`
- `view_text_website`
- `create_file_with_block`

---

## Protocol: research-fdc-001
_Defines the formal Finite Development Cycle (FDC) for conducting deep research._

### Rules
- **specialized-fsm**: The Research FDC must be governed by its own dedicated Finite State Machine, defined in `tooling/research_fsm.json`. This FSM is tailored for a research workflow, with states for gathering, synthesis, and reporting.
  - *Enforcement: The `master_control.py` orchestrator must load and execute plans against this specific FSM when initiating an L4 Deep Research Cycle.*
- **executable-plans**: Research plans must be generated by `tooling/research_planner.py` as valid, executable plans that conform to the `research_fsm.json` definition. They are not just templates but formal, verifiable artifacts.
  - *Enforcement: The output of the research planner must be linted and validated by the `fdc_cli.py` tool using the `research_fsm.json`.*
- **l4-invocation**: The L4 Deep Research Cycle is the designated mechanism for resolving complex 'unknown unknowns'. It is invoked by the main orchestrator when a task requires knowledge that cannot be obtained through simple L1-L3 orientation probes.
  - *Enforcement: The `master_control.py` orchestrator is responsible for triggering the L4 cycle.*

### Associated Tools
- `tooling/master_control.py`
- `tooling/research_planner.py`
- `tooling/research.py`
- `tooling/fdc_cli.py`

---
