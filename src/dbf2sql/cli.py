"""
Command Line Interface for DBF to SQL Converter
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

from .converter import DBFToSQLConverter


def find_dbf_files_in_folder(folder_path: str) -> List[str]:
    """
    Find all DBF files in a folder and its subdirectories.

    Args:
        folder_path: Path to the folder to search

    Returns:
        List of DBF file paths
    """
    dbf_files: List[str] = []
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder_path}")

    # Find all .dbf files recursively
    for dbf_file in folder.rglob("*.dbf"):
        dbf_files.append(str(dbf_file))

    # Also check for .DBF files (uppercase)
    for dbf_file in folder.rglob("*.DBF"):
        dbf_files.append(str(dbf_file))

    return sorted(dbf_files)


def main() -> None:
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert DBF files to SQL files efficiently",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dbf2sql file1.dbf file2.dbf
  dbf2sql --batch-size 2000 --encoding cp1252 data/*.dbf
  dbf2sql --output-dir /path/to/output data/*.dbf
  dbf2sql -o output_folder file1.dbf file2.dbf
  dbf2sql --folder /path/to/dbf/folder
  dbf2sql --folder /path/to/dbf/folder --output-dir /path/to/output
  dbf2sql --help
        """,
    )

    parser.add_argument("dbf_files", nargs="*", help="DBF files to convert")

    parser.add_argument(
        "--folder",
        "-f",
        type=str,
        help="Folder containing DBF files to convert (searches recursively)",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of records to process in each batch (default: 1000)",
    )

    parser.add_argument(
        "--encoding", default="utf-8", help="Character encoding for DBF files (default: utf-8)"
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        help="Output directory for SQL files (default: same directory as DBF files)",
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    # Validate arguments
    if not args.dbf_files and not args.folder:
        parser.error("You must specify either DBF files or use --folder option")

    if args.dbf_files and args.folder:
        parser.error("Cannot specify both DBF files and --folder option. Use one or the other.")

    # Set up logging level
    if args.verbose:
        logging.getLogger("dbf2sql").setLevel(logging.DEBUG)

    # Determine which files to process
    if args.folder:
        try:
            dbf_files = find_dbf_files_in_folder(args.folder)
            if not dbf_files:
                print(f"No DBF files found in folder: {args.folder}")
                sys.exit(1)
            print(f"Found {len(dbf_files)} DBF file(s) in folder: {args.folder}")
        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        dbf_files = args.dbf_files

    # Create converter
    converter = DBFToSQLConverter(batch_size=args.batch_size, encoding=args.encoding)

    # Convert files
    results = converter.convert_multiple_files(dbf_files, output_dir=args.output_dir)

    # Print summary
    successful = sum(1 for success in results.values() if success)
    total = len(results)

    print("\nConversion Summary:")
    print(f"  Total files: {total}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {total - successful}")

    if successful < total:
        print("\nFailed files:")
        for file_path, success in results.items():
            if not success:
                print(f"  - {file_path}")

    # Exit with appropriate code
    sys.exit(0 if successful == total else 1)


if __name__ == "__main__":
    main()
