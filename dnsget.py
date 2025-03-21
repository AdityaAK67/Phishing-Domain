import dnstwist
import json
import sys
import re

try:
    import dns.resolver  
except ImportError:
    print("\n⚠️ WARNING: dnspython library is missing! Install it using: pip install dnspython\n")
    sys.exit(1)

def sanitize_domain(url):
    """Extracts and cleans the domain name from a full URL."""
    return re.sub(r"https?://|www\.|/.*", "", url).strip()  

def scan_domain(domain):
    """Scan domain permutations using dnstwist and save results."""
    domain = sanitize_domain(domain)  
    output_file = f"{domain}_dnsget.json"

    print(f"\n🚀 Scanning {domain} for registered permutations...\n")

   
    scan_results = dnstwist.run(
        domain=domain,
        registered=True,  
        threads=100,  
        whois=False,  
        mx=False,  
        ssdeep=False  
    )

    found_domains = []
    print("\n🔍 Live Results:\n")

    for entry in scan_results:
        if entry.get("dns_a") or entry.get("dns_ns"):  
            found_domains.append(entry)
            print(f"✅ Found: {entry['domain']}")

    
    with open(output_file, "w") as f:
        json.dump(found_domains, f, indent=4)

    print(f"\n✅ Scan Complete! Results saved to `{output_file}`\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n⚠️ ERROR: No domain provided!\n")
        print("   Usage: python dnsget.py <domain or URL>\n")
        sys.exit(1)

    target_domain = sys.argv[1]
    scan_domain(target_domain)
