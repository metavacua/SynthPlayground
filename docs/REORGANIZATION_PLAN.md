# Repository Reorganization and Cleanup Plan

## Overview

This document outlines the plan for reorganizing and cleaning up the SynthPlayground repository. Two experimental approaches are being developed as candidates for replacing the current main workflow:

1. **CoPilot_Experiment_0**: An AI-assisted development workflow experiment
2. **CatCleanup**: A categorical cleanup and organization system

## Current State Analysis

### Main Entry Points

The repository currently has multiple entry points:
- `run.py`: Main interpreter for APPL language
- `main.aura`: Aura-zero witness program
- `self_improvement_project/main.py`: Self-improvement process
- `tooling/agent_shell.py`: Interactive agent shell
- `tooling/master_control_cli.py`: Master control CLI

### Repository Structure Issues

1. **Multiple overlapping systems**: The repository contains several language implementations (Aura, APPL, LFI-ILL, pLLLU) with unclear relationships
2. **Scattered documentation**: Documentation exists in multiple formats and locations
3. **Unclear entry points**: Multiple "main" files create confusion about the primary workflow
4. **Archive accumulation**: The `archive/` directory contains unorganized historical code

## Experimental Approaches

### CoPilot_Experiment_0

**Status**: Planning Phase

**Objective**: Create an AI-assisted development workflow that integrates with the existing protocol system while providing a more intuitive interface for human developers.

**Key Features to Develop**:
- Unified command-line interface
- Integration with existing tooling
- Simplified protocol management
- Enhanced error reporting and recovery
- Better integration with version control

**Prerequisites**:
- [ ] Audit current agent_shell.py and master_control.py
- [ ] Design unified CLI interface
- [ ] Create prototype implementation
- [ ] Develop test suite
- [ ] Document migration path from current system

### CatCleanup

**Status**: Planning Phase

**Objective**: Implement a categorical approach to code organization based on formal category theory principles, ensuring clear separation of concerns and well-defined interfaces.

**Key Features to Develop**:
- Category-based module organization
- Formal interface definitions
- Dependency graph visualization
- Automated refactoring tools
- Consistency verification

**Prerequisites**:
- [ ] Map current codebase to categorical structure
- [ ] Define category boundaries and functors
- [ ] Create migration tooling
- [ ] Implement verification system
- [ ] Document categorical architecture

## Cleanup Tasks

### Phase 1: Documentation and Inventory

- [x] Create this reorganization plan
- [ ] Document all current entry points
- [ ] Map dependencies between modules
- [ ] Identify deprecated code
- [ ] Create migration checklist

### Phase 2: Archive Organization

- [ ] Review and categorize archive/ contents
- [ ] Move truly obsolete code to archive/deprecated/
- [ ] Extract reusable components from archive
- [ ] Document archive structure

### Phase 3: Module Consolidation

- [ ] Consolidate language implementations
- [ ] Merge overlapping tooling
- [ ] Standardize naming conventions
- [ ] Update import paths

### Phase 4: Testing and Validation

- [ ] Ensure all tests pass
- [ ] Add missing test coverage
- [ ] Validate protocol compliance
- [ ] Run full system audit

### Phase 5: Migration

- [ ] Implement chosen experimental approach
- [ ] Create migration scripts
- [ ] Update documentation
- [ ] Deprecate old entry points
- [ ] Update CI/CD pipelines

## Success Criteria

The reorganization will be considered successful when:

1. There is a single, clear entry point for the primary workflow
2. All modules have well-defined responsibilities
3. Dependencies are explicit and minimal
4. Documentation is comprehensive and up-to-date
5. All tests pass
6. The archive is organized and documented
7. Migration path is clear and documented

## Timeline

To be determined based on resource availability and priority assessment.
