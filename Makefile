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
HIERARCHICAL_COMPILER_SCRIPT = tooling/hierarchical_compiler.py
ALL_PROTOCOL_SOURCES = $(shell find . -path '*/protocols/*.protocol.json' -o -path '*/protocols/*.protocol.md' -o -path '*/protocols/*.autodoc.md')

# The AGENTS.md file is a target that depends on the hierarchical compiler
# and all possible source files it might find.
AGENTS.md: $(ALL_PROTOCOL_SOURCES) $(HIERARCHICAL_COMPILER_SCRIPT) $(COMPILER_SCRIPT) knowledge_core/SYSTEM_DOCUMENTATION.md
	@echo "--> [Protocol Build] Saving current AGENTS.md for diff analysis..."
	@mv -f AGENTS.md AGENTS.md.old 2>/dev/null || true
	@echo "--> [Protocol Build] Recursively compiling all AGENTS.md and README.md files..."
	@python3 $(HIERARCHICAL_COMPILER_SCRIPT)
	@echo "--> [Protocol Build] Running mandatory re-orientation cycle..."
	@python3 tooling/reorientation_manager.py --old-agents-file AGENTS.md.old --new-agents-file AGENTS.md
	@rm -f AGENTS.md.old

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

# --- AGENTS.standard.md ---
STANDARD_COMPILER_SCRIPT = tooling/standard_agents_compiler.py
AGENTS.standard.md: $(STANDARD_COMPILER_SCRIPT) Makefile
	@echo "--> Compiling standard-compliant AGENTS.md..."
	@python3 $(STANDARD_COMPILER_SCRIPT)

# A phony target to easily trigger the standard-compliant AGENTS.md compilation.
agents-standard: AGENTS.standard.md


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

readme: AGENTS.md tooling/readme_generator.py
	@echo "--> Generating README.md from source..."
	@python3 tooling/readme_generator.py --source-file AGENTS.md --output-file README.md

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