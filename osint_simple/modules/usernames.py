import subprocess
import sys
from ..utils import log_info, log_error, BOLD, RESET
from ..manager import TOOLS

def check_usernames(username):
    """Wraps Sherlock to check for a username across platforms."""
    log_info(f"Running Sherlock for '{username}'...")
    
    # Use absolute path from TOOLS
    cmd = [TOOLS["sherlock"]["cmd"], username, "--timeout", "5", "--print-found"]
    
    try:
        # Run and stream output
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
            # Check stderr if something went wrong
            err = process.stderr.read()
            if err:
                log_error(f"Sherlock encountered an error: {err}")
                
    except FileNotFoundError:
        log_error("Sherlock executable not found. Please run environment check.")
    except Exception as e:
        log_error(f"Execution failed: {e}")
