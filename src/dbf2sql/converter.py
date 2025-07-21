"""
DBF to SQL Converter Core Module

Contains the main converter class and functionality.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

try:
    from dbfread import DBF  # type: ignore
except ImportError:
    print("Error: dbfread library not found. Please install it with: pip install dbfread")
    sys.exit(1)


class DBFToSQLConverter:
    """Memory-efficient DBF to SQL converter."""

    def __init__(self, batch_size: int = 1000, encoding: str = "utf-8"):
        """
        Initialize the converter.

        Args:
            batch_size: Number of records to process in each batch
            encoding: Character encoding for DBF files
        """
        self.batch_size = batch_size
        self.encoding = encoding
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger("dbf2sql")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _get_sql_type(self, field_type: str, field_length: int, field_decimal: int) -> str:
        """
        Convert DBF field type to SQL type.

        Args:
            field_type: DBF field type (C, N, D, L, etc.)
            field_length: Field length
            field_decimal: Decimal places

        Returns:
            SQL type string
        """
        type_mapping = {
            "C": f"VARCHAR({field_length})",  # Character
            "N": (
                f"DECIMAL({field_length},{field_decimal})" if field_decimal > 0 else "BIGINT"
            ),  # Numeric
            "D": "DATE",  # Date
            "L": "BOOLEAN",  # Logical
            "F": f"DECIMAL({field_length},{field_decimal})",  # Float
            "M": "TEXT",  # Memo
            "I": "INTEGER",  # Integer
            "B": "DOUBLE",  # Double
            "T": "DATETIME",  # DateTime
            "Y": "DECIMAL(19,4)",  # Currency
        }

        return type_mapping.get(field_type, f"VARCHAR({field_length})")

    def _escape_sql_value(self, value: Any) -> str:
        """
        Escape SQL values properly.

        Args:
            value: Value to escape

        Returns:
            Escaped SQL value string
        """
        if value is None:
            return "NULL"
        elif isinstance(value, str):
            # Escape single quotes by doubling them
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        elif isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            # Convert to string and escape
            escaped = str(value).replace("'", "''")
            return f"'{escaped}'"

    def _create_table_sql(self, table_name: str, fields: List[Dict[str, Any]]) -> str:
        """
        Generate CREATE TABLE SQL statement.

        Args:
            table_name: Name of the table
            fields: List of field definitions

        Returns:
            CREATE TABLE SQL statement
        """
        field_definitions: List[str] = []

        for field in fields:
            field_name = field["name"]
            sql_type = self._get_sql_type(field["type"], field["length"], field["decimal"])
            field_definitions.append(f"    {field_name} {sql_type}")

        return f"""-- Table: {table_name}
DROP TABLE IF EXISTS {table_name};
CREATE TABLE {table_name} (
{',\n'.join(field_definitions)}
);
"""

    def _process_records_batch(
        self, records: List[Dict[str, Any]], table_name: str, field_names: List[str]
    ) -> str:
        """
        Process a batch of records into a single INSERT statement.

        Args:
            records: List of record dictionaries
            table_name: Name of the table
            field_names: List of field names

        Returns:
            INSERT SQL statement
        """
        if not records:
            return ""

        # Build the INSERT statement
        field_list = ", ".join(field_names)
        values_list: List[str] = []

        for record in records:
            # Get values in the same order as field_names
            values = [self._escape_sql_value(record.get(field)) for field in field_names]
            values_list.append(f"({', '.join(values)})")

        # Combine all values into a single INSERT statement
        values_str = ",\n    ".join(values_list)

        return f"""INSERT INTO {table_name} ({field_list}) VALUES
    {values_str};
