# OSINT Simple

A unified Command Line Interface (CLI) wrapper for powerful Open Source Intelligence (OSINT) tools. Built with inspiration from Bellingcat's methodology, this tool simplifies person investigations and deep web searches.

## Features

### 👤 People Search
- **Maigret & Sherlock:** Search usernames across hundreds of platforms.
- **Holehe:** Check if an email is registered on 120+ social media sites.
- **GHunt:** Investigate Google accounts and Gmail addresses.
- **h8mail:** Search for email/username mentions in data breaches.
- **Telegram Checker:** Official Bellingcat tool to link phone numbers to Telegram accounts.

### 🌐 Deep Web & Geolocation
- **Dark Web Search:** Sequential search across Ahmia and Torch (.onion sites).
- **Clearnet Fallbacks:** Automatic failover to Clearnet mirrors if Tor is unavailable.
- **ExifTool:** Extract metadata from images and PDFs.
- **IP Geolocation:** Trace and map IP addresses.

### 📜 Archiving
- **Wayback Machine:** Search site history or save URLs for evidence preservation.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pngbtw/osint-simple.git
   cd osint-simple
   ```

2. **Run the start script:**
   The tool will automatically create a virtual environment and install all dependencies on the first run.
   ```bash
   ./start.py
   ```

3. **Install Tools:**
   Select **Option 99** in the menu to automatically install all required OSINT binaries (Maigret, Holehe, etc.).

## Usage

Simply run `./start.py` and follow the interactive menu.

**Note for Dark Web Search:** For the most reliable results, ensure the Tor service is running on your machine:
```bash
sudo apt install tor
sudo systemctl start tor
```

## Security & Privacy policy

This tool is designed with privacy in mind. It runs entirely on your local machine.

- **Credentials:** API keys (e.g., for Telegram) are stored locally in a `.env` file.
- **Session Data:** Authenticated session files (`*.session`) are kept locally to maintain logins.
- **Data Protection:** All configuration files, session data, and investigation results (reports, logs) are strictly excluded from version control via `.gitignore`. **No sensitive data is ever uploaded to this repository.**

## License
MIT License