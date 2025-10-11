# Makefile for project standards and validation

.PHONY: all install format lint test build compile-protocols compile-security-protocols clean docs

# ==============================================================================
# Default Target
# ==============================================================================
all: AGENTS.md

# ==============================================================================
# Dependency Management
# ==============================================================================
install:
	@echo "--> Installing dependencies from requirements.txt..."
	@pip install -r requirements.txt

# ==============================================================================
# Code Quality & Formatting
# ==============================================================================
format: AGENTS.md
	@echo "--> Formatting Python code with black..."
	@black .

lint: AGENTS.md
	@echo "--> Linting Python code with flake8..."
	@flake8 .

# ==============================================================================
# Testing
# ==============================================================================
test: AGENTS.md
	@echo "--> Running all unit tests..."
	@python3 -m unittest discover -v .

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
AGENTS.md: $(AGENT_PROTOCOLS_JSON) $(AGENT_PROTOCOLS_MD) $(AGENT_PROTOCOLS_AUTODOC) $(SCHEMA_FILE) $(COMPILER_SCRIPT) knowledge_core/SYSTEM_DOCUMENTATION.md
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
# Knowledge Graph Enrichment
# ==============================================================================
enrich-kg: AGENTS.md tooling/knowledge_integrator.py
	@echo "--> Enriching knowledge graph with external data..."
	@python3 tooling/knowledge_integrator.py


# ==============================================================================
# Documentation Generation
# ==============================================================================
# Find all non-test Python files in directories scanned by doc_generator.py
PYTHON_DOC_SOURCES = $(shell find tooling/ utils/ -name "*.py" -not -name "test_*.py")

# Rule to generate the main system documentation from Python source files.
knowledge_core/SYSTEM_DOCUMENTATION.md: tooling/doc_generator.py $(PYTHON_DOC_SOURCES)
	@echo "--> Generating system documentation from source..."
	@python3 tooling/doc_generator.py

# A phony target to easily trigger documentation generation.
docs: knowledge_core/SYSTEM_DOCUMENTATION.md

readme:
	@echo "--> Generating README.md from source..."
	@python3 tooling/readme_generator.py

# ==============================================================================
# Auditing
# ==============================================================================
audit:
	@echo "--> Running protocol auditor..."
	@python3 tooling/protocol_auditor.py

# ==============================================================================
# Main Targets
# ==============================================================================
# Rule to generate the GitHub Pages site.
pages: AGENTS.md README.md tooling/pages_generator.py
	@echo "--> Generating GitHub Pages site from metalanguage..."
	@python3 tooling/pages_generator.py

# A general build target that compiles all protocols and generates documentation.
build: docs readme compile-protocols compile-security-protocols pages

clean:
	@echo "--> Removing compiled protocol and documentation artifacts..."
	@rm -f AGENTS.md
	@rm -f README.md
	@rm -f SECURITY.md
	@rm -f knowledge_core/SYSTEM_DOCUMENTATION.md