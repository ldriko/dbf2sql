.PHONY: help install install-dev test lint format clean build upload check-types run-example

help:
	@echo "Available commands:"
	@echo "  install      - Install package in development mode"
	@echo "  install-dev  - Install package and development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting (flake8)"
	@echo "  format       - Format code (black + isort)"
	@echo "  check-types  - Run type checking (mypy)"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  upload       - Upload package to PyPI"
	@echo "  run-example  - Run example usage script"

install:
	pip install -e .

install-dev:
	pip install -e .[dev]
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

lint:
	flake8 src/dbf2sql tests/ scripts/

format:
	black src/dbf2sql tests/ scripts/
	isort src/dbf2sql tests/ scripts/

check-types:
	mypy src/dbf2sql

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

run-example:
	python scripts/example_usage.py

# Development workflow
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make lint' to check code style"
	@echo "Run 'make format' to format code"
