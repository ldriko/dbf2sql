#!/bin/bash
# DBF to SQL Converter - Unix/Linux Shell Script
# Usage: ./convert.sh file1.dbf file2.dbf ...

echo "DBF to SQL Converter"
echo "===================="

if [ $# -eq 0 ]; then
    echo "Usage: $0 file1.dbf [file2.dbf ...]"
    echo "Example: $0 data.dbf customers.dbf"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Virtual environment not found. Please run setup.py first."
    exit 1
fi

# Run the converter with all arguments
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/dbf2sql.py" "$@"

echo
echo "Conversion completed!"
