# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-12

### Added
- Initial release of DBF to SQL Converter
- Memory-efficient batch processing of DBF files
- Support for multiple DBF field types
- Command-line interface with argparse
- Python package structure with proper setup.py
- Type hints and mypy support
- Comprehensive test suite
- Development tools (Makefile, tox, GitHub Actions)
- Documentation and examples

### Features
- Convert DBF files to SQL INSERT statements
- Configurable batch size for memory efficiency
- Support for multiple character encodings
- Automatic SQL type mapping from DBF field types
- Progress tracking for large files
- Error handling and logging
- Console script entry point

### Technical
- Modern Python packaging with pyproject.toml
- Type stubs for dbfread library
- Comprehensive test coverage
- Code formatting with black and isort
- Linting with flake8
- CI/CD with GitHub Actions
- Cross-platform support (Linux, Windows, macOS)
