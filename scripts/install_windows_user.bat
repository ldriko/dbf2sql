@echo off
REM DBF to SQL Converter - Windows User Installer
REM No administrator privileges required

echo DBF to SQL Converter - Windows User Installer
echo ==============================================

REM Define paths
set INSTALL_DIR=%USERPROFILE%\AppData\Local\DBF2SQL
set SCRIPT_NAME=dbf2sql.bat

REM Create installation directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying files to %INSTALL_DIR%...
copy dbf2sql.py "%INSTALL_DIR%\"
copy dbfread.pyi "%INSTALL_DIR%\"
copy requirements.txt "%INSTALL_DIR%\"

REM Create batch wrapper
echo Creating user command wrapper...
echo @echo off > "%INSTALL_DIR%\%SCRIPT_NAME%"
echo REM DBF to SQL Converter - User wrapper >> "%INSTALL_DIR%\%SCRIPT_NAME%"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\%SCRIPT_NAME%"
echo python "%INSTALL_DIR%\dbf2sql.py" %%* >> "%INSTALL_DIR%\%SCRIPT_NAME%"

REM Add to user PATH
echo Adding to user PATH...
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set CURRENT_PATH=%%B
if "%CURRENT_PATH%"=="" set CURRENT_PATH=%PATH%
echo %CURRENT_PATH% | find "%INSTALL_DIR%" >nul
if %errorlevel% neq 0 (
    reg add "HKCU\Environment" /v PATH /t REG_SZ /d "%CURRENT_PATH%;%INSTALL_DIR%" /f
    echo User PATH updated successfully
) else (
    echo User PATH already contains installation directory
)

echo.
echo Installation complete!
echo The 'dbf2sql' command is now available for your user account.
echo You may need to restart your command prompt for PATH changes to take effect.
echo.
echo Usage: dbf2sql myfile.dbf
echo.
pause
