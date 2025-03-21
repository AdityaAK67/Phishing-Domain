# # import dnstwist
# # import json
# # import requests
# # import whois
# # import difflib
# # import sys
# # from bs4 import BeautifulSoup

# # # Function to get page content
# # def get_page_html(url):
# #     try:
# #         response = requests.get(url, timeout=5)
# #         if response.status_code == 200:
# #             return response.text
# #     except requests.RequestException:
# #         return None
# #     return None

# # # Function to extract form data from a page
# # def extract_form_data(html):
# #     try:
# #         soup = BeautifulSoup(html, "html.parser")
# #         forms = soup.find_all("form")
# #         form_data = []
# #         for form in forms:
# #             inputs = {inp.get("name", "unnamed"): inp.get("type", "text") for inp in form.find_all("input")}
# #             form_data.append(inputs)
# #         return form_data
# #     except Exception:
# #         return None

# # # Function to check similarity between login pages
# # def compare_login_pages(real_html, fake_html):
# #     if not real_html or not fake_html:
# #         return 0  # No page means no match

# #     real_soup = BeautifulSoup(real_html, "html.parser")
# #     fake_soup = BeautifulSoup(fake_html, "html.parser")

# #     real_text = real_soup.get_text()
# #     fake_text = fake_soup.get_text()

# #     # Compare text similarity
# #     similarity = difflib.SequenceMatcher(None, real_text, fake_text).ratio()
# #     return similarity

# # def main():
# #     # Ensure the script is executed with a domain argument
# #     if len(sys.argv) != 2:
# #         print("⚠️ ERROR: Please provide a domain as an argument!")
# #         print("Usage: python advphi.py <domain>")
# #         return

# #     domain = sys.argv[1]
# #     output_file = f"{domain}_advphi.json"

# #     # Get the real login page HTML
# #     real_login_url = f"https://{domain}/login"
# #     real_login_html = get_page_html(real_login_url)

# #     print(f"\n🚀 Scanning {domain} for phishing domains...\n")
# #     scan_results = dnstwist.run(domain=domain, registered=True, threads=50, whois=False)

# #     found_domains = []
# #     for entry in scan_results:
# #         domain_name = entry.get("domain")
# #         if not domain_name:
# #             continue

# #         # Check if login page exists
# #         fake_login_url = f"https://{domain_name}/login"
# #         fake_login_html = get_page_html(fake_login_url)

# #         similarity_score = compare_login_pages(real_login_html, fake_login_html) if fake_login_html else 0

# #         # WHOIS info
# #         try:
# #             w = whois.whois(domain_name)
# #             reg_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
# #         except Exception:
# #             reg_date = None

# #         # Fake detection logic
# #         reasons = []
# #         is_fake = False

# #         if similarity_score > 0.7:  # 70%+ similarity = likely phishing
# #             reasons.append(f"🚨 Login page looks {int(similarity_score * 100)}% similar to original")
# #             is_fake = True

# #         if reg_date and (2024 - reg_date.year) < 1:
# #             reasons.append("⚠️ Recently registered domain")
# #             is_fake = True

# #         # Save results
# #         result = {
# #             "domain": domain_name,
# #             "login_page_similarity": f"{int(similarity_score * 100)}%",
# #             "registration_date": str(reg_date),
# #             "is_fake": is_fake,
# #             "reasons": reasons
# #         }
# #         found_domains.append(result)

# #         # Display results
# #         print(f"\n🔍 {domain_name} - {'🛑 FAKE' if is_fake else '✅ Legit'}")
# #         for reason in reasons:
# #             print(f"   ➡ {reason}")

# #     # Save final results
# #     with open(output_file, "w") as f:
# #         json.dump(found_domains, f, indent=4)

# #     print(f"\n✅ Scan Complete! Results saved to `{output_file}`\n")

# # if __name__ == "__main__":
# #     main()




# import dnstwist
# import json
# import requests
# import whois
# import difflib
# import sys
# import time
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse

