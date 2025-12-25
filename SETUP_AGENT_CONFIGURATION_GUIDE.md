# Setup Agent Configuration Guide for CatCleanup Branch

## Quick Start for Setup Agent

### Canonical Build Command
```bash
python3 tooling/builder.py --target all
```

### Single Entry Point
```bash
python3 tooling/agent_shell.py [arguments]
```

---

## Overview

This guide provides the setup agent with everything needed to reliably configure the CatCleanup repository. The branch has been consolidated to use a single unified build system with clear entry points.

### Key Points
- **Primary Build System:** `tooling/builder.py` (unified, configuration-driven)
- **Secondary Interface:** `make` (wraps builder.py for convenience)
- **Primary Entry Point:** `tooling/agent_shell.py` (agent operations)
- **Status:** All build targets now work correctly

---

## Build System Architecture

### 1. Unified Builder (`tooling/builder.py`)

The canonical build system. All build operations should use this script.

**Usage:**
```bash
python3 tooling/builder.py --target <target_name>
python3 tooling/builder.py --target all  # Build everything
python3 tooling/builder.py --list        # List all available targets
```

**Configuration File:** `build_config.yaml`
- Defines all build targets and their dependencies
- Single source of truth for build logic
- Supports both "compiler" and "command" type targets

### 2. Makefile (`Makefile`)

Convenience wrapper around the builder for teams that prefer traditional `make` commands.

**Usage:**
```bash
make all    # Equivalent to: python3 tooling/builder.py --target all
make install
make lint
make test
```

### 3. Direct Script Execution (DEPRECATED)

The following scripts should NOT be run directly anymore:
- ~~`python3 tooling/generate_agents_md.py`~~ (use builder)
- ~~`python3 tooling/lint_chc_protocols.py`~~ (use builder)
- ~~`python3 tooling/protocol_compiler.py`~~ (use builder)

They still work standalone but bypass dependency checking and may cause issues.

---

## Available Build Targets

### Core Targets (Must Run)

```bash
# Install dependencies (first step)
python3 tooling/builder.py --target install

# Compile protocols (generates protocols.yaml-ld)
python3 tooling/builder.py --target protocols

# Generate AGENTS.md (the master protocol document)
python3 tooling/builder.py --target agents-md

# Integrate knowledge sources
python3 tooling/builder.py --target knowledge-integrate
```

### Complete Build

```bash
# Runs all core targets in correct order
python3 tooling/builder.py --target all
```

### Utility Targets

```bash
# Code quality
python3 tooling/builder.py --target lint           # Flake8 linting
python3 tooling/builder.py --target format         # Black formatting

# Code maintenance
python3 tooling/builder.py --target ast-generate           # Generate ASTs
python3 tooling/builder.py --target extract-symbols        # Extract symbols
python3 tooling/builder.py --target remove-unused-imports  # Clean imports

# Testing
python3 tooling/builder.py --target test          # Pytest
python3 tooling/builder.py --target test-all      # All repository tests

# Special
python3 tooling/builder.py --target guardian-protocol  # Guardian protocol
```

---

## Entry Points

### Primary Entry Point: Agent Operations

**File:** `tooling/agent_shell.py`

**Purpose:** API-driven entry point for agent operations. This is the main entry point for all agent tasks.

**Usage:**
```bash
python3 tooling/agent_shell.py [arguments]
```

**Verification:**
```bash
python3 -c "import tooling.agent_shell; print('OK')"
```

### Orchestrator Entry Point

**File:** `tooling/master_control.py`

**Purpose:** Master orchestrator implementing the Context-Free Development Cycle (CFDC).

**Features:**
- Hierarchical plan execution
- Plan validation against FSM
- Registry-first plan resolution

**Usage:** Typically called from agent_shell.py, but can be used directly.

**Verification:**
```bash
python3 -c "from tooling.master_control import MasterControlGraph; print('OK')"
```

---

## Setup Workflow for Setup Agent

### Step 1: Install Dependencies
```bash
python3 tooling/builder.py --target install
```

This installs all Python dependencies from `requirements.txt` using `--break-system-packages` flag (required for Python 3.12+).

### Step 2: Run Full Build
```bash
python3 tooling/builder.py --target all
```

This will:
1. Lint CHC protocols
2. Generate AGENTS.md
3. Compile protocols to YAML-LD
4. Integrate knowledge sources

### Step 3: Verify Entry Points
```bash
# Test agent_shell.py can be imported
python3 -c "import tooling.agent_shell; print('agent_shell.py: OK')"

# Test master_control.py can be imported
python3 -c "from tooling.master_control import MasterControlGraph; print('master_control.py: OK')"
```

