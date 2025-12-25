# CatCleanup Branch Build Consolidation and Entry Point Documentation

## Executive Summary

This document details the state of build processes and entry points on the CatCleanup branch, identifies issues preventing reliable setup agent configuration, and provides a consolidated canonical workflow.

**Last Updated:** 2025-12-25
**Status:** IN PROGRESS - Issues being resolved

---

## 1. Repository State Overview

### 1.1 CatCleanup Branch Context

The CatCleanup branch was created as a consolidation effort involving:
- Significant deletions and rearrangement of files/directories
- Removal of Aura interpreter and related files (aura.py, integration_demo.aura, test files)
- Removal of HDL prover files (test_hdl_prover.py, hdl_prover.py, protocols/core/hdl-proving.protocol.yaml)
- General cleanup of redundant or experimental code

**Expected Breakage:** As noted in the task description, multiple processes and entry points are expected to be non-functional due to this reorganization.

### 1.2 Current Build Architecture

The repository has THREE distinct build systems:

#### System 1: Unified Builder (PRIMARY)
- **Entry Point:** `python3 tooling/builder.py`
- **Configuration:** `build_config.yaml`
- **Status:** PARTIALLY FUNCTIONAL
- **Description:** The intended central build system that should be the single source of truth for all build operations

#### System 2: Makefile (SECONDARY)
- **Entry Point:** `make` (wraps builder.py)
- **Status:** PARTIALLY FUNCTIONAL
- **Description:** Simple wrapper providing traditional `make` interface to the builder

#### System 3: Direct Script Execution (REDUNDANT)
- Multiple scripts can be run directly:
  - `python3 tooling/generate_agents_md.py`
  - `python3 tooling/protocol_compiler.py`
  - `python3 tooling/lint_chc_protocols.py`
  - `python3 tooling/knowledge_integrator.py`
- **Status:** PARTIALLY FUNCTIONAL
- **Description:** Legacy approach that bypasses the unified builder

---

## 2. Identified Entry Points

### 2.1 Primary Entry Point (RECOMMENDED)
**File:** `tooling/agent_shell.py`
**Purpose:** API-driven entry point for the agent, replaces old file-based signaling
**Dependencies:** MasterControlGraph FSM, centralized logging

### 2.2 Orchestrator Entry Point
**File:** `tooling/master_control.py`
**Purpose:** Master orchestrator implementing the Context-Free Development Cycle (CFDC)
**Features:**
- Hierarchical plan execution with stack management
- Plan validation against FSM
- Registry-first plan resolution

### 2.3 Legacy/Standalone Entry Points
**File:** `run.py`
**Purpose:** Standalone runner for LFI interpreter
**Status:** BROKEN - has import issues (imports from current directory without path setup)

**File:** `language_theory/toolchain/__main__.py`
**Purpose:** Separate toolchain for language theory operations
**Status:** UNKNOWN - needs testing

---

## 3. Current Build Targets (from build_config.yaml)

### 3.1 Available Targets

| Target | Type | Status | Description |
|--------|------|--------|-------------|
| `install` | command | BROKEN | Install Python dependencies (pip install fails) |
| `lint-protocols` | command | BROKEN | Lint CHC protocols (import path issues) |
| `protocols` | compiler | WORKING | Compile protocol sources to YAML-LD |
| `agents-md` | command | PARTIAL | Generate AGENTS.md (has import errors but completes) |
| `knowledge-integrate` | compiler | UNKNOWN | Integrate knowledge sources |
| `lint` | command | UNKNOWN | Lint code with flake8 |
| `format` | command | UNKNOWN | Format code with black |
| `test` | command | UNKNOWN | Run pytest |
| `test-all` | command | UNKNOWN | Run all tests |
| `ast-generate` | command | UNKNOWN | Generate ASTs |
| `extract-symbols` | command | UNKNOWN | Extract symbols from ASTs |
| `remove-unused-imports` | command | UNKNOWN | Remove unused imports |
| `guardian-protocol` | command | UNKNOWN | Compile guardian protocol |

### 3.2 Build Groups

- **`all`:** runs `agents-md`, `protocols`, `knowledge-integrate`
- **`knowledge`:** runs `knowledge-integrate`

---

## 4. Issues Identified

### 4.1 Critical Issues (Preventing Build Success)

#### Issue #1: pip install fails with externally-managed-environment
**Impact:** Cannot install dependencies via standard pip
**Error:** `error: externally-managed-environment`
**Root Cause:** Python 3.12 system installation policy
**Affected Targets:** `install`
**Fix Required:** Use `--break-system-packages` flag or create virtual environment

#### Issue #2: lint-protocols fails with module import errors
**Impact:** Cannot validate CHC protocols
**Error:** `No module named 'protocols'`
**Root Cause:** `importlib.import_module()` called without adding project root to sys.path
**Affected Targets:** `lint-protocols`, `agents-md` (dependency)
**Fix Required:** Add project root to sys.path before importing

#### Issue #3: run.py has broken imports
**Impact:** Standalone LFI interpreter runner doesn't work
**Error:** `ModuleNotFoundError` for parser, type_checker, interpreter
**Root Cause:** Imports from current directory without path setup
**Fix Required:** Add project root to sys.path or fix imports

### 4.2 Documentation Issues

