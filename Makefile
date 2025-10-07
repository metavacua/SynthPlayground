# Makefile for simplifying common development tasks.

# Use bash as the shell
SHELL := /bin/bash

# Define Python interpreter - useful for virtual environments
PYTHON := python3

# Find all Python source files
SOURCES = $(shell find . -name "*.py" -not -path "./.venv/*" -not -path "./env/*")

.PHONY: help install test format lint validate-placeholders

help:
	@echo "Available commands:"
	@echo "  make install                  Install project dependencies."
	@echo "  make test                     Run all unit tests."
	@echo "  make format                   Format code using black."
	@echo "  make lint                     Lint code using flake8."
	@echo "  make validate-placeholders    Validate that all TODOs are correctly formatted."

install: requirements.txt
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

test:
	@echo "Running tests..."
	$(PYTHON) -m unittest discover -s . -p "test_*.py"

format:
	@echo "Formatting code..."
	$(PYTHON) -m black .

lint:
	@echo "Linting code..."
	$(PYTHON) -m flake8 .

validate-placeholders:
	@echo "Validating placeholders..."
	$(PYTHON) tooling/placeholder_manager.py validate