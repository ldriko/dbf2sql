"""
DBF to SQL Converter

A memory-efficient Python package to convert DBF (dBase) files to SQL INSERT statements.
"""

from .cli import main
from .converter import DBFToSQLConverter

__version__ = "1.0.0"
__author__ = "DBF2SQL Team"
__email__ = "contact@dbf2sql.com"

__all__ = ["DBFToSQLConverter", "main"]
