#!/usr/bin/env python3
"""
User-level installer for DBF to SQL Converter (Unix/Linux)
"""

import os
import sys
import shutil
import stat
from pathlib import Path

def install_user_level():
    """Install the converter for current user only."""
    
    # Define paths
    script_dir = Path(__file__).parent
    home_dir = Path.home()
    bin_dir = home_dir / ".local" / "bin"
    lib_dir = home_dir / ".local" / "lib" / "dbf2sql"
    
    try:
        # Create directories
        bin_dir.mkdir(parents=True, exist_ok=True)
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
        
        # Create wrapper script
        wrapper_content = f"""#!/bin/bash
# DBF to SQL Converter - User wrapper
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
        
        # Check if ~/.local/bin is in PATH
        path_env = os.environ.get('PATH', '')
        if str(bin_dir) not in path_env:
            print(f"\nIMPORTANT: Add {bin_dir} to your PATH")
            print("Add this line to your ~/.bashrc or ~/.zshrc:")
            print(f'export PATH="$PATH:{bin_dir}"')
            print("Then run: source ~/.bashrc (or ~/.zshrc)")
        
        print("\nInstallation complete!")
        print("You can now run 'dbf2sql' from anywhere in the system.")
        print("Example: dbf2sql myfile.dbf")
        
    except Exception as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_user_level()
