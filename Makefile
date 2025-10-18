# ==============================================================================
# Makefile for Project Standards and Validation
#
# This Makefile has been refactored to be a simple, clean interface to the
# unified `builder.py` script. All build logic, commands, and configurations
# are defined in `build_config.json` and executed by the builder.
#
# This approach provides a single source of truth for the build system while
# retaining the convenience of traditional `make` commands.
# ==============================================================================

.PHONY: all install format lint test build clean docs security agents readme audit audit-docs quality pre-submit-check

# --- Variables ---
BUILDER = python3 tooling/builder.py

# --- High-Level Targets ---

# Default target: build all primary artifacts.
all:
	@$(BUILDER) --target all

# Run all code quality checks in sequence.
quality:
	@$(BUILDER) --target quality

# Build all primary project artifacts.
build: all

# --- Individual Commands (Delegated to Builder) ---

install:
	@$(BUILDER) --target install

format:
	@$(BUILDER) --target format

lint:
	@$(BUILDER) --target lint

test:
	@$(BUILDER) --target test

docs:
	@$(BUILDER) --target docs

security:
	@$(BUILDER) --target security

agents:
	@$(BUILDER) --target agents

readme:
	@$(BUILDER) --target readme

audit:
	@$(BUILDER) --target audit

audit-docs:
	@$(BUILDER) --target audit-docs

clean:
	@$(BUILDER) --target clean

pre-submit-check:
	@python3 tooling/pre_submit_check.py

# --- Help/Discovery ---

list:
	@$(BUILDER) --list

help:
	@echo "Makefile for project standards and validation."
	@echo "This Makefile is a wrapper around the unified builder.py script."
	@echo "All build logic is defined in build_config.json."
	@echo ""
	@echo "Available targets:"
	@$(BUILDER) --list