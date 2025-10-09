# Makefile for project standards and validation

.PHONY: install format lint validate-protocol build compile-protocols clean

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
PROTOCOLS = $(wildcard protocols/*.md)

# The AGENTS.md file is a target that depends on the source protocol files
# and the compiler script itself. It will only be rebuilt if any of them change.
AGENTS.md: $(PROTOCOLS) tooling/protocol_compiler.py
	@echo "--> Compiling protocols into AGENTS.md..."
	@python3 tooling/protocol_compiler.py

# A phony target to easily trigger the compilation.
compile-protocols: AGENTS.md

# A general build target.
build: compile-protocols

validate-protocol:
	@echo "--> Validating protocol source file presence and naming..."
	@python3 tooling/protocol_validator.py

clean:
	@echo "--> Removing compiled AGENTS.md..."
	@rm -f AGENTS.md