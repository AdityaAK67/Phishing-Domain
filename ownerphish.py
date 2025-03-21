# import dnstwist
# import json
# import whois
# import sys

# def get_whois_info(domain):
#     """Retrieves WHOIS information for a domain."""
#     try:
#         w = whois.whois(domain)
#         return {
#             "registrant": w.name,
#             "organization": w.org,
#             "email": w.email,
#             "registrar": w.registrar,
#             "creation_date": str(w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date)
#         }
#     except Exception as e:
#         return {"error": str(e)}

# def compare_whois(real_info, fake_info):
#     """Compares WHOIS registrant details to detect phishing risks."""
#     if "error" in fake_info:
#         return False, ["WHOIS data not found"]

#     reasons = []
#     is_fake = False

#     if real_info["organization"] and fake_info["organization"]:
#         if real_info["organization"].lower() != fake_info["organization"].lower():
#             reasons.append(f"🚨 Organization mismatch: {fake_info['organization']} (Fake) vs {real_info['organization']} (Real)")
#             is_fake = True

#     if real_info["registrar"] and fake_info["registrar"]:
#         if real_info["registrar"].lower() != fake_info["registrar"].lower():
#             reasons.append(f"⚠️ Registrar mismatch: {fake_info['registrar']} (Fake) vs {real_info['registrar']} (Real)")

#     if real_info["email"] and fake_info["email"]:
#         if real_info["email"].lower() != fake_info["email"].lower():
#             reasons.append(f"🔍 Email mismatch: {fake_info['email']} (Fake) vs {real_info['email']} (Real)")
#             is_fake = True

#     return is_fake, reasons

# def main():
#     """Main function to check ownership of potentially phishing domains."""
#     if len(sys.argv) != 2:
#         print("⚠️ ERROR: Please provide a domain as an argument!")
#         print("Usage: python ownerphish.py <domain>")
#         return

#     domain = sys.argv[1]
#     output_file = f"{domain}_ownerphish.json"

#     print(f"\n🔍 Checking domain ownership for phishing risks: {domain}...\n")

#     # Get real domain WHOIS info
#     real_whois = get_whois_info(domain)

#     # Scan for similar phishing domains using dnstwist
#     scan_results = dnstwist.run(domain=domain, registered=True, threads=50, whois=False)

#     found_domains = []
#     for entry in scan_results:
#         fake_domain = entry.get("domain")
#         if not fake_domain:
#             continue

#         
#         fake_whois = get_whois_info(fake_domain)

#         
#         is_fake, reasons = compare_whois(real_whois, fake_whois)

#         result = {
#             "domain": fake_domain,
#             "is_fake": is_fake,
#             "registrant": fake_whois.get("registrant"),
#             "organization": fake_whois.get("organization"),
#             "email": fake_whois.get("email"),
#             "registrar": fake_whois.get("registrar"),
#             "creation_date": fake_whois.get("creation_date"),
#             "reasons": reasons
#         }
#         found_domains.append(result)

#         
#         print(f"\n🔍 {fake_domain} - {'🛑 FAKE' if is_fake else '✅ Legit'}")
#         for reason in reasons:
#             print(f"   ➡ {reason}")

#    
#     with open(output_file, "w") as f:
#         json.dump(found_domains, f, indent=4)

#     print(f"\n✅ Phishing Ownership Check Complete! Results saved to `{output_file}`\n")

# if __name__ == "__main__":
#     main()

import requests
import re
import json
import dnstwist
import sys

def get_whois_info(domain):
    """Fetch WHOIS data from www.whois.com/whois/ by web scraping."""
    try:
        url = f"https://www.whois.com/whois/{domain}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            return {"error": "WHOIS lookup failed: Invalid response"}

        
        registrant = re.search(r"Registrant Name:\s*(.*?)\n", response.text)
        organization = re.search(r"Registrant Organization:\s*(.*?)\n", response.text)
        email = re.search(r"Registrant Email:\s*(.*?)\n", response.text)
        registrar = re.search(r"Registrar:\s*(.*?)\n", response.text)
        creation_date = re.search(r"Creation Date:\s*(.*?)\n", response.text)

        return {
            "registrant": registrant.group(1).strip() if registrant else "N/A",
            "organization": organization.group(1).strip() if organization else "N/A",
            "email": email.group(1).strip() if email else "N/A",
            "registrar": registrar.group(1).strip() if registrar else "N/A",
            "creation_date": creation_date.group(1).strip() if creation_date else "N/A"
        }

    except Exception as e:
        return {"error": f"WHOIS lookup error: {str(e)}"}

def compare_whois(real_info, fake_info):
    """Compares WHOIS registrant details to detect phishing risks."""
    if "error" in fake_info:
        return False, ["WHOIS data not found"]

    reasons = []
    is_fake = False

    if real_info["organization"] and fake_info["organization"]:
        if real_info["organization"].lower() != fake_info["organization"].lower():
            reasons.append(f"🚨 Organization mismatch: {fake_info['organization']} (Fake) vs {real_info['organization']} (Real)")
            is_fake = True

    if real_info["registrar"] and fake_info["registrar"]:
        if real_info["registrar"].lower() != fake_info["registrar"].lower():
            reasons.append(f"⚠️ Registrar mismatch: {fake_info['registrar']} (Fake) vs {real_info['registrar']} (Real)")

    if real_info["email"] and fake_info["email"]:
        if real_info["email"].lower() != fake_info["email"].lower():
            reasons.append(f"🔍 Email mismatch: {fake_info['email']} (Fake) vs {real_info['email']} (Real)")
            is_fake = True

    return is_fake, reasons

def main():
    """Main function to check ownership of potentially phishing domains."""
    if len(sys.argv) != 2:
        print("⚠️ ERROR: Please provide a domain as an argument!")
        print("Usage: python ownerphish.py <domain>")
        return

    domain = sys.argv[1]
    output_file = f"{domain}_ownerphish.json"

    print(f"\n🔍 Checking domain ownership for phishing risks: {domain}...\n")

    
    real_whois = get_whois_info(domain)

    
    scan_results = dnstwist.run(domain=domain, registered=True, threads=50, whois=False)

    found_domains = []
    for entry in scan_results:
        fake_domain = entry.get("domain")
        if not fake_domain:
            continue

        
        fake_whois = get_whois_info(fake_domain)

        
        is_fake, reasons = compare_whois(real_whois, fake_whois)

        result = {
            "domain": fake_domain,
            "is_fake": is_fake,
            "registrant": fake_whois.get("registrant"),
            "organization": fake_whois.get("organization"),
            "email": fake_whois.get("email"),
            "registrar": fake_whois.get("registrar"),
            "creation_date": fake_whois.get("creation_date"),
            "reasons": reasons
        }
        found_domains.append(result)

        
        print(f"\n🔍 {fake_domain} - {'🛑 FAKE' if is_fake else '✅ Legit'}")
        for reason in reasons:
            print(f"   ➡ {reason}")

    
    with open(output_file, "w") as f:
        json.dump(found_domains, f, indent=4)

    print(f"\n✅ Phishing Ownership Check Complete! Results saved to `{output_file}`\n")

if __name__ == "__main__":
    main()
