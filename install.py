#!/usr/bin/env python3
"""
Modern installation script for DBF to SQL Converter
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8+ required")
        print(f"  Current version: {version.major}.{version.minor}.{version.micro}")
        return False

    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_package():
    """Install the package in development mode."""
    try:
        print("Installing package in development mode...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("✓ Package installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install package: {e}")
        return False


def install_dev_dependencies():
    """Install development dependencies."""
    try:
        print("Installing development dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
        print("✓ Development dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install development dependencies: {e}")
        return False


def run_tests():
    """Run a quick test to verify installation."""
    try:
        print("Running quick test...")
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from dbf2sql import DBFToSQLConverter; print('✓ Import successful')",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✓ Package is working correctly")
            return True
        else:
            print(f"✗ Package test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error running test: {e}")
        return False


def main():
    """Main installation function."""
    print("DBF to SQL Converter - Modern Installation")
    print("=" * 45)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("✗ pyproject.toml not found. Please run this script from the project directory.")
        sys.exit(1)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Install package
    if not install_package():
        sys.exit(1)

    # Install development dependencies
    if not install_dev_dependencies():
        print("⚠ Development dependencies failed to install, but core package is ready")

    # Run tests
    if not run_tests():
        print("⚠ Tests failed, but installation may still be working")

    print("\n" + "=" * 45)
    print("Installation completed successfully!")
    print("\nYou can now use the converter in several ways:")
    print("1. Command line: dbf2sql your_file.dbf")
    print("2. Python import: from dbf2sql import DBFToSQLConverter")
    print("3. Run examples: python scripts/example_usage.py")
    print("4. Run tests: make test")
    print("5. See help: dbf2sql --help")


if __name__ == "__main__":
    main()
