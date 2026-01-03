import subprocess
import requests
import json
from ..utils import log_info, log_error, log_success, BOLD, RESET

def extract_metadata(file_path):
    """Uses ExifTool to extract metadata from a file."""
    log_info(f"Extracting metadata from: {file_path}")
    
    # We use the system 'exiftool'
    cmd = ["exiftool", file_path]
    
    try:
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        if process.returncode == 0:
            print(f"\n{BOLD}Metadata Report:{RESET}")
            print(process.stdout)
        else:
            log_error(f"ExifTool Error: {process.stderr}")
            
    except FileNotFoundError:
        log_error("ExifTool is not installed on the system.")
    except Exception as e:
        log_error(f"Error: {e}")

def geolocate_ip(ip_address):
    """Uses ip-api.com to locate an IP address."""
    log_info(f"Geolocating IP: {ip_address}")
    
    url = f"http://ip-api.com/json/{ip_address}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") == "success":
            print(f"\n{BOLD}Geolocation Results:{RESET}")
            print(f"  IP: {data.get('query')}")
            print(f"  Country: {data.get('country')} ({data.get('countryCode')})")
            print(f"  Region: {data.get('regionName')} ({data.get('region')})")
            print(f"  City: {data.get('city')}")
            print(f"  ISP: {data.get('isp')}")
            print(f"  Org: {data.get('org')}")
            print(f"  Coordinates: {data.get('lat')}, {data.get('lon')}")
            
            # Generate a Google Maps link
            print(f"  Map: https://www.google.com/maps/search/?api=1&query={data.get('lat')},{data.get('lon')}")
        else:
            log_error(f"API Error: {data.get('message')}")
            
    except Exception as e:
        log_error(f"Request failed: {e}")
