import subprocess
import sys
from ..utils import log_info, log_error, BOLD, RESET
from ..manager import TOOLS

def search_username(username):
    """Wraps Maigret to search for a username across hundreds of sites."""
    log_info(f"Running Maigret for '{username}'...")
    
    # Maigret is very powerful and provides a lot of info
    cmd = [TOOLS["maigret"]["cmd"], username, "--timeout", "10", "--pdf"]
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=1
        )
        
        print(f"\n{BOLD}Results (Streaming):{RESET}")
        for line in process.stdout:
            # Maigret output can be dense, we show progress
            if "Found" in line or "Search in" in line:
                print(line, end='')
            
        process.wait()
        log_info(f"Maigret finished. Report saved if generated.")
        
    except Exception as e:
        log_error(f"Execution failed: {e}")
