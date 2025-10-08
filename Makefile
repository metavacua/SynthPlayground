# Makefile for SynthPlayground

# Define the default target
.DEFAULT_GOAL := help

# Phony targets don't represent files
.PHONY: help install format lint build-protocol validate-protocol

# Tool definitions
PYTHON := python3
PIP := pip
BLACK := black .
FLAKE8 := flake8 .

help:
	@echo "Available commands:"
	@echo "  make install           - Installs all dependencies from requirements.txt."
	@echo "  make format            - Formats the code using black."
	@echo "  make lint              - Lints the code using flake8."
	@echo "  make build-protocol    - Builds the AGENTS.md protocol file from sources."
	@echo "  make validate-protocol - Checks if the committed AGENTS.md is up-to-date."

install:
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt

format:
	@echo "Formatting code..."
	@$(BLACK)

lint:
	@echo "Linting code..."
	@$(FLAKE8)

build-protocol:
	@echo "Building AGENTS.md from protocol_sources/..."
	@$(PYTHON) tooling/build_protocol.py
	@echo "AGENTS.md has been successfully built."

validate-protocol: build-protocol
	@echo "Validating AGENTS.md..."
	@git diff --exit-code AGENTS.md || (echo "Error: AGENTS.md is not up-to-date. Please run 'make build-protocol' and commit the changes." >&2; exit 1)
	@echo "AGENTS.md is up-to-date."