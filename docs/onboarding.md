# Onboarding Guide: Welcome to the Self-Improving Agent Repository

Welcome! This guide is designed to help you understand the structure and core concepts of this repository. Our goal is to maintain a sophisticated, self-improving AI agent, and your contributions are key to that mission.

## 1. Core Philosophy: Structured Self-Improvement

This is not a typical software project. The primary goal is the continuous, automated improvement of the agent itself. This is achieved through a set of core protocols and feedback loops, which are the "source code" of the agent's behavior.

- **Read This First:** The `AGENTS.md` file is the most important document in this repository. It is the compiled, human-readable version of all the agent's operational protocols. Before you do anything else, skim this file to understand the "rules of the game."

## 2. Repository Structure: Where to Find Things

```
/
├── AGENTS.md           # The master protocol document (generated, don't edit directly)
├── protocols/          # The source code for AGENTS.md (edit these files)
├── knowledge_core/     # The agent's long-term memory and knowledge base
│   ├── lessons.jsonl   # Structured, actionable lessons from past tasks
│   └── plan_registry.json # Reusable, named execution plans
├── logs/               # Structured logs of all agent activity
├── tooling/            # Scripts and tools the agent uses to do its work
├── postmortems/        # Templates and archives for post-task analysis
├── research/           # Research materials and reports
└── self_improvement_project/ # A simple project to practice core skills
```

## 3. Your First Contribution: The "FizzBuzz" Test

We've created a simple, self-contained project to help you get started: the `self_improvement_project`. This is a safe sandbox where you can practice the core development workflow without affecting the main agent.

**Your Task:**
1.  Navigate to the `self_improvement_project/` directory.
2.  Read the `README.md` file there for instructions.
3.  Try to improve the FizzBuzz implementation or its tests in some small way.
4.  Follow the development cycle: make a change, run the tests, and ensure they pass.

This exercise will familiarize you with the basic editing and testing loop.

## 4. The Development Lifecycle: From Plan to Pull Request

Every task in this repository follows a structured lifecycle:

1.  **Planning:** A formal plan is created, outlining the steps to be taken.
2.  **Execution:** The agent (or you) executes the plan, using the tools in the `tooling/` directory.
3.  **Testing:** All relevant tests must pass.
4.  **Post-Mortem:** After the task, a structured post-mortem is conducted to identify lessons learned.
5.  **Self-Correction:** Actionable lessons are added to `knowledge_core/lessons.jsonl`, which are then used to programmatically improve the agent's protocols.

When you are ready to contribute to the main agent, you will follow this same fundamental process.

---

This guide provides a starting point. The best way to learn is by exploring the files and protocols. Welcome to the team!