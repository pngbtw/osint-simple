import subprocess
import sys
import os
import getpass
from ..utils import log_info, log_error, log_warning, log_success, BOLD, RESET, CYAN
from ..manager import TOOLS

ENV_FILE = ".env"

def setup_config():
    """Checks for .env configuration and prompts user if missing."""
    if os.path.exists(ENV_FILE):
        return

    print(f"\n{BOLD}{CYAN}--- First Time Setup: Telegram Checker ---{RESET}")
    print("To use this tool, you need Telegram API credentials.")
    print("1. Go to https://my.telegram.org")
    print("2. Log in and go to 'API development tools'")
    print("3. Create a new app (any name works) to get your API_ID and API_HASH")
    print(f"{BOLD}These credentials will be saved to '{ENV_FILE}' for future use.{RESET}\n")

    api_id = input("Enter your API_ID: ").strip()
    api_hash = getpass.getpass("Enter your API_HASH (hidden): ").strip()
    phone = input("Enter YOUR Phone Number (international format, e.g. +1234567890): ").strip()

    if not api_id or not api_hash or not phone:
        log_error("Missing information. Skipping setup. Tool might fail.")
        return

    try:
        with open(ENV_FILE, "w") as f:
            f.write(f"API_ID={api_id}\n")
            f.write(f"API_HASH={api_hash}\n")
            f.write(f"PHONE_NUMBER={phone}\n")
        log_success("Configuration saved to .env")
    except Exception as e:
        log_error(f"Failed to save .env: {e}")

def check_phone(phone_number):
    """Wraps bellingcat/telegram-phone-number-checker."""
    # Ensure config exists before running
    setup_config()
    
    log_info(f"Checking Telegram for target: {phone_number}")
    
    cmd = [TOOLS["telegram-checker"]["cmd"], "--phone-numbers", phone_number]
    
    try:
        # We expect the tool to pick up the .env file automatically
        process = subprocess.run(
            cmd,
            text=True
        )
        
        if process.returncode != 0:
            log_error("Telegram check failed.")
            print(f"Tip: If authentication failed, try deleting '{ENV_FILE}' and re-running to update credentials.")
            
    except Exception as e:
        log_error(f"Execution failed: {e}")

def show_instructions():
    # Helper to trigger setup if needed
    setup_config()