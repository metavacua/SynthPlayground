# AI Agent Self-Improving Codebase

## Overview

This repository is an experimental environment for a self-correcting and self-improving AI agent. The agent's primary goal is to autonomously manage, refactor, and enhance its own codebase and governing protocols.

## Getting Started

All instructions for setting up the development environment, running tests, and interacting with the agent are located in the `AGENTS.md` file. This file provides a clear and static set of instructions.

### Build System

This project uses a unified, configuration-driven build system. The main entry point is the `tooling/builder.py` script, which reads its configuration from `build_config.json`.

To see a list of all available build targets, run:
```bash
python3 tooling/builder.py --list
```

To run a specific target, use the `--target` flag. For example, to compile all protocols:
```bash
python3 tooling/builder.py --target protocols
```

To run all default build steps (including protocol compilation), you can run the "all" build group:
```bash
python3 tooling/builder.py --target all
```

## How It Works

The core of this project is a set of machine-readable protocols located in the `protocols/` directory. These protocols define the agent's behavior and are compiled into `AGENTS.md` files within each protocol module. The `AGENTS.md` file in the root directory provides a high-level overview and instructions for AI agents.

The long-term vision is for the agent to be able to modify its own protocols, allowing it to evolve its own development processes and capabilities over time.
