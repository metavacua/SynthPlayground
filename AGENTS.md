# AGENTS.md

This file provides instructions for AI coding agents to interact with this project.

## Project Overview

This is a Python-based project with a sophisticated, self-correcting agent architecture.

## Build & Commands

This repository uses a unified build system driven by `tooling/builder.py`. All build, test, and quality assurance commands are defined as targets in `build_config.json`.

To run a build target, use the following command:

```bash
python3 tooling/builder.py --target [TARGET_NAME]
```

To see a list of all available targets, run:

```bash
python3 tooling/builder.py --list
```

## Core Protocols

The agent's behavior is governed by a set of core protocols, which are defined in the following modules:
- [Compliance](protocols/compliance/AGENTS.md)
- [Core](protocols/core/AGENTS.md)
- [Experimental](protocols/experimental/AGENTS.md)
- [Security](protocols/security/AGENTS.md)
- [Self Improvement](protocols/self_improvement/AGENTS.md)
- [Testing](protocols/testing/AGENTS.md)
