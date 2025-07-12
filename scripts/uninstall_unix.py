#!/usr/bin/env python3
"""
Uninstaller for DBF to SQL Converter (Unix/Linux)
"""

import os
import sys
import shutil
from pathlib import Path

def uninstall_system():
    """Uninstall system-wide installation."""
    if os.geteuid() != 0:
        print("This script needs to be run with sudo privileges to uninstall system-wide.")
        print("Usage: sudo python3 uninstall_unix.py")
        sys.exit(1)
    
    # Define paths
    bin_path = Path("/usr/local/bin/dbf2sql")
    lib_dir = Path("/usr/local/lib/dbf2sql")
    
    try:
        # Remove executable
        if bin_path.exists():
            bin_path.unlink()
            print(f"Removed {bin_path}")
        
        # Remove lib directory
        if lib_dir.exists():
            shutil.rmtree(lib_dir)
            print(f"Removed {lib_dir}")
        
        print("System-wide uninstallation complete!")
        
    except Exception as e:
        print(f"Uninstallation failed: {e}")
        sys.exit(1)

def uninstall_user():
    """Uninstall user-level installation."""
    # Define paths
    home_dir = Path.home()
    bin_path = home_dir / ".local" / "bin" / "dbf2sql"
    lib_dir = home_dir / ".local" / "lib" / "dbf2sql"
    
    try:
        # Remove executable
        if bin_path.exists():
            bin_path.unlink()
            print(f"Removed {bin_path}")
        
        # Remove lib directory
        if lib_dir.exists():
            shutil.rmtree(lib_dir)
            print(f"Removed {lib_dir}")
        
        print("User-level uninstallation complete!")
        
    except Exception as e:
        print(f"Uninstallation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--user":
        uninstall_user()
    else:
        uninstall_system()
