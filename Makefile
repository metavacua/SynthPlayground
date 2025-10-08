# Makefile for managing the development environment

# Phony targets prevent conflicts with files of the same name
.PHONY: all install test format lint orient

# Default target runs all checks
all: install test format lint

# Run the AORP Orientation Cascade
orient:
	@echo "--- Running AORP Orientation Cascade ---"
	@echo "[L1] Verifying Self-Awareness (agent_meta.json)..."
	@if [ ! -f knowledge_core/agent_meta.json ]; then echo "L1 FAILED: agent_meta.json not found."; exit 1; fi
	@echo "[L2] Actively Synchronizing Repository State..."
	@echo "--> Regenerating dependency graph (dependency_graph.json)..."
	@python3 tooling/dependency_graph_generator.py
	@echo "--> Regenerating symbol map (symbols.json)..."
	@python3 tooling/symbol_map_generator.py
	@echo "--> Verifying static knowledge artifacts..."
	@if [ ! -f knowledge_core/lessons_learned.md ]; then echo "L2 FAILED: lessons_learned.md not found."; exit 1; fi
	@if [ ! -f knowledge_core/temporal_orientation.md ]; then echo "L2 FAILED: temporal_orientation.md not found."; exit 1; fi
	@echo "[L3] Probing Environment..."
	@python3 tooling/probe.py
	@echo "--- Orientation Complete ---"

# Install Python dependencies from requirements.txt
install:
	@echo "Installing dependencies..."
	@pip install --upgrade pip
	@pip install -r requirements.txt

# Run unit tests using Python's unittest discovery
test:
	@echo "Running tests..."
	@echo "--> Running utils tests..."
	@python3 -m unittest discover utils/
	@echo "--> Running tooling tests..."
	@python3 -m unittest discover tooling/

# Format Python code using black
format:
	@echo "Formatting code..."
	@black .

# Lint Python code using flake8
lint:
	@echo "Linting code..."
	@flake8 .