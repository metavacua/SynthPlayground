# Makefile for project standards and validation

.PHONY: install format lint build compile-protocols clean

# ==============================================================================
# Dependency Management
# ==============================================================================
install:
	@echo "--> Installing dependencies from requirements.txt..."
	@pip install -r requirements.txt

# ==============================================================================
# Code Quality & Formatting
# ==============================================================================
format:
	@echo "--> Formatting Python code with black..."
	@black .

lint:
	@echo "--> Linting Python code with flake8..."
	@flake8 .

# ==============================================================================
# Protocol Compilation & Validation
# ==============================================================================
PROTOCOLS = $(wildcard protocols/*.protocol.json)

# The AGENTS.md file is a target that depends on the source protocol files,
# the schema, and the compiler script itself. It will only be rebuilt if any of them change.
AGENTS.md: $(PROTOCOLS) protocols/protocol.schema.json tooling/protocol_compiler.py
	@echo "--> Compiling protocols into AGENTS.md..."
	@python3 tooling/protocol_compiler.py

# A phony target to easily trigger the compilation.
compile-protocols: AGENTS.md

# A general build target.
build: compile-protocols

clean:
	@echo "--> Removing compiled protocol artifacts (AGENTS.json, AGENTS.md)..."
	@rm -f AGENTS.json AGENTS.md