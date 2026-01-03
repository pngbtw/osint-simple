#!/usr/bin/env python3
import sys
import os
import subprocess
from osint_simple.main import main

VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")

def in_venv():
    return sys.prefix == VENV_DIR

def create_venv():
    print("Setting up virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("Virtual environment created.")
        
        # Upgrade pip inside venv
        pip_bin = os.path.join(VENV_DIR, "bin", "pip")
        subprocess.check_call([pip_bin, "install", "--upgrade", "pip"])
        
        # Install requests immediately as it's a core dependency
        subprocess.check_call([pip_bin, "install", "requests"])
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating venv: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists(VENV_DIR):
        create_venv()

    if not in_venv():
        # Re-execute this script using the venv's python
        python_bin = os.path.join(VENV_DIR, "bin", "python")
        try:
            os.execv(python_bin, [python_bin] + sys.argv)
        except OSError as e:
            print(f"Failed to activate venv: {e}")
            sys.exit(1)
            
    # If we are here, we are in the venv
    main()
