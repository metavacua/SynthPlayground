# Makefile for project standards and validation

.PHONY: install format lint build compile-protocols compile-security-protocols clean docs

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
# --- Shared Variables ---
SCHEMA_FILE = protocols/protocol.schema.json
COMPILER_SCRIPT = tooling/protocol_compiler.py

# --- AGENTS.md ---
AGENT_PROTOCOLS_JSON = $(wildcard protocols/*.protocol.json)
AGENT_PROTOCOLS_MD = $(wildcard protocols/*.protocol.md)
AGENT_PROTOCOLS_AUTODOC = $(wildcard protocols/*.autodoc.md)

# The AGENTS.md file is a target that depends on all its source files.
AGENTS.md: $(AGENT_PROTOCOLS_JSON) $(AGENT_PROTOCOLS_MD) $(AGENT_PROTOCOLS_AUTODOC) $(SCHEMA_FILE) $(COMPILER_SCRIPT)
	@echo "--> Compiling agent protocols into AGENTS.md and Knowledge Graph..."
	@python3 $(COMPILER_SCRIPT) \
		--source-dir protocols \
		--output-file AGENTS.md \
		--schema-file $(SCHEMA_FILE) \
		--knowledge-graph-file

# A phony target to easily trigger the main protocol compilation.
compile-protocols: AGENTS.md

# --- SECURITY.md ---
SECURITY_PROTOCOLS_JSON = $(wildcard protocols/security/*.protocol.json)
SECURITY_PROTOCOLS_MD = $(wildcard protocols/security/*.protocol.md)

# The SECURITY.md file is a target that depends on all its source files.
SECURITY.md: $(SECURITY_PROTOCOLS_JSON) $(SECURITY_PROTOCOLS_MD) $(SCHEMA_FILE) $(COMPILER_SCRIPT)
	@echo "--> Compiling security protocols into SECURITY.md..."
	@python3 $(COMPILER_SCRIPT) \
		--source-dir protocols/security \
		--output-file SECURITY.md \
		--schema-file $(SCHEMA_FILE)

# A phony target to easily trigger the security protocol compilation.
compile-security-protocols: SECURITY.md


# ==============================================================================
# Documentation Generation
# ==============================================================================
docs:
	@echo "--> Generating system documentation from source..."
	@python3 tooling/doc_generator.py

# ==============================================================================
# Main Targets
# ==============================================================================
# A general build target that compiles all protocols and generates documentation.
build: compile-protocols compile-security-protocols docs

clean:
	@echo "--> Removing compiled protocol and documentation artifacts..."
	@rm -f AGENTS.md
	@rm -f SECURITY.md
	@rm -f knowledge_core/SYSTEM_DOCUMENTATION.md
	@rm -f knowledge_core/protocols.ttl