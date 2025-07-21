"""
Command Line Interface for DBF to SQL Converter
"""

import argparse
import logging
import sys

from .converter import DBFToSQLConverter


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
  dbf2sql --help
        """,
    )

    parser.add_argument("dbf_files", nargs="+", help="DBF files to convert")

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
        "--output-dir", "-o", 
        type=str, 
        help="Output directory for SQL files (default: same directory as DBF files)"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    # Set up logging level
    if args.verbose:
        logging.getLogger("dbf2sql").setLevel(logging.DEBUG)

    # Create converter
    converter = DBFToSQLConverter(batch_size=args.batch_size, encoding=args.encoding)

    # Convert files
    results = converter.convert_multiple_files(args.dbf_files, output_dir=args.output_dir)

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
