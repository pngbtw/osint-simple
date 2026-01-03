import subprocess
from ..utils import log_info, log_error, BOLD, RESET
from ..manager import TOOLS

def check_leaks(target):
    """Wraps h8mail to check for breach data."""
    log_info(f"Running h8mail for {target}...")
    
    # h8mail -t target
    cmd = [TOOLS["h8mail"]["cmd"], "-t", target]
    
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
        
    except FileNotFoundError:
        log_error("h8mail executable not found.")
    except Exception as e:
        log_error(f"Execution failed: {e}")
