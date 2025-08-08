#!/usr/bin/env python3
"""
Example usage of the DBF to SQL converter as a Python module
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Add the src directory to the path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dbf2sql import DBFToSQLConverter


def example_usage():
    """Example of using the converter programmatically."""

    # Initialize the converter with custom settings
    converter = DBFToSQLConverter(
        batch_size=2000,  # Process 2000 records at a time
        encoding="cp1252",  # Use Windows-1252 encoding
    )

    # Example 1: Convert a single file
    print("Example 1: Converting a single DBF file")
    success = converter.convert_dbf_to_sql("data.dbf", "output.sql")
    if success:
        print("✓ Conversion successful!")
    else:
        print("✗ Conversion failed!")

    # Example 1b: Convert a single file to a specific output directory
    print("\nExample 1b: Converting a single DBF file to specific output directory")
    success = converter.convert_dbf_to_sql("data.dbf", output_dir="sql_output")
    if success:
        print("✓ Conversion successful!")
    else:
        print("✗ Conversion failed!")

    # Example 2: Convert multiple files
    print("\nExample 2: Converting multiple DBF files")
    dbf_files = ["file1.dbf", "file2.dbf", "file3.dbf"]
    results = converter.convert_multiple_files(dbf_files)

    for file_path, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {file_path}: {status}")

    # Example 2b: Convert multiple files to a specific output directory
    print("\nExample 2b: Converting multiple DBF files to specific output directory")
    output_directory = "sql_output"
    results = converter.convert_multiple_files(dbf_files, output_dir=output_directory)

    for file_path, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {file_path} -> {output_directory}/: {status}")

    # Example 3: Find and convert all DBF files in a directory
    print("\nExample 3: Converting all DBF files in current directory")
    dbf_files = [f for f in os.listdir(".") if f.endswith(".dbf")]

    if dbf_files:
        print(f"Found {len(dbf_files)} DBF files")
        results = converter.convert_multiple_files(dbf_files)

        successful = sum(1 for success in results.values() if success)
        print(f"Successfully converted {successful} out of {len(dbf_files)} files")
    else:
        print("No DBF files found in current directory")


def batch_convert_directory(directory_path: str, output_dir: Optional[str] = None) -> None:
    """
    Convert all DBF files in a directory.

    Args:
        directory_path: Path to directory containing DBF files
        output_dir: Optional output directory for SQL files
    """
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    # Find all DBF files
    dbf_files: list[str] = []
    for root, _dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".dbf"):
                dbf_files.append(os.path.join(root, file))

    if not dbf_files:
        print(f"No DBF files found in {directory_path}")
        return

    print(f"Found {len(dbf_files)} DBF files in {directory_path}")

    # Initialize converter
    converter = DBFToSQLConverter(batch_size=1000)

    # Convert files
    for dbf_file in dbf_files:
        sql_path: Optional[str] = None
        if output_dir:
            # Generate output path in specified directory
            filename = os.path.basename(dbf_file)
            sql_filename = filename.replace(".dbf", ".sql")
            sql_path = os.path.join(output_dir, sql_filename)

            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

        success = converter.convert_dbf_to_sql(dbf_file, sql_path)
        status = "✓" if success else "✗"
        print(f"  {status} {dbf_file}")


if __name__ == "__main__":
    print("DBF to SQL Converter - Example Usage")
    print("=" * 40)

    # Run basic examples
    example_usage()

    # Example of batch conversion
    print("\n" + "=" * 40)
    print("Batch conversion example:")
    batch_convert_directory(".", "output_sql")