### Step 4: Run Tests (Optional but Recommended)
```bash
python3 tooling/builder.py --target test
```

---

## Troubleshooting

### Issue: `error: externally-managed-environment`
**Solution:** The build system already handles this with `--break-system-packages`. If you see this error, it means you're not using the builder.

### Issue: `No module named 'protocols'`
**Solution:** Add project root to Python path. The build system scripts already do this. If you see this, you're running a script directly instead of through the builder.

### Issue: Import errors for agent_shell or master_control
**Solution:** Run `python3 tooling/builder.py --target install` first to ensure dependencies are installed.

### Issue: Build targets failing with "Target not found"
**Solution:** Use `python3 tooling/builder.py --list` to see valid target names.

---

## Idempotency and Consistency

The build system is designed to be idempotent:
- Running `python3 tooling/builder.py --target all` multiple times produces the same result
- Each target checks if it's already been executed and skips if so
- Safe to run repeatedly

### Verification

Run the full build 3 times consecutively:
```bash
python3 tooling/builder.py --target all  # Run 1
python3 tooling/builder.py --target all  # Run 2
python3 tooling/builder.py --target all  # Run 3
```

All runs should complete successfully with "SUCCESS" status for all targets.

---

## File Structure Reference

```
/home/engine/project/
├── build_config.yaml           # Central build configuration
├── Makefile                    # Convenience wrapper
├── requirements.txt            # Python dependencies
│
├── tooling/
│   ├── builder.py              # PRIMARY BUILD SYSTEM
│   ├── agent_shell.py          # PRIMARY ENTRY POINT
│   ├── master_control.py       # Orchestrator
│   ├── generate_agents_md.py   # Generates AGENTS.md
│   ├── lint_chc_protocols.py   # Lints CHC protocols
│   └── protocol_compiler.py    # Compiles protocols
│
├── protocols/                  # Protocol definitions
│   ├── chc/                    # CHC-verified protocols
│   └── *.protocol.yaml         # Protocol files
│
├── knowledge_core/             # Knowledge artifacts
└── AGENTS.md                   # Master protocol document (generated)
```

---

## Differences from CTO.new Normative

This repository deviates from standard CTO.new conventions in these ways:

| Aspect | Standard CTO.new | CatCleanup Branch |
|--------|------------------|-------------------|
| Entry Point | Single `main.py` | `tooling/agent_shell.py` |
| Build System | Simple Makefile | `tooling/builder.py` with YAML config |
| Packaging | setup.py/pyproject.toml | None (legacy approach) |
| Protocols | YAML files only | CHC-verified Python proofs |

### Impact on Setup Agent
- Must use `tooling/builder.py` instead of Makefile alone
- Must understand CHC protocol system (optional, handled by builder)
- No standard Python packaging (use requirements.txt directly)

---

## MCP Server Compatibility

For future MCP server integration:

1. **Builder MCP Wrapper:** `tooling/builder.py` can be wrapped to accept MCP requests
2. **Agent Shell:** `tooling/agent_shell.py` is designed for programmatic/API access
3. **Protocol Access:** Protocols are compiled to `protocols.yaml-ld` for easy access

Consider exposing these via MCP:
- Build operations (`builder.py --target <target>`)
- Agent operations (`agent_shell.py`)
- Protocol information (from `AGENTS.md` and `protocols.yaml-ld`)

---

## Verification Checklist

After setup, verify:

- [ ] Dependencies installed without errors
- [ ] `python3 tooling/builder.py --target all` completes successfully
- [ ] All 4 core targets show "SUCCESS" status
- [ ] `AGENTS.md` is generated/updated
- [ ] `protocols.yaml-ld` is generated
- [ ] `tooling.agent_shell` can be imported
- [ ] `tooling.master_control` can be imported
- [ ] Build is idempotent (run 3 times, all succeed)

---

## Support and Issues

If setup fails:

1. Check that you're on the correct branch: `catcleanup-consolidate-builds-entrypoints-setup-agent-reliability`
2. Run `python3 tooling/builder.py --target all` and check output
3. Verify Python path is set correctly
4. Check that dependencies installed successfully
5. Consult `CATCLEANUP_BUILD_DOCUMENTATION.md` for detailed information

---

## Quick Reference Commands

```bash
# Full build
python3 tooling/builder.py --target all

# List all targets
python3 tooling/builder.py --list

# Install dependencies
python3 tooling/builder.py --target install

# Run tests
python3 tooling/builder.py --target test

# Format code
python3 tooling/builder.py --target format

# Lint code
python3 tooling/builder.py --target lint
```
