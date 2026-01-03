import subprocess
from ..utils import log_info, log_error, BOLD, RESET
from ..manager import TOOLS

def gather_intel(domain, limit=50, source="all"):
    """Wraps theHarvester to gather emails, subdomains, etc."""
    log_info(f"Running theHarvester on {domain} (Limit: {limit})...")
    
    cmd = [TOOLS["theHarvester"]["cmd"], "-d", domain, "-l", str(limit), "-b", source]
    
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
            # theHarvester can be verbose, maybe filter? For now, print all.
            print(line, end='')
            
        process.wait()
        
    except FileNotFoundError:
        log_error("theHarvester executable not found.")
    except Exception as e:
        log_error(f"Execution failed: {e}")
