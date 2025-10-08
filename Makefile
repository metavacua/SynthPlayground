# Makefile for project standards and validation

.PHONY: install format lint validate-protocol

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
# Protocol Validation
# ==============================================================================
validate-protocol:
	@echo "--> Validating protocol file presence and naming..."
	@python3 tooling/protocol_validator.py