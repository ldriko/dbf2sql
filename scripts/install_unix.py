#!/usr/bin/env python3
"""
System-wide installer for DBF to SQL Converter (Unix/Linux)
"""

import os
import sys
import shutil
import stat
from pathlib import Path

def install_system_wide():
    """Install the converter system-wide on Unix/Linux."""
    
    # Check if running as root/sudo
    if os.geteuid() != 0:
        print("This script needs to be run with sudo privileges to install system-wide.")
        print("Usage: sudo python3 install_unix.py")
        sys.exit(1)
    
    # Define paths
    script_dir = Path(__file__).parent
    bin_dir = Path("/usr/local/bin")
    lib_dir = Path("/usr/local/lib/dbf2sql")
    
    try:
        # Create lib directory
        lib_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy main script and dependencies
        files_to_copy = [
            "dbf2sql.py",
            "dbfread.pyi",
            "requirements.txt"
        ]
        
        for file in files_to_copy:
            src = script_dir / file
            dst = lib_dir / file
            if src.exists():
                shutil.copy2(src, dst)
                print(f"Copied {file} to {dst}")
        
        # Create wrapper script in /usr/local/bin
        wrapper_content = f"""#!/bin/bash
# DBF to SQL Converter - System wrapper
SCRIPT_DIR="{lib_dir}"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python3 "$SCRIPT_DIR/dbf2sql.py" "$@"
"""
        
        wrapper_path = bin_dir / "dbf2sql"
        with open(wrapper_path, 'w') as f:
            f.write(wrapper_content)
        
        # Make wrapper executable
        wrapper_path.chmod(wrapper_path.stat().st_mode | stat.S_IEXEC)
        
        print(f"Created executable wrapper at {wrapper_path}")
        print("\nInstallation complete!")
        print("You can now run 'dbf2sql' from anywhere in the system.")
        print("Example: dbf2sql myfile.dbf")
        
    except Exception as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_system_wide()
