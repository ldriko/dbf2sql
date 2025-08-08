#!/usr/bin/env python3
"""
Diagnostic script for DBF to SQL Converter
Helps troubleshoot common issues and verify setup
"""

import sys
import importlib.util
from pathlib import Path


def check_python_version():
    """Check Python version compatibility."""
    print("Python Version Check:")
    version = sys.version_info
    print(f"  Current version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ✗ Python 3.8+ required")
        return False
    else:
        print("  ✓ Python version is compatible")
        return True


def check_installation():
    """Check if the package is installed."""
    print("\nInstallation Check:")

    try:
        # Try importing from installed package
        import dbf2sql

        print("  ✓ Package installed successfully")
        print(f"  Version: {getattr(dbf2sql, '__version__', 'unknown')}")
        return True
    except ImportError:
        print("  ✗ Package not installed")
        print("  → Run: pip install -e .")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nDependency Check:")

    try:
        # Check if we can import dbfread
        spec = importlib.util.find_spec("dbfread")
        if spec is None:
            print("  ✗ dbfread not found")
            print("  → Run: pip install dbfread")
            return False
        else:
            print("  ✓ dbfread is available")
            return True
    except Exception as e:
        print(f"  ✗ Error checking dependencies: {e}")
        return False


def check_files():
    """Check if all necessary files exist."""
    print("\nFile Check:")

    required_files = [
        "src/dbf2sql/__init__.py",
        "src/dbf2sql/converter.py",
        "src/dbf2sql/cli.py",
        "requirements.txt",
        "README.md",
        "setup.py",
    ]

    all_exist = True

    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            all_exist = False

    return all_exist


def check_sample_dbf():
    """Check for sample DBF files."""
    print("\nSample DBF Files Check:")

    dbf_files = list(Path(".").glob("*.dbf"))

    if not dbf_files:
        print("  ⚠ No DBF files found in current directory")
        print("  → Add some DBF files to test the converter")
        return False

    print(f"  ✓ Found {len(dbf_files)} DBF files:")
    for dbf_file in dbf_files:
        print(f"    - {dbf_file.name}")

    return True


def check_permissions():
    """Check file permissions."""
    print("\nPermissions Check:")

    # Check if we can write to current directory
    try:
        test_file = Path("test_write.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("  ✓ Can write to current directory")
        return True
    except Exception as e:
        print(f"  ✗ Cannot write to current directory: {e}")
        return False


def run_quick_test() -> bool:
    """Run a quick test of the converter."""
    print("\nQuick Test:")

    try:
        # Try to import the converter
        from dbf2sql import DBFToSQLConverter

        # Create a converter instance
        converter = DBFToSQLConverter()
        print("  ✓ DBFToSQLConverter imported successfully")

        # Test SQL type mapping (accessing protected method for testing)
        sql_type = converter._get_sql_type("C", 50, 0)  # type: ignore
        if sql_type == "VARCHAR(50)":
            print("  ✓ SQL type mapping works")
        else:
            print(f"  ✗ SQL type mapping failed: {sql_type}")
            return False

        # Test SQL escaping (accessing protected method for testing)
        escaped = converter._escape_sql_value("test's string")  # type: ignore
        if escaped == "'test''s string'":
            print("  ✓ SQL escaping works")
        else:
            print(f"  ✗ SQL escaping failed: {escaped}")
            return False

        return True

    except Exception as e:
        print(f"  ✗ Error during quick test: {e}")
        return False


def main() -> bool:
    """Main diagnostic function."""
    print("DBF to SQL Converter - Diagnostic Tool")
    print("=" * 40)

    checks = [
        check_python_version,
        check_installation,
        check_dependencies,
        check_files,
        check_sample_dbf,
        check_permissions,
        run_quick_test,
    ]

    results: list[bool] = []
    for check in checks:
        results.append(check())

    print("\n" + "=" * 40)
    print("Diagnostic Summary:")

    passed = sum(results)
    total = len(results)

    print(f"  Passed: {passed}/{total} checks")

    if passed == total:
        print("  ✓ All checks passed! The converter should work properly.")
    else:
        print("  ⚠ Some checks failed. Please address the issues above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
