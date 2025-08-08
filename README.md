# DBF to SQL Converter

A memory-efficient Python application to convert DBF (dBase) files to SQL INSERT statements. The tool processes large files efficiently by using batch processing and combining multiple records into single INSERT statements for optimal database performance.

## Features

- **Memory Efficient**: Processes records in configurable batches to handle large files
- **Fast SQL Generation**: Combines multiple records into single INSERT statements
- **Automatic Schema Detection**: Automatically generates CREATE TABLE statements based on DBF field types
- **Multiple File Support**: Process multiple DBF files in one command
- **Encoding Support**: Configurable character encoding for different DBF file formats
- **Error Handling**: Robust error handling with detailed logging
- **Progress Tracking**: Shows conversion progress for large files

## Installation

### From PyPI (Recommended)
```bash
pip install dbf2sql
```

### From Source
```bash
git clone https://github.com/yourusername/dbf2sql.git
cd dbf2sql
pip install -e .
```

### Development Setup
```bash
git clone https://github.com/yourusername/dbf2sql.git
cd dbf2sql
make dev-setup
```

## Usage

### Basic Usage

Convert a single DBF file:
```bash
dbf2sql data.dbf
```

Convert multiple DBF files:
```bash
dbf2sql file1.dbf file2.dbf file3.dbf
```

Convert all DBF files in a folder:
```bash
dbf2sql --folder /path/to/dbf/files
```

Convert all DBF files in a folder to specific output directory:
```bash
dbf2sql --folder /path/to/dbf/files --output-dir /path/to/output
```

### Advanced Options

```bash
dbf2sql --batch-size 2000 --encoding cp1252 --output-dir sql_output data/*.dbf
```

### Using as a Python Library

```python
from dbf2sql import DBFToSQLConverter

# Create converter instance
converter = DBFToSQLConverter(batch_size=1000, encoding='utf-8')

# Convert a single file
success = converter.convert_dbf_to_sql('data.dbf', 'output.sql')

# Convert a single file to specific output directory
success = converter.convert_dbf_to_sql('data.dbf', output_dir='sql_output')

# Convert multiple files
results = converter.convert_multiple_files(['file1.dbf', 'file2.dbf'])

# Convert multiple files to specific output directory
results = converter.convert_multiple_files(['file1.dbf', 'file2.dbf'], output_dir='sql_output')
```

### Command Line Options

- `dbf_files`: One or more DBF files to convert (required if --folder not used)
- `--folder, -f`: Folder containing DBF files to convert (searches recursively)
- `--batch-size`: Number of records to process in each batch (default: 1000)
- `--encoding`: Character encoding for DBF files (default: utf-8)
- `--output-dir, -o`: Output directory for SQL files (default: same directory as DBF files)
- `--verbose, -v`: Enable verbose logging

## Output

For each input DBF file, the tool generates:
- A SQL file with the same name but `.sql` extension
- By default, SQL files are created in the same directory as the DBF files
- With `--output-dir` option, SQL files are created in the specified directory
- CREATE TABLE statement with appropriate field types
- INSERT statements with batched records for optimal performance
- Comments with file information and record counts

## Performance Optimizations

1. **Batch Processing**: Records are processed in configurable batches (default: 1000)
2. **Single INSERT Statements**: Multiple records are combined into single INSERT statements
3. **Memory Efficient**: Uses iterators to avoid loading entire files into memory
4. **Optimized SQL Types**: Automatic mapping of DBF field types to appropriate SQL types

## Supported DBF Field Types

| DBF Type | SQL Type | Description |
|----------|----------|-------------|
| C | VARCHAR(n) | Character |
| N | DECIMAL(n,d) or BIGINT | Numeric |
| D | DATE | Date |
| L | BOOLEAN | Logical |
| F | DECIMAL(n,d) | Float |
| M | TEXT | Memo |
| I | INTEGER | Integer |
| B | DOUBLE | Double |
| T | DATETIME | DateTime |
| Y | DECIMAL(19,4) | Currency |

## Examples

### Convert a single file
```bash
dbf2sql customers.dbf
# Output: customers.sql
```

### Convert multiple files with custom batch size
```bash
dbf2sql --batch-size 5000 sales.dbf products.dbf orders.dbf
# Output: sales.sql, products.sql, orders.sql
```

### Convert files with specific encoding
```bash
dbf2sql --encoding cp1252 legacy_data.dbf
# Output: legacy_data.sql
```

### Convert files to specific output directory
```bash
dbf2sql --output-dir /path/to/output customers.dbf orders.dbf
# Output: /path/to/output/customers.sql, /path/to/output/orders.sql
```

### Short form of output directory option
```bash
dbf2sql -o sql_files data/*.dbf
# Output: All SQL files in sql_files/ directory
```

### Verbose output
```bash
dbf2sql --verbose large_file.dbf
# Shows detailed progress and debug information
```

### Convert all DBF files in a folder
```bash
dbf2sql --folder /path/to/data/folder
# Finds and converts all .dbf and .DBF files recursively
```

### Convert folder with output directory
```bash
dbf2sql --folder /source/folder --output-dir /output/folder
# All SQL files created in /output/folder
```

## Error Handling

The tool includes comprehensive error handling:
- Invalid file paths
- Corrupted DBF files
- Encoding issues
- Permission errors
- Disk space issues

Failed conversions are reported in the summary, and the tool exits with an appropriate error code.

## Project Structure

```
dbf2sql/
├── src/
│   └── dbf2sql/
│       ├── __init__.py       # Package initialization
│       ├── converter.py      # Main converter class
│       ├── cli.py           # Command-line interface
│       ├── py.typed         # Type hints marker
│       └── dbfread.pyi      # Type stubs for dbfread
├── tests/
│   ├── __init__.py
│   └── test_converter.py    # Test cases
├── scripts/
│   ├── example_usage.py     # Usage examples
│   ├── diagnostic.py       # Diagnostic tool
│   └── install_*.py        # Installation scripts
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml          # Modern Python packaging
├── setup.py               # Package setup
├── Makefile              # Development commands
└── README.md             # This file
```

## Development

### Setup Development Environment
```bash
make dev-setup
```

### Run Tests
```bash
make test
```

### Format Code
```bash
make format
```

### Check Code Quality
```bash
make lint
make check-types
```

### Build Package
```bash
make build
```

## Contributing

Feel free to submit issues or pull requests to improve the tool.

## License

This tool is provided as-is for educational and practical use.
