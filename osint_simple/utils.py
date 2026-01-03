import sys
import shutil
import subprocess

# ANSI Colors
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"

def print_banner():
    print(f"""{CYAN}
   ____ _____ ___ _   _ _____   _____ _                 _      
  / __ \  ___|_ _| \ | |_   _| /  ___(_)               | |     
 | |  | \ `--.| ||  \| | | |   \ `--. _ _ __ ___  _ __ | | ___ 
 | |  | |`--. \ || . ` | | |    `--. \ | '_ ` _ \| '_ \| |/ _ \\
 | |__| /\__/ / || |\  | | |   /\__/ / | | | | | | |_) | |  __/
  \____/\____/___|_| \_/ \_/   \____/|_|_| |_| |_| .__/|_|\___|
                                                 | |           
                                                 |_|           
    {RESET}{BOLD}Unified OSINT Automation Wrapper{RESET}
    """)

def log_info(msg):
    print(f"[{BLUE}INFO{RESET}] {msg}")

def log_success(msg):
    print(f"[{GREEN}OK{RESET}] {msg}")

def log_warning(msg):
    print(f"[{YELLOW}WARN{RESET}] {msg}")

def log_error(msg):
    print(f"[{RED}ERR{RESET}] {msg}")

def check_command(cmd):
    """Checks if a command exists in the system path."""
    return shutil.which(cmd) is not None

def install_package(package_name, upgrade=False):
    """Attempts to install a python package via pip."""
    try:
        print(f"Installing {package_name}...")
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        if upgrade:
            cmd.append("--upgrade")
        subprocess.check_call(cmd)
        log_success(f"Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError:
        log_error(f"Failed to install {package_name}. Please install it manually.")
        return False
