import os
import sys
import subprocess
from .utils import check_command, log_warning, log_success, log_error, install_package, BOLD, RESET, RED

# Define paths relative to the virtual environment
VENV_BIN = os.path.join(sys.prefix, "bin")

TOOLS = {
    "maigret": {"cmd": os.path.join(VENV_BIN, "maigret"), "pip": "maigret"},
    "holehe": {"cmd": os.path.join(VENV_BIN, "holehe"), "pip": "holehe"},
    "sherlock": {"cmd": os.path.join(VENV_BIN, "sherlock"), "pip": "sherlock-project"},
    "h8mail": {"cmd": os.path.join(VENV_BIN, "h8mail"), "pip": "h8mail"},
    "telegram-checker": {"cmd": os.path.join(VENV_BIN, "telegram-phone-number-checker"), "pip": "telegram-phone-number-checker"},
    "ghunt": {"cmd": os.path.join(VENV_BIN, "ghunt"), "pip": "ghunt"},
}

def check_tools():
    """Checks for required tools and returns a status dict."""
    status = {}
    print(f"\n{BOLD}Checking Environment...{RESET}")
    for tool, details in TOOLS.items():
        # Check if the binary exists at the specific venv path
        if os.path.exists(details["cmd"]):
            log_success(f"{tool} found.")
            status[tool] = True
        else:
            log_warning(f"{tool} NOT found.")
            status[tool] = False
            
    # Check system tool ExifTool separately
    if check_command("exiftool"):
        log_success("exiftool found (System).")
        status["exiftool"] = True
    else:
        log_warning("exiftool NOT found. (Install via 'sudo apt install libimage-exiftool-perl' or similar)")
        status["exiftool"] = False
        
    return status

import shutil

def ensure_tool(tool_name):
    """Ensures a tool is available, offering to install if missing."""
    if tool_name == "exiftool":
        if check_command("exiftool"):
            return True
        
        print(f"\n{BOLD}{RED}ExifTool is missing.{RESET}")
        choice = input("Attempt to install via sudo apt? (You may be asked for your password) [Y/n] ").lower()
        
        if choice in ["", "y", "yes"]:
            try:
                print("Running: sudo apt-get install -y libimage-exiftool-perl")
                subprocess.check_call(["sudo", "apt-get", "install", "-y", "libimage-exiftool-perl"])
                log_success("ExifTool installed successfully!")
                return True
            except subprocess.CalledProcessError:
                log_error("Installation failed. Please run 'sudo apt-get install libimage-exiftool-perl' manually.")
                return False
            except FileNotFoundError:
                log_error("'sudo' not found. Please install ExifTool manually.")
                return False
        else:
             print("Skipping ExifTool installation.")
             return False

    if tool_name not in TOOLS:
        log_error(f"Unknown tool: {tool_name}")
        return False
        
    tool_path = TOOLS[tool_name]["cmd"]
    if os.path.exists(tool_path):
        return True
    
    # Prompt user
    choice = input(f"Tool '{tool_name}' is missing. Install via pip? [Y/n] ").lower()
    if choice in ["", "y", "yes"]:
        # Resolve specific dependency conflicts for Maigret
        if tool_name == "maigret":
             install_package("typing-extensions", upgrade=True)
             
        return install_package(TOOLS[tool_name]["pip"])
    return False