"""

    def convert_dbf_to_sql(self, dbf_file_path: str, sql_file_path: Optional[str] = None, output_dir: Optional[str] = None) -> bool:
        """
        Convert a DBF file to SQL file.

        Args:
            dbf_file_path: Path to the DBF file
            sql_file_path: Path to the output SQL file (optional)
            output_dir: Output directory for SQL files (optional)

        Returns:
            True if conversion was successful, False otherwise
        """
        try:
            dbf_path = Path(dbf_file_path)
            if not dbf_path.exists():
                self.logger.error(f"DBF file not found: {dbf_file_path}")
                return False

            # Generate SQL file path if not provided
            if sql_file_path is None:
                if output_dir is not None:
                    # Use specified output directory
                    output_path = Path(output_dir)
                    output_path.mkdir(parents=True, exist_ok=True)
                    sql_file_path = str(output_path / f"{dbf_path.stem}.sql")
                else:
                    # Use same directory as DBF file
                    sql_file_path = str(dbf_path.with_suffix(".sql"))

            self.logger.info(f"Converting {dbf_file_path} to {sql_file_path}")

            # Open DBF file
            with DBF(dbf_file_path, encoding=self.encoding, char_decode_errors="ignore") as dbf:
                # Get table name from filename (without extension)
                table_name = dbf_path.stem

                # Get field information
                fields: List[Dict[str, Any]] = []
                for field in dbf.fields:  # type: ignore
                    field_any = cast(Any, field)
                    field_info = {
                        "name": field_any.name,
                        "type": field_any.type,
                        "length": field_any.length,
                        "decimal": field_any.decimal_count,
                    }
                    fields.append(field_info)

                field_names: List[str] = [field["name"] for field in fields]

                self.logger.info(f"Table: {table_name}, Fields: {len(fields)}, Records: {len(dbf)}")

                # Write SQL file
                with open(sql_file_path, "w", encoding="utf-8") as sql_file:
                    # Write header comment
                    sql_file.write(f"-- Generated from {dbf_file_path}\n")
                    sql_file.write(f"-- Total records: {len(dbf)}\n")
                    sql_file.write("-- Generated by DBF2SQL Converter\n\n")

                    # Write CREATE TABLE statement
                    create_table_sql = self._create_table_sql(table_name, fields)
                    sql_file.write(create_table_sql)
                    sql_file.write("\n")

                    # Process records in batches
                    batch: List[Dict[str, Any]] = []
                    total_processed = 0

                    for record in cast(Any, dbf):
                        # Convert record to dict to ensure proper typing
                        record_dict: Dict[str, Any] = dict(record)
                        batch.append(record_dict)

                        if len(batch) >= self.batch_size:
                            # Process batch
                            insert_sql = self._process_records_batch(batch, table_name, field_names)
                            sql_file.write(insert_sql)
                            sql_file.write("\n")

                            total_processed += len(batch)
                            batch = []

                            if total_processed % (self.batch_size * 10) == 0:
                                self.logger.info(f"Processed {total_processed} records...")

                    # Process remaining records
                    if batch:
                        insert_sql = self._process_records_batch(batch, table_name, field_names)
                        sql_file.write(insert_sql)
                        sql_file.write("\n")
                        total_processed += len(batch)

                    # Write footer comment
                    sql_file.write(
                        f"-- Conversion completed: {total_processed} records processed\n"
                    )

                self.logger.info(
                    f"Successfully converted {total_processed} records to {sql_file_path}"
                )
                return True

        except Exception as e:
            self.logger.error(f"Error converting {dbf_file_path}: {str(e)}")
            return False

    def convert_multiple_files(self, dbf_files: List[str], output_dir: Optional[str] = None) -> Dict[str, bool]:
        """
        Convert multiple DBF files to SQL files.

        Args:
            dbf_files: List of DBF file paths
            output_dir: Output directory for SQL files (optional)

        Returns:
            Dictionary mapping file paths to conversion success status
        """
        results: Dict[str, bool] = {}

        for dbf_file in dbf_files:
            self.logger.info(f"Starting conversion of {dbf_file}")
            results[dbf_file] = self.convert_dbf_to_sql(dbf_file, output_dir=output_dir)

        return results
