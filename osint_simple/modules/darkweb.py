import requests
import re
import socket
import time
from datetime import datetime
from urllib.parse import urljoin
from ..utils import log_info, log_error, log_warning, BOLD, RESET, CYAN, YELLOW

# Dark Web Engine URLs
AHMIA_ONION = "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/"
TORCH_ONION = "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/"
HAYSTAK_ONION = "http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/"
EXCAVATOR_ONION = "http://2v7ueqz3ljidvofv.onion/"
PHOBOS_ONION = "http://phobosx7pzicnc6g3b7cz67y467sh6atfksrcvxh3zxy6q6thv6vxad.onion/"
DDG_ONION = "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/"

def check_tor():
    """Checks if Tor is running on port 9050 (System) or 9150 (Browser). Returns port or None."""
    for port in [9050, 9150]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return port
    return None

def parse_time_ago_to_days(date_str):
    """Converts Ahmia date strings (relative or absolute) to number of days ago."""
    date_str = date_str.lower().strip()
    if not date_str or "unknown" in date_str: return 0
    
    try:
        if any(x in date_str for x in ["hour", "minute", "second", "just now"]):
            return 0 
        
        iso_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_str)
        if iso_match:
            d = datetime.strptime(iso_match.group(0), "%Y-%m-%d")
            return (datetime.now() - d).days

        num_match = re.search(r'(\d+)', date_str)
        val = int(num_match.group(1)) if num_match else 0
        
        if "yesterday" in date_str: return 1
        if "day" in date_str: return val
        if "week" in date_str: return val * 7
        if "month" in date_str: return val * 30
        if "year" in date_str: return val * 365
        return 0 
    except:
        return 0

def get_hidden_inputs(session, url, headers=None):
    """Helper: Fetches a page and extracts hidden input fields from forms.
       Needed for Ahmia's dynamic CSRF/bot protection.
    """
    try:
        r = session.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            # Basic regex to find hidden inputs: <input type="hidden" name="..." value="...">
            # This covers the random token like name="298425" value="874c85"
            hidden = re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]+)">', r.text)
            return dict(hidden)
    except:
        pass
    return {}

def search_ahmia(query, days=None):
    """Entry point for Dark Web search."""
    tor_port = check_tor()
    if tor_port:
        log_info(f"Tor detected on port {tor_port}. Verifying circuit...")
        proxies = {'http': f'socks5h://127.0.0.1:{tor_port}', 'https': f'socks5h://127.0.0.1:{tor_port}'}
        try:
            requests.get(DDG_ONION, timeout=20, proxies=proxies)
            log_info("Circuit verified. Searching Onion engines...")
        except:
            log_warning("Tor circuit seems unstable. This may take longer or fail.")

        if run_tor_search(query, days, tor_port):
            log_info("Tor search completed.")
            return
        log_warning("No results found via Tor engines. Trying Clearnet fallbacks...")
    else:
        log_warning("Tor service not detected. Using Clearnet fallbacks...")
    
    run_clearnet_search(query, days)

