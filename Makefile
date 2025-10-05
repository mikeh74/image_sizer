.PHONY: help install install-dev lint format check test clean build dist upload pre-commit

# Variables
PYTHON := .venv/bin/python
PIP := .venv/bin/pip
RUFF := .venv/bin/ruff
PYTEST := .venv/bin/pytest
PRE_COMMIT := .venv/bin/pre-commit

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install the package"
	@echo "  install-dev  - Install the package in development mode with dev dependencies"
	@echo "  lint         - Run ruff linting"
	@echo "  format       - Run ruff formatting"
	@echo "  check        - Run all checks (lint + format check)"
	@echo "  pre-commit   - Run pre-commit on all files"
	@echo "  test         - Run tests with pytest"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build the package"
	@echo "  dist         - Create distribution files"
	@echo "  upload       - Upload to PyPI (requires authentication)"

# Create virtual environment if it doesn't exist
.venv/bin/activate:
	python3 -m venv .venv
	$(PIP) install --upgrade pip setuptools wheel

# Installation targets
install: .venv/bin/activate
	$(PIP) install .

install-dev: .venv/bin/activate
	$(PIP) install -e ".[dev]"

# Code quality targets
lint:
	$(RUFF) check src/ tests/

format:
	$(RUFF) format src/ tests/

format-check:
	$(RUFF) format --check src/ tests/

check: lint format-check
	@echo "✅ All checks passed!"

# Pre-commit targets
pre-commit: pre-commit-install
	$(PRE_COMMIT) run --all-files

pre-commit-install:
	$(PIP) install pre-commit
	$(PRE_COMMIT) install

pre-commit-update:
	$(PRE_COMMIT) autoupdate

# Testing targets
test:
	$(PYTEST)

test-cov:
	$(PYTEST) --cov=imagefixer --cov-report=html --cov-report=term

# Build and distribution targets
clean:
	rm -rf .venv/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

dist: build
	@echo "Distribution files created in dist/"
	@ls -la dist/

upload: dist
	$(PYTHON) -m twine upload dist/*

# Development shortcuts
fix: format
	$(RUFF) check --fix src/ tests/

dev-setup: install-dev
	$(PRE_COMMIT) install
	@echo "Development environment set up!"
	@echo "Run 'make check' or 'make pre-commit' to verify everything works."
