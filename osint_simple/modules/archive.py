import requests
import json
import sys
from datetime import datetime
from ..utils import log_info, log_success, log_error, BOLD, RESET

WAYBACK_CDX_URL = "https://web.archive.org/cdx/search/cdx"
WAYBACK_SAVE_URL = "https://web.archive.org/save/"

def search_history(domain, limit=10):
    """Searches the Wayback Machine for snapshots of a domain."""
    log_info(f"Searching Wayback Machine for {domain}...")
    
    params = {
        'url': domain,
        'output': 'json',
        'fl': 'timestamp,original,statuscode',
        'collapse': 'digest',
        'limit': limit
    }
    
    try:
        response = requests.get(WAYBACK_CDX_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data or len(data) <= 1: # Header only
                log_info("No archives found.")
                return

            print(f"\n{BOLD}Found {len(data)-1} snapshots:{RESET}")
            # data[0] is header ['timestamp', 'original', 'statuscode']
            for row in data[1:]:
                ts, url, status = row
                # Format timestamp YYYYMMDDHHMMSS -> YYYY-MM-DD HH:MM:SS
                dt = datetime.strptime(ts, "%Y%m%d%H%M%S")
                print(f"[{dt}] Status: {status} -> {url}")
                print(f"   View: https://web.archive.org/web/{ts}/{url}")
        else:
            if response.status_code == 503:
                log_error("Wayback Machine API is currently unavailable (503 Service Unavailable). Try again in a few minutes.")
            else:
                log_error(f"API Error: {response.status_code}")
            
    except Exception as e:
        log_error(f"Failed to connect: {e}")

def save_url(url):
    """Submits a URL to the Wayback Machine for archiving."""
    log_info(f"Attempting to archive {url}...")
    target = f"{WAYBACK_SAVE_URL}{url}"
    
    try:
        # User-agent is often required to avoid 403s on save
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; OSINTSimple/1.0)'}
        response = requests.get(target, headers=headers)
        
        if response.status_code == 200:
            log_success(f"Archived successfully! Check: {target}")
        elif response.status_code == 403:
             log_error("Access Forbidden. Wayback Machine might be blocking automated requests.")
        else:
            log_error(f"Failed to archive. Status: {response.status_code}")
            
    except Exception as e:
        log_error(f"Error: {e}")
