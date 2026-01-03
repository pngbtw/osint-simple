import subprocess
import sys
from ..utils import log_info, log_error, BOLD, RESET
from ..manager import TOOLS

def check_email_presence(email):
    """Wraps Holehe to check which sites an email is registered on."""
    log_info(f"Running Holehe for '{email}'...")
    
    cmd = [TOOLS["holehe"]["cmd"], email]
    
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
            # Holehe uses colors in terminal, we try to preserve or clean
            print(line, end='')
            
        process.wait()
        
    except Exception as e:
        log_error(f"Execution failed: {e}")