- No clear documentation of canonical build workflow
- Makefile and builder.py have inconsistent targets
- Entry points not clearly documented
- No README explaining the relationship between build systems

### 4.3 Architectural Issues

- Multiple ways to accomplish same build tasks
- Unclear which entry point setup agent should use
- Dependencies between targets not clearly documented
- No single source of truth for build process

---

## 5. Planned Fixes

### 5.1 Immediate Fixes (Priority 1)

1. **Fix pip install**
   - Modify `build_config.yaml` to use `--break-system-packages` flag
   - Document that this is a development-only workaround

2. **Fix lint-protocols import issues**
   - Add `sys.path.insert(0, os.path.abspath('.'))` to `tooling/lint_chc_protocols.py`
   - Ensure `__init__.py` files exist in protocols directories

3. **Fix run.py imports**
   - Add proper sys.path setup to enable imports from root directory

### 5.2 Consolidation Fixes (Priority 2)

4. **Deprecate direct script execution**
   - Remove or deprecate direct execution of `tooling/generate_agents_md.py`
   - Force all builds through `tooling/builder.py`

5. **Update Makefile**
   - Ensure all Make targets map correctly to builder targets
   - Remove redundant or conflicting targets

6. **Create comprehensive documentation**
   - Document canonical build workflow
   - Document entry points and their purposes
   - Create quick reference guide

### 5.3 MCP Compatibility Considerations

Future MCP server compatibility:
- Ensure `tooling/agent_shell.py` can be called via MCP
- Consider making `tooling/builder.py` MCP-compatible
- Document expected MCP interaction patterns

---

## 6. CTO.new Normative Deviation Analysis

### 6.1 Expected CTO.new Structure

Standard CTO.new projects typically have:
- Clear single entry point (e.g., `main.py` or `app.py`)
- Standard Python packaging (setup.py or pyproject.toml)
- Virtual environment management
- Single build system (Makefile or builder)
- Clear documentation in README.md

### 6.2 Current Deviations

| Aspect | Expected | Current | Impact |
|--------|----------|---------|--------|
| Entry Point | Single clear entry | Multiple entry points | Setup agent confusion |
| Build System | Single unified system | 3 overlapping systems | Redundancy, inconsistency |
| Packaging | setup.py/pyproject.toml | No packaging config | No standard installation |
| Dependencies | requirements.txt | requirements.txt exists | OK |
| Documentation | README.md | Multiple docs, no central | Hard to navigate |
| Testing | pytest with config | pytest exists | Needs verification |

### 6.3 Setup Agent Impact

The deviations impact setup agent in these ways:
1. **Multiple entry points:** Agent doesn't know which to use
2. **Multiple build systems:** Agent tries wrong system or gets confused
3. **No packaging:** Agent can't determine correct installation method
4. **Broken dependencies:** Agent encounters errors during configuration

---

## 7. Consolidated Canonical Workflow

### 7.1 Recommended Build Process

```bash
# 1. Install dependencies (with workaround)
python3 tooling/builder.py --target install

# 2. Compile protocols
python3 tooling/builder.py --target protocols

# 3. Generate AGENTS.md
python3 tooling/builder.py --target agents-md

# 4. Build all artifacts
python3 tooling/builder.py --target all
```

### 7.2 Recommended Entry Points

**For Agent Operations:**
```bash
python3 tooling/agent_shell.py [arguments]
```

**For Build Operations:**
```bash
python3 tooling/builder.py --target <target_name>
```

### 7.3 Deprecated/Removed Entry Points

- ~~`python3 run.py`~~ - BROKEN, to be fixed or removed
- ~~Direct script execution~~ - Should use builder.py instead

---

## 8. Verification Plan

To verify the build system is working correctly:

1. **Run the full build:**
   ```bash
   python3 tooling/builder.py --target all
   ```

2. **Verify each target:**
   - install: Dependencies installed without error
   - protocols: protocols.yaml-ld generated
   - agents-md: AGENTS.md generated/updated
   - knowledge-integrate: integrated_knowledge.jsonld generated

3. **Test entry points:**
   - agent_shell.py can be imported
   - master_control.py can be imported

4. **Repeat 3 times:**
   - Run full build 3 consecutive times
   - Verify no errors on subsequent runs (idempotent)

---

## 9. Future Considerations

### 9.1 MCP Server Compatibility

The team intends to move towards MCP (Model Context Protocol) server compatibility. Relevant architectural decisions:

- `tooling/agent_shell.py` should remain the primary agent entry point
- `tooling/builder.py` could be wrapped by MCP server for build operations
- Consider making builder.py accept MCP-style requests
- Protocol compilation could be exposed via MCP

### 9.2 Cleanup Recommendations

After MCP transition:
- Remove legacy `run.py` if not needed
- Deprecate direct script execution entirely
- Consolidate to single entry point (agent_shell.py)
- Standardize build process documentation

---

## 10. Change Log

| Date | Change | Author | Status |
|------|--------|--------|--------|
| 2025-12-25 | Initial documentation | Automated | In Progress |
| 2025-12-25 | Fixed pip install issue | Automated | Pending |
| 2025-12-25 | Fixed lint-protocols import | Automated | Pending |
| 2025-12-25 | Fixed run.py imports | Automated | Pending |
| 2025-12-25 | Verified 3 consecutive builds | Automated | Pending |
