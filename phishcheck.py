import dnstwist
import json
import whois
import requests
import re
import sys
import concurrent.futures
from datetime import datetime

def sanitize_domain(url):
    """Removes 'http://', 'https://', 'www.' and paths from the URL to extract the domain."""
    return re.sub(r"https?://|www\.|/.*", "", url).strip()

def check_blacklist(domains):
    """Checks if domains are blacklisted using Google Safe Browsing API (batch request)."""
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    params = {
        "client": {"clientId": "phishcheck", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": f"http://{domain}"} for domain in domains]
        }
    }
    try:
        response = requests.post(api_url, json=params, params={"key": "YOUR_API_KEY"}, timeout=5)
        matches = response.json().get("matches", [])
        return {entry["threat"]["url"].replace("http://", ""): True for entry in matches}
    except requests.exceptions.RequestException:
        return {}

def check_ssl(domain):
    """Checks if a domain has SSL (HTTPS) enabled with optimized request."""
    try:
        response = requests.head(f"https://{domain}", timeout=3, allow_redirects=True, stream=True)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_whois_info(domain):
    """Fetch WHOIS data using the whois library."""
    try:
        w = whois.whois(domain)
        if isinstance(w.creation_date, list):
            creation_date = w.creation_date[0]  
        else:
            creation_date = w.creation_date
        return creation_date if isinstance(creation_date, datetime) else None
    except Exception:
        return None

def process_domain(domain):
    """Performs phishing domain checks in parallel."""
    is_https = check_ssl(domain)
    registration_date = get_whois_info(domain)
    reasons = []

    if not is_https:
        reasons.append("❌ No HTTPS (SSL)")
    if registration_date and (2024 - registration_date.year) < 1:
        reasons.append("⚠️ Recently registered")

    is_fake = bool(reasons)
    return {
        "domain": domain,
        "https": is_https,
        "registration_date": str(registration_date),
        "is_fake": is_fake,
        "reasons": reasons
    }

def scan_domain(target_domain):
    """Scans for phishing domains using optimized dnstwist and parallel execution."""
    output_file = f"{target_domain}_phishcheck.json"
    print(f"\n🚀 Scanning {target_domain} for possible phishing...\n")

    scan_results = dnstwist.run(domain=target_domain, registered=True, threads=100, whois=False)
    domains = [entry.get("domain") for entry in scan_results if entry.get("domain")]

    if not domains:
        print("✅ No phishing domains found.")
        return

    # Parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_domain, domains))

    # Check blacklisting in bulk
    blacklisted_domains = check_blacklist(domains)
    for result in results:
        domain = result["domain"]
        if blacklisted_domains.get(domain):
            result["is_fake"] = True
            result["reasons"].append("🚨 Blacklisted (Possible phishing)")

        print(f"\n🔍 {domain} - {'🛑 FAKE' if result['is_fake'] else '✅ Legit'}")
        for reason in result["reasons"]:
            print(f"   ➡ {reason}")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Scan Complete! Results saved to `{output_file}`\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n⚠️ ERROR: No domain provided!\n")
        print("   Usage: python phishcheck.py <domain or URL>\n")
        sys.exit(1)

    target_url = sys.argv[1]
    target_domain = sanitize_domain(target_url)
    scan_domain(target_domain)
