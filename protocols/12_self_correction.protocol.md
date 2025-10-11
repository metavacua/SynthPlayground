# Protocol: The Closed-Loop Self-Correction Cycle

This protocol describes the automated workflow that enables the agent to programmatically improve its own governing protocols based on new knowledge. It transforms the ad-hoc, manual process of learning into a reliable, machine-driven feedback loop.

## The Problem: The Open Loop

Previously, "lessons learned" were compiled into a simple markdown file, `knowledge_core/lessons_learned.md`. While this captured knowledge, it was a dead end. There was no automated process to translate these text-based insights into actual changes to the protocol source files. This required manual intervention, creating a significant bottleneck and a high risk of protocols becoming stale.

## The Solution: A Protocol-Driven Self-Correction (PDSC) Workflow

The PDSC workflow closes the feedback loop by introducing a set of new tools and structured data formats that allow the agent to enact its own improvements.

**1. Structured, Actionable Lessons (`knowledge_core/lessons.jsonl`):**
- Post-mortem analysis now generates lessons as structured JSON objects, not free-form text.
- Each lesson includes a machine-readable `action` field, which contains a specific, executable command.

**2. The Protocol Updater (`tooling/protocol_updater.py`):**
- A new, dedicated tool for programmatically modifying the protocol source files (`*.protocol.json`).
- It accepts commands like `add-tool`, allowing for precise, automated changes to protocol definitions.

**3. The Orchestrator (`tooling/self_correction_orchestrator.py`):**
- This script is the engine of the cycle. It reads `lessons.jsonl`, identifies pending lessons, and uses the `protocol_updater.py` to execute the defined actions.
- After applying a lesson, it updates the lesson's status, creating a clear audit trail.
- It finishes by running `make AGENTS.md` to ensure the changes are compiled into the live protocol.

This new, automated cycle—**Analyze -> Structure Lesson -> Execute Correction -> Re-compile Protocol**—is a fundamental step towards autonomous self-improvement.