def run_tor_search(query, days=None, port=9050):
    """Internal: Execute search over Tor network using multiple engines."""
    proxies = {'http': f'socks5h://127.0.0.1:{port}', 'https': f'socks5h://127.0.0.1:{port}'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0'}
    
    # Define engines with their possible search paths and param names
    engines = [
        {
            "name": "Ahmia",
            "url": AHMIA_ONION,
            "paths": ["search/", "search?q=", ""],
            "param": "q",
            "needs_token": True # Flag to fetch hidden token first
        },
        {
            "name": "Torch",
            "url": TORCH_ONION,
            "paths": ["cgi-bin/omega/omega"], # Action URL
            "param": "P", # Changed from 'query' to 'P'
            "needs_token": True, # Needs 'tkn' and other hidden fields
            "token_url": TORCH_ONION # Where to fetch the token from (Root)
        }
    ]
    
    any_success = False
    for engine in engines:
        engine_success = False
        
        # Pre-fetch token if needed
        extra_params = {}
        session = requests.Session()
        session.proxies = proxies
        
        if engine.get("needs_token"):
            log_info(f"Fetching token for {engine['name']}...")
            # Default to engine URL if token_url not specified
            t_url = engine.get("token_url", engine["url"])
            token_params = get_hidden_inputs(session, t_url, headers=headers)
            if token_params:
                extra_params.update(token_params)
                log_info(f"Got tokens: {list(token_params.keys())}")
        
        for path in engine["paths"]:
            try:
                search_url = urljoin(engine["url"], path)
                log_info(f"Searching {engine['name']} ({path if path else 'root'})...")
                
                params = {engine["param"]: query}
                params.update(extra_params)
                
                response = session.get(search_url, params=params, headers=headers, timeout=60, allow_redirects=True)
                
                if response.status_code == 200:
                    if parse_and_print_results(response.text, engine["name"], filter_days=days):
                        any_success = True
                        engine_success = True
                        break # Found results for this engine, move to next engine
                else:
                    log_warning(f"{engine['name']} returned status {response.status_code}")
                    
            except Exception as e:
                err_str = str(e).lower()
                if "0x01" in err_str: log_error(f"{engine['name']} unreachable: SOCKS failure. (Tor circuit issue)")
                elif "0x05" in err_str: log_error(f"{engine['name']} unreachable: Connection refused.")
                else: log_error(f"{engine['name']} search failed: {str(e)[:60]}...")
            
            if engine_success: break
            time.sleep(1)
            
    return any_success

def run_clearnet_search(query, days=None):
    """Internal: Clearnet fallbacks with corrected formatted gateway URLs."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # Try Ahmia Clearnet first (With Token Logic)
    try:
        url_base = "https://ahmia.fi/"
        url_search = "https://ahmia.fi/search/"
        
        session = requests.Session()
        log_info("Fetching Ahmia (Clearnet) token...")
        token_params = get_hidden_inputs(session, url_base, headers=headers)
        
        params = {'q': query}
        params.update(token_params)
        
        response = session.get(url_search, params=params, headers=headers, timeout=15)
        if response.status_code == 200:
            if parse_and_print_results(response.text, "Ahmia (Clearnet)", filter_days=days):
                return True
    except Exception as e:
        # log_error(f"Ahmia Clearnet failed: {e}") 
        pass

    # Corrected Gateway URLs (Onion address prefix is required)
    AHMIA_V3 = "juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd"
    gateways = [
        ("Ahmia (Onion.moe)", f"https://{AHMIA_V3}.onion.moe/search/?q={query}"),
        ("Ahmia (Onion.pet)", f"https://{AHMIA_V3}.onion.pet/search/?q={query}"),
        ("Ahmia (Onion.dog)", f"https://{AHMIA_V3}.onion.dog/search/?q={query}"),
        ("Ahmia (Onion.ws)", f"https://{AHMIA_V3}.onion.ws/search/?q={query}")
    ]

    # Try Gateways
    for name, g_url in gateways:
        try:
            log_info(f"Trying {name}...")
            # Some gateways might pass the token transparently, but if they are simple proxies, they might fail too.
            # We try simple GET first.
            response = requests.get(g_url, headers=headers, timeout=25)
            if response.status_code == 200:
                if parse_and_print_results(response.text, name, filter_days=days):
                    return True
        except: pass

    # Attempt DuckDuckGo Dorking
    if run_ddg_dork(query): return True
    
    # Attempt Torry.io
    return run_torry_search(query)

def run_ddg_dork(query):
    log_info("Dorking DuckDuckGo...")
    # Permissive dork for cached onion links
    dork_query = f'"{query}" (site:onion.ly OR site:onion.moe OR site:onion.ws OR site:onion.dog OR site:onion.pet)'
    url = "https://html.duckduckgo.com/html/"
    try:
        response = requests.get(url, params={'q': dork_query}, timeout=15)
        if response.status_code == 200:
            links = re.findall(r'([a-z2-7]{16,56}\.onion)', response.text)
            links = list(set(links))
            if links:
                print(f"\n{BOLD}Found {len(links)} onion mentions via DuckDuckGo:{RESET}")
                for i, link in enumerate(links[:15]):
                    print(f"[{i+1}] http://{link}")
                return True
    except: pass
    return False

def run_torry_search(query):
    log_info("Trying Torry.io fallback...")
    url = "https://torry.io/search/"
    try:
        response = requests.get(url, params={'q': query}, timeout=15)
        if response.status_code == 200:
            links = re.findall(r'(http://[a-z2-7]{16,56}\.onion[^\s"\'>]*)', response.text)
            links = list(set(links))
            if links:
                print(f"\n{BOLD}Found {len(links)} links via Torry.io:{RESET}")
                for i, link in enumerate(links[:15]):
                    print(f"[{i+1}] {link}")
                return True
    except: pass
    print(f"\n{BOLD}No results found across all engines.{RESET}")
    return False

def parse_and_print_results(content, source, filter_days=None):
    max_days = int(filter_days) if filter_days else 9999
    IGNORE = ["juhanurmihxlp77", "xmh57jrkn", "haystak", "onion.moe", "torry.io", "ahmia.fi", "2v7ueqz3l", "duckduckgo", "onion.pet", "onion.ws", "onion.dog"]
    
    # 1. Try to find result blocks (Structured)
    result_blocks = []
    # Use lowercase for splitting to be robust
    content_lower = content.lower()
    if 'class="result"' in content_lower:
        parts = re.split(r'class="result"', content, flags=re.IGNORECASE)
        result_blocks = parts[1:]

    if result_blocks:
        valid_results = []
        for block in result_blocks:
            date_match = re.search(r'last_seen">(.*?)</span>', block, re.IGNORECASE)
            date_str = date_match.group(1).strip() if date_match else "Unknown"
            if max_days != 9999 and parse_time_ago_to_days(date_str) > max_days: continue
                
            link_match = re.search(r'href=[\'"](http://[a-z2-7]{16,56}\.onion.*?)[\'"]', block)
            title_search = re.search(r'>(.*?)</a>', block)
            
            if link_match:
                valid_results.append({
                    'link': link_match.group(1),
                    'title': title_search.group(1).strip() if title_search else "No Title",
                    'date': date_str
                })
        
        if valid_results:
            print(f"\n{BOLD}Search Results ({source}):{RESET}")
            for i, res in enumerate(valid_results[:15]):
                clean_title = re.sub('<[^<]+?>', '', res['title'])
                print(f"[{i+1}] {clean_title}")
                print(f"    Link: {res['link']}")
                print(f"    Seen: {res['date']}")
                print("-" * 30)
            return True

    # 2. Deep Scan fallback (Unstructured)
    links = re.findall(r'(http[s]?://[a-z2-7]{16,56}\.onion[^\s"\'><]*)', content)
    # Also look for raw onion links
    raw_onions = re.findall(r'([a-z2-7]{16,56}\.onion)', content)
    for ro in raw_onions:
        links.append("http://" + ro)
    unique_links = []
    seen = set()
    for l in links:
        l = l.rstrip('/')
        if not any(ig in l for ig in IGNORE) and l not in seen:
            unique_links.append(l)
            seen.add(l)
    
    if unique_links:
        print(f"\n{BOLD}Found {len(unique_links)} unique links via {source} (Deep Scan):{RESET}")
        for i, link in enumerate(unique_links[:20]):
            print(f"[{i+1}] {link}")
        return True
        
    return False
