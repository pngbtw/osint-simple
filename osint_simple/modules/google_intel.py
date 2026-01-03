import subprocess
import sys
from ..utils import log_info, log_error, BOLD, RESET
from ..manager import TOOLS

def ghunt_login():
    """Helper to run ghunt login."""
    log_info("Starting GHunt Login...")
    log_info("You will need to follow the instructions to paste your Google cookies.")
    try:
        subprocess.run([TOOLS["ghunt"]["cmd"], "login"])
    except Exception as e:
        log_error(f"Login failed: {e}")

def check_gmail(email):
    """Wraps GHunt to check a Gmail address."""
    log_info(f"Running GHunt for '{email}'...")
    
    # GHunt requires 'email' command from the 'ghunt' package
    # command structure: ghunt email <address>
    cmd = [TOOLS["ghunt"]["cmd"], "email", email]
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=1
        )
        
        print(f"\n{BOLD}Results:{RESET}")
        for line in process.stdout:
            print(line, end='')
            
        process.wait()
        
        if process.returncode != 0:
            log_error("GHunt finished with errors. You might need to configure cookies (run 'ghunt login' in terminal).")
            
    except Exception as e:
        log_error(f"Execution failed: {e}")
