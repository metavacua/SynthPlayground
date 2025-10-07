# Makefile for simplifying common development tasks.

# Use bash as the shell
SHELL := /bin/bash

# Define Python interpreter
PYTHON := python

# Default target
.PHONY: help

help:
	@echo "Available commands:"
	@echo "  make install                      Install project dependencies."
	@echo "  make test                         Run all unit tests."
	@echo "  make format                       Format code using black."
	@echo "  make lint                         Lint code using flake8."
	@echo "  make validate-placeholders        Validate that all TODOs are correctly formatted."
	@echo "  make orient summary='<message>'   Log a new temporal orientation entry."

install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

test:
	@echo "Running tests..."
	$(PYTHON) -m unittest discover -s tooling -p "test_*.py"
	$(PYTHON) -m unittest discover -s utils -p "test_*.py"

format:
	@echo "Formatting code..."
	$(PYTHON) -m black .

lint:
	@echo "Linting code..."
	$(PYTHON) -m flake8 .

validate-placeholders:
	@echo "Validating placeholders..."
	$(PYTHON) tooling/placeholder_manager.py validate

orient:
	@if [ -z "$(summary)" ]; then \
		echo "Error: summary argument is required. Usage: make orient summary='Your summary'"; \
		exit 1; \
	fi
	$(PYTHON) tooling/temporal_orienter.py "$(summary)"