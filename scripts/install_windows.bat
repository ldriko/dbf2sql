@echo off
REM DBF to SQL Converter - Windows System Installer
REM Run as Administrator

echo DBF to SQL Converter - Windows System Installer
echo ================================================

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - OK
) else (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

REM Define paths
set INSTALL_DIR=C:\Program Files\DBF2SQL
set SCRIPT_NAME=dbf2sql.bat

REM Create installation directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying files to %INSTALL_DIR%...
copy dbf2sql.py "%INSTALL_DIR%\"
copy dbfread.pyi "%INSTALL_DIR%\"
copy requirements.txt "%INSTALL_DIR%\"

REM Create batch wrapper
echo Creating system command wrapper...
echo @echo off > "%INSTALL_DIR%\%SCRIPT_NAME%"
echo REM DBF to SQL Converter - System wrapper >> "%INSTALL_DIR%\%SCRIPT_NAME%"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\%SCRIPT_NAME%"
echo python "%INSTALL_DIR%\dbf2sql.py" %%* >> "%INSTALL_DIR%\%SCRIPT_NAME%"

REM Add to system PATH
echo Adding to system PATH...
for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH') do set CURRENT_PATH=%%B
echo %CURRENT_PATH% | find "%INSTALL_DIR%" >nul
if %errorlevel% neq 0 (
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_SZ /d "%CURRENT_PATH%;%INSTALL_DIR%" /f
    echo PATH updated successfully
) else (
    echo PATH already contains installation directory
)

echo.
echo Installation complete!
echo The 'dbf2sql' command is now available system-wide.
echo You may need to restart your command prompt or reboot for PATH changes to take effect.
echo.
echo Usage: dbf2sql myfile.dbf
echo.
pause
