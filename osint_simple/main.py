import sys
import argparse
from .utils import print_banner, log_error, install_package, BOLD, RESET, CYAN, YELLOW
from .manager import check_tools, ensure_tool, TOOLS

# Try importing requests, install if missing
try:
    import requests
except ImportError:
    print("Core library 'requests' is missing.")
    install_package("requests")
    import requests

# Import modules
from .modules import usernames, social, email_check, leaks, archive, telegram, google_intel, geo, darkweb

def interactive_mode():
    print_banner()
    tools_status = check_tools()
    
    while True:
        print(f"\n{BOLD}--- PEOPLE SEARCH ---{RESET}")
        print(f"1. {CYAN}Usernames (Maigret){RESET} - Deep search {'[Ready]' if tools_status.get('maigret') else '[Missing]'}")
        print(f"2. {CYAN}Usernames (Sherlock){RESET} - Classic search {'[Ready]' if tools_status.get('sherlock') else '[Missing]'}")
        print(f"3. {CYAN}Email Check (Holehe){RESET} - Registered sites {'[Ready]' if tools_status.get('holehe') else '[Missing]'}")
        print(f"4. {CYAN}Google/Gmail (GHunt){RESET} - Account Intel {'[Ready]' if tools_status.get('ghunt') else '[Missing]'}")
        print(f"5. {CYAN}Leak Check (h8mail){RESET} - Breach data {'[Ready]' if tools_status.get('h8mail') else '[Missing]'}")
        print(f"6. {CYAN}Telegram Checker{RESET} - Phone to Telegram {'[Ready]' if tools_status.get('telegram-checker') else '[Missing]'}")
        
        print(f"\n{BOLD}--- DEEP WEB & GEO ---{RESET}")
        print(f"7. {CYAN}Dark Web Search{RESET} (Ahmia) - Onion Mentions")
        print(f"8. {CYAN}Metadata (ExifTool){RESET} - Images/PDFs {'[Ready]' if tools_status.get('exiftool') else '[Missing (System)]'}")
        print(f"9. {CYAN}IP Geolocation{RESET} - Trace IP Address")
        
        print(f"\n{BOLD}--- GENERAL ---{RESET}")
        print(f"10. {CYAN}Archive/History{RESET} (Wayback Machine)")
        print("99. Install Missing Tools")
        print("0. Exit")
        
        choice = input("\n> ")
        
        if choice == "1":
            if ensure_tool("maigret"):
                target = input("Enter username: ")
                social.search_username(target)
            else:
                log_error("Maigret is required.")
                
        elif choice == "2":
            if ensure_tool("sherlock"):
                target = input("Enter username: ")
                usernames.check_usernames(target)
            else:
                log_error("Sherlock is required.")
                
        elif choice == "3":
            if ensure_tool("holehe"):
                target = input("Enter email: ")
                email_check.check_email_presence(target)
            else:
                log_error("Holehe is required.")
        
        elif choice == "4":
            if ensure_tool("ghunt"):
                sub = input("1. Search Gmail\n2. GHunt Login (Configure cookies)\n> ")
                if sub == "1":
                    target = input("Enter Gmail address: ")
                    google_intel.check_gmail(target)
                elif sub == "2":
                    google_intel.ghunt_login()
            else:
                log_error("GHunt is required.")

        elif choice == "5":
            if ensure_tool("h8mail"):
                target = input("Enter email or handle: ")
                leaks.check_leaks(target)
            else:
                log_error("h8mail is required.")

        elif choice == "6":
            if ensure_tool("telegram-checker"):
                # telegram.show_instructions() # Deprecated, handled inside check_phone
                target = input("Enter phone number (with +, e.g. +123456789): ")
                telegram.check_phone(target)
            else:
                log_error("Telegram checker is required.")
        
        elif choice == "7":
            print(f"\n{BOLD}{CYAN}--- DARK WEB SEARCH GUIDE ---{RESET}")
            print("This tool searches .onion sites via Ahmia and Torry.")
            print(f"{BOLD}Note:{RESET} For reliable results, you should have Tor running locally.")
            print(f"      Install: {CYAN}sudo apt install tor{RESET}")
            print(f"      Start:   {CYAN}sudo systemctl start tor{RESET}")
            print("If Tor is not found, we will use Unreliable Clearnet Mirrors.\n")
            
            print(f"{YELLOW}{BOLD}PRO TIP:{RESET} For deeper historic footprinting (breaches, social, IPs),")
            print(f"visit {CYAN}https://oathnet.org/{RESET} manually in your browser.")
            print("-" * 40 + "\n")
            
            target = input("Enter keyword (username, email, etc.): ")
            print("Time Filter:")
            print("0. All Time (Default)")
            print("1. Last 24 Hours")
            print("2. Last 7 Days")
            print("3. Last 30 Days")
            tf = input("Select filter [0-3]: ")
            
            days = None
            if tf == "1": days = "1"
            elif tf == "2": days = "7"
            elif tf == "3": days = "30"
            
            darkweb.search_ahmia(target, days)

        elif choice == "8":
            if ensure_tool("exiftool"):
                target = input("Enter path to file: ")
                geo.extract_metadata(target)
            else:
                log_error("ExifTool is missing.")
                
        elif choice == "9":
            target = input("Enter IP Address: ")
            geo.geolocate_ip(target)

        elif choice == "10":
            sub = input("1. Search History\n2. Save URL\n> ")
            if sub == "1":
                target = input("Enter domain/URL: ")
                archive.search_history(target)
            elif sub == "2":
                target = input("Enter URL to save: ")
                archive.save_url(target)
                
        elif choice == "99":
            print(f"\n{BOLD}Verifying dependencies...{RESET}")
            status = check_tools()
            missing = [name for name, installed in status.items() if not installed]
            
            if not missing:
                print(f"\n{CYAN}{BOLD}Everything is already installed and ready!{RESET}")
            else:
                print(f"\nInstalling {len(missing)} missing tools...")
                for tool in missing:
                    ensure_tool(tool)
                print(f"\n{CYAN}{BOLD}Installation process complete.{RESET}")
            
            input("\nPress Enter to return to menu...")
            tools_status = status # Use the status we already fetched to avoid double printing
            continue # Force immediate return to menu start
            
        elif choice == "0":
            sys.exit(0)
            
        else:
            print("Invalid option.")

def main():
    if len(sys.argv) > 1:
        # Argument parsing could go here for non-interactive mode
        print("CLI arguments not yet implemented. Starting interactive mode.")
    
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
