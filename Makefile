# Makefile for project standards and validation
# Refactored to use the unified builder.py script

.PHONY: all install format lint test build clean docs security agents readme

# ==============================================================================
# Variables
# ==============================================================================
BUILDER_SCRIPT = tooling/builder.py

# ==============================================================================
# Default Target
# ==============================================================================
all: build

# ==============================================================================
# High-Level Build Targets
# ==============================================================================
# These targets delegate all logic to the centralized builder script.
# The builder script reads its configuration from build_config.json.

# Build all primary artifacts
build:
	@echo "--> Running unified build for all targets..."
	@python3 $(BUILDER_SCRIPT) --target all

# Generate system documentation
docs:
	@echo "--> Building target: docs"
	@python3 $(BUILDER_SCRIPT) --target docs

# Compile security protocols
security:
	@echo "--> Building target: security"
	@python3 $(BUILDER_SCRIPT) --target security

# Compile hierarchical agent protocols
agents:
	@echo "--> Building target: agents"
	@python3 $(BUILDER_SCRIPT) --target agents

# Generate the root README.md
readme:
	@echo "--> Building target: readme"
	@python3 $(BUILDER_SCRIPT) --target readme

# ==============================================================================
# Code Quality & Testing
# ==============================================================================
install:
	@echo "--> Installing dependencies from requirements.txt..."
	@pip install -r requirements.txt

format:
	@echo "--> Formatting Python code with black..."
	@black .

lint:
	@echo "--> Linting Python code with flake8..."
	@flake8 .

test:
	@echo "--> Running all unit tests..."
	@python3 -m unittest discover -v .

# ==============================================================================
# Auditing
# ==============================================================================
audit:
	@echo "--> Running protocol auditor..."
	@python3 tooling/protocol_auditor.py

# ==============================================================================
# Cleanup
# ==============================================================================
clean:
	@echo "--> Removing compiled protocol and documentation artifacts..."
	@rm -f AGENTS.md
	@rm -f README.md
	@rm -f SECURITY.md
	@rm -f knowledge_core/SYSTEM_DOCUMENTATION.md