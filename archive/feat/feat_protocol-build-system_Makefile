# Makefile for SynthPlayground

# Define the default target
.DEFAULT_GOAL := help

# Phony targets don't represent files
.PHONY: help build-protocol validate-protocol

help:
	@echo "Available commands:"
	@echo "  make build-protocol  - Builds the AGENTS.md protocol file from sources."
	@echo "  make validate-protocol - Checks if the committed AGENTS.md is up-to-date."

build-protocol:
	@echo "Building AGENTS.md from protocol_sources/..."
	@python3 tooling/build_protocol.py
	@echo "AGENTS.md has been successfully built."

validate-protocol: build-protocol
	@echo "Validating AGENTS.md..."
	@git diff --exit-code AGENTS.md || (echo "Error: AGENTS.md is not up-to-date. Please run 'make build-protocol' and commit the changes." >&2; exit 1)
	@echo "AGENTS.md is up-to-date."