# # Function to get page HTML
# def get_page_html(url):
#     try:
#         response = requests.get(url, timeout=5)
#         if response.status_code == 200:
#             return response.text
#     except requests.RequestException:
#         return None
#     return None

# # Function to extract internal links from a website
# def extract_internal_links(html, base_url):
#     soup = BeautifulSoup(html, "html.parser")
#     links = set()
#     for a_tag in soup.find_all("a", href=True):
#         href = a_tag["href"]
#         full_url = urljoin(base_url, href)
#         if urlparse(full_url).netloc == urlparse(base_url).netloc:  # Ensure it's internal
#             links.add(full_url)
#     return list(links)

# # Function to extract text from HTML
# def extract_text(html):
#     if not html:
#         return ""
#     soup = BeautifulSoup(html, "html.parser")
#     return soup.get_text(separator=" ").strip()

# # Function to compare website content
# def compare_websites(real_pages, fake_pages):
#     if not real_pages or not fake_pages:
#         return 0  # No data to compare

#     total_similarity = 0
#     comparisons = 0

#     for real_url, real_html in real_pages.items():
#         real_text = extract_text(real_html)

#         for fake_url, fake_html in fake_pages.items():
#             fake_text = extract_text(fake_html)
#             similarity = difflib.SequenceMatcher(None, real_text, fake_text).ratio()
#             total_similarity += similarity
#             comparisons += 1

#     return total_similarity / comparisons if comparisons > 0 else 0

# def main():
#     if len(sys.argv) != 2:
#         print("⚠️ ERROR: Please provide a domain as an argument!")
#         print("Usage: python advphi.py <domain>")
#         return

#     domain = sys.argv[1]
#     output_file = f"{domain}_advphi.json"
#     base_url = f"https://{domain}"

#     # Step 1: Fetch homepage and extract internal links
#     print(f"\n🚀 Crawling {domain} for internal pages...\n")
#     main_page_html = get_page_html(base_url)
#     if not main_page_html:
#         print("❌ ERROR: Unable to fetch the main page.")
#         return

#     internal_links = extract_internal_links(main_page_html, base_url)
#     internal_links = [base_url] + internal_links[:5]  # Limit to 5 extra pages to avoid excessive requests
#     print(f"🔍 Found {len(internal_links)} internal pages to scan.")

#     # Step 2: Fetch content from all internal pages
#     real_pages = {}
#     for link in internal_links:
#         real_pages[link] = get_page_html(link)
#         time.sleep(1)  # Avoid rapid requests

#     # Step 3: Scan for phishing domains
#     print(f"\n🚀 Scanning {domain} for phishing domains...\n")
#     scan_results = dnstwist.run(domain=domain, registered=True, threads=50, whois=False)

#     found_domains = []
#     for entry in scan_results:
#         domain_name = entry.get("domain")
#         if not domain_name:
#             continue

#         fake_base_url = f"https://{domain_name}"
#         fake_main_page_html = get_page_html(fake_base_url)
#         if not fake_main_page_html:
#             continue

#         # Step 4: Fetch phishing website internal pages
#         fake_links = extract_internal_links(fake_main_page_html, fake_base_url)
#         fake_links = [fake_base_url] + fake_links[:5]  # Limit to 5 pages
#         fake_pages = {}
#         for link in fake_links:
#             fake_pages[link] = get_page_html(link)
#             time.sleep(1)

#         # Step 5: Compare entire website structure
#         similarity_score = compare_websites(real_pages, fake_pages)

#         # WHOIS info
#         try:
#             w = whois.whois(domain_name)
#             reg_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
#         except Exception:
#             reg_date = None

#         # Step 6: Fake detection logic
#         reasons = []
#         is_fake = False

#         if similarity_score > 0.7:  # 70%+ similarity = likely phishing
#             reasons.append(f"🚨 Website content looks {int(similarity_score * 100)}% similar to original.")
#             is_fake = True

#         if reg_date and (2024 - reg_date.year) < 1:
#             reasons.append("⚠️ Recently registered domain - potential phishing attempt.")
#             is_fake = True

