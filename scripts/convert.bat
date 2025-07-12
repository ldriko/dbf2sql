@echo off
REM DBF to SQL Converter - Windows Batch Script
REM Usage: convert.bat file1.dbf file2.dbf ...

echo DBF to SQL Converter
echo ==================

if "%~1"=="" (
    echo Usage: convert.bat file1.dbf [file2.dbf ...]
    echo Example: convert.bat data.dbf customers.dbf
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Please run setup.py first.
    exit /b 1
)

REM Run the converter with all arguments
.venv\Scripts\python dbf2sql.py %*

echo.
echo Conversion completed!
pause