#         # Save results
#         result = {
#             "domain": domain_name,
#             "website_similarity": f"{int(similarity_score * 100)}%",
#             "registration_date": str(reg_date),
#             "is_fake": is_fake,
#             "reasons": reasons
#         }
#         found_domains.append(result)

#         # Display results
#         print(f"\n🔍 {domain_name} - {'🛑 FAKE' if is_fake else '✅ Legit'}")
#         for reason in reasons:
#             print(f"   ➡ {reason}")

#     # Save final results
#     with open(output_file, "w") as f:
#         json.dump(found_domains, f, indent=4)

#     print(f"\n✅ Scan Complete! Results saved to `{output_file}`\n")

# if __name__ == "__main__":
#     main()




import dnstwist
import json
import requests
import whois
import difflib
import sys
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to get page HTML
def get_page_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = 'utf-8'  
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(f"❌ ERROR: Unable to fetch {url} - {e}")
    return None


def extract_internal_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.add(full_url)
    return list(links)


def extract_text(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ").strip()

# Function to compare website content
def compare_websites(real_pages, fake_pages):
    if not real_pages or not fake_pages:
        return 0

    total_similarity = 0
    comparisons = 0

    for real_url, real_html in real_pages.items():
        real_text = extract_text(real_html)
        for fake_url, fake_html in fake_pages.items():
            fake_text = extract_text(fake_html)
            similarity = difflib.SequenceMatcher(None, real_text, fake_text).ratio()
            total_similarity += similarity
            comparisons += 1

    return total_similarity / comparisons if comparisons > 0 else 0

def scan_domain(domain):
    output_file = f"{domain}_advphi.json"
    base_url = f"https://{domain}"

    print(f"\n🚀 Crawling {domain} for internal pages...\n")
    main_page_html = get_page_html(base_url)
    if not main_page_html:
        print("❌ ERROR: Unable to fetch the main page.")
        return

    internal_links = extract_internal_links(main_page_html, base_url)
    internal_links = [base_url] + internal_links[:5]
    print(f"🔍 Found {len(internal_links)} internal pages to scan.")

    real_pages = {link: get_page_html(link) for link in internal_links}
    time.sleep(1)

    print(f"\n🚀 Scanning {domain} for phishing domains...\n")
    scan_results = dnstwist.run(domain=domain, registered=True, threads=100, whois=False)

    found_domains = []
    for entry in scan_results:
        domain_name = entry.get("domain")
        if not domain_name:
            continue

        fake_base_url = f"https://{domain_name}"
        fake_main_page_html = get_page_html(fake_base_url)
        if not fake_main_page_html:
            continue

        fake_links = extract_internal_links(fake_main_page_html, fake_base_url)
        fake_links = [fake_base_url] + fake_links[:5]
        fake_pages = {link: get_page_html(link) for link in fake_links}
        time.sleep(1)

        similarity_score = compare_websites(real_pages, fake_pages)

        try:
            w = whois.whois(domain_name)
            reg_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        except Exception:
            reg_date = None

        reasons = []
        is_fake = False

        if similarity_score > 0.7:
            reasons.append(f"🚨 Website content is {int(similarity_score * 100)}% similar to original.")
            is_fake = True

        if reg_date and (2024 - reg_date.year) < 1:
            reasons.append("⚠️ Recently registered domain - potential phishing attempt.")
            is_fake = True

        result = {
            "domain": domain_name,
            "website_similarity": f"{int(similarity_score * 100)}%",
            "registration_date": str(reg_date),
            "is_fake": is_fake,
            "reasons": reasons
        }
        found_domains.append(result)

        print(f"\n🔍 {domain_name} - {'🛑 FAKE' if is_fake else '✅ Legit'}")
        for reason in reasons:
            print(f"   ➡ {reason}")

    with open(output_file, "w") as f:
        json.dump(found_domains, f, indent=4)

    print(f"\n✅ Scan Complete! Results saved to `{output_file}`\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("⚠️ ERROR: Please provide a domain as an argument!")
        print("Usage: python advphi.py <domain>")
        sys.exit(1)

    target_domain = sys.argv[1]
    scan_domain(target_domain)
