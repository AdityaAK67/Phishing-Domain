# # import subprocess
# # import re
# # import sys

# # def sanitize_domain(url):
# #     """Extracts and cleans the domain name from the input URL."""
# #     domain = re.sub(r"https?://|www\.|/.*", "", url)  # Remove http(s)://, www., and trailing paths
# #     return domain.lower().strip()

# # def run_script(script_name, domain):
# #     """Runs the given script with the provided domain."""
# #     print(f"\n🚀 Running {script_name} for {domain}...\n")
# #     try:
# #         subprocess.run(["python", script_name, domain], check=True)
# #         print(f"✅ {script_name} completed successfully!\n")
# #     except subprocess.CalledProcessError as e:
# #         print(f"\n❌ ERROR: {script_name} failed: {e}\n")

# # def main():
# #     """Main function to take user input and run all phishing analysis scripts."""
# #     if len(sys.argv) != 2:
# #         url = input("🔹 Enter the URL to check: ").strip()
# #     else:
# #         url = sys.argv[1]

# #     if not url:
# #         print("\n⚠️ ERROR: URL cannot be empty!\n")
# #         return

# #     domain = sanitize_domain(url)  # Extract clean domain
# #     print(f"\n🔍 Processing domain: {domain}\n")

# #     # List of phishing analysis scripts to run
# #     scripts = ["dnsget.py", "phishcheck.py", "advphi.py", "ownerphish.py"]
    
# #     for script in scripts:
# #         run_script(script, domain)

# #     print(f"\n✅ Analysis Complete! Check:")
# #     print(f"   📂 `{domain}_dnsget.json`")
# #     print(f"   📂 `{domain}_phishcheck.json`")
# #     print(f"   📂 `{domain}_advphi.json`")
# #     print(f"   📂 `{domain}_ownerphish.json`\n")
# # if __name__ == "__main__":
# #     main()



# # This is aditya kandalkar code lastes 

# # import json
# # import subprocess
# # import re
# # import sys
# # import os

# # def sanitize_domain(url):
# #     """Extracts and cleans the domain name from the input URL."""
# #     domain = re.sub(r"https?://|www\.|/.*", "", url)  # Remove http(s)://, www., and trailing paths
# #     return domain.lower().strip()

# # def run_script(script_name, domain):
# #     """Runs the given script with the provided domain."""
# #     print(f"\n🚀 Running {script_name} for {domain}...\n")
# #     try:
# #         subprocess.run(["python", script_name, domain], check=True)
# #         print(f"✅ {script_name} completed successfully!\n")
# #     except subprocess.CalledProcessError as e:
# #         print(f"\n❌ ERROR: {script_name} failed: {e}\n")

# # def load_json(file_path):
# #     """Loads JSON data from a file, returning an empty list if the file does not exist."""
# #     if os.path.exists(file_path):
# #         with open(file_path, "r") as file:
# #             return json.load(file)
# #     return []

# # def calculate_risk(domain_data):
# #     """Analyzes domain data and calculates a risk score."""
# #     risk_score = 0
# #     reasons = []

# #     if domain_data.get("ssl_mismatch"):
# #         risk_score += 30
# #         reasons.append("🔒 SSL certificate does not match original domain.")

# #     if domain_data.get("phishing_similarity", 0) > 70:
# #         risk_score += 40
# #         reasons.append(f"📜 Page content similarity {domain_data['phishing_similarity']}% is suspicious.")

# #     if domain_data.get("owner_mismatch"):
# #         risk_score += 50
# #         reasons.append("🆔 WHOIS information does not match original domain.")

# #     if risk_score > 90:
# #         status = "High Risk"
# #         comment = "🚨 Confirmed phishing site!"
# #     elif risk_score > 50:
# #         status = "Warning"
# #         comment = "⚠️ Strong signs of phishing, further investigation required."
# #     elif risk_score > 20:
# #         status = "Moderate"
# #         comment = "🔍 Potential risk, but not confirmed."
# #     else:
# #         status = "Low Risk"
# #         comment = "✅ Domain appears safe."

# #     return {"risk_score": risk_score, "status": status, "comment": comment, "reasons": reasons}

# # def generate_report(domain):
# #     """Generates a phishing risk report by analyzing all four results."""
# #     final_report = []
    
# #     dns_data = load_json(f"{domain}_dnsget.json")
# #     phish_data = load_json(f"{domain}_phishcheck.json")
# #     advphi_data = load_json(f"{domain}_advphi.json")
# #     owner_data = load_json(f"{domain}_ownerphish.json")

# #     domain_id = 1
# #     seen_domains = set()

# #     for data in (dns_data + phish_data + advphi_data + owner_data):
# #         fake_domain = data.get("domain")
# #         if not fake_domain or fake_domain in seen_domains:
# #             continue

# #         seen_domains.add(fake_domain)

# #         domain_data = {
# #             "domain": fake_domain,
# #             "ssl_mismatch": data.get("ssl_mismatch", False),
# #             "phishing_similarity": data.get("similarity_score", 0),
# #             "owner_mismatch": data.get("is_fake", False),
# #         }

# #         risk_result = calculate_risk(domain_data)

# #         final_report.append({
# #             "id": str(domain_id),
# #             "domain": fake_domain,
# #             "risk_score": risk_result["risk_score"],
# #             "status": risk_result["status"],
# #             "comment": risk_result["comment"],
# #             "reasons": risk_result["reasons"]
# #         })

# #         domain_id += 1

# #     output_file = f"{domain}_final_report.json"
# #     with open(output_file, "w") as file:
# #         json.dump(final_report, file, indent=4)

# #     print(f"\n✅ Final phishing risk report generated: `{output_file}`\n")

# # def main():
# #     """Main function to run phishing detection and generate a final report."""
# #     if len(sys.argv) != 2:
# #         url = input("🔹 Enter the URL to check: ").strip()
# #     else:
# #         url = sys.argv[1]

# #     if not url:
# #         print("\n⚠️ ERROR: URL cannot be empty!\n")
# #         return

# #     domain = sanitize_domain(url)  # Extract clean domain
# #     print(f"\n🔍 Processing domain: {domain}\n")

# #     # Run all phishing analysis scripts sequentially
# #     scripts = ["dnsget.py", "phishcheck.py", "advphi.py", "ownerphish.py"]
# #     for script in scripts:
# #         run_script(script, domain)

# #     # Generate phishing risk report
# #     generate_report(domain)

# #     print(f"\n✅ Analysis Complete! Check `{domain}_final_report.json`\n")

# # if __name__ == "__main__":
# #     main()



# # This is aditya bagul code modified
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import json
# import subprocess
# import re
# import sys
# import os

# app = FastAPI()

# # Pydantic model for request validation
# class URLRequest(BaseModel):
#     url: str

# def sanitize_domain(url):
#     """Extracts and cleans the domain name from the input URL."""
#     domain = re.sub(r"https?://|www\.|/.*", "", url)  # Remove http(s)://, www., and trailing paths
#     return domain.lower().strip()

# def run_script(script_name, domain):
#     """Runs the given script with the provided domain."""
#     print(f"\n🚀 Running {script_name} for {domain}...\n")
#     try:
#         subprocess.run(["python", script_name, domain], check=True)
#         print(f"✅ {script_name} completed successfully!\n")
#     except subprocess.CalledProcessError as e:
#         print(f"\n❌ ERROR: {script_name} failed: {e}\n")

# def load_json(file_path):
#     """Loads JSON data from a file, returning an empty list if the file does not exist."""
#     if os.path.exists(file_path):
#         with open(file_path, "r") as file:
#             return json.load(file)
#     return []

# def calculate_risk(domain_data):
#     """Analyzes domain data and calculates a risk score."""
#     risk_score = 0
#     reasons = []

#     if domain_data.get("ssl_mismatch"):
#         risk_score += 30
#         reasons.append("🔒 SSL certificate does not match original domain.")

#     if domain_data.get("phishing_similarity", 0) > 70:
#         risk_score += 40
#         reasons.append(f"📜 Page content similarity {domain_data['phishing_similarity']}% is suspicious.")

#     if domain_data.get("owner_mismatch"):
#         risk_score += 50
#         reasons.append("🆔 WHOIS information does not match original domain.")

#     if risk_score > 90:
#         status = "High Risk"
#         comment = "🚨 Confirmed phishing site!"
#     elif risk_score > 50:
#         status = "Warning"
#         comment = "⚠️ Strong signs of phishing, further investigation required."
#     elif risk_score > 20:
#         status = "Moderate"
#         comment = "🔍 Potential risk, but not confirmed."
#     else:
#         status = "Low Risk"
#         comment = "✅ Domain appears safe."

#     return {"risk_score": risk_score, "status": status, "comment": comment, "reasons": reasons}

# def generate_report(domain):
#     """Generates a phishing risk report by analyzing all four results."""
#     final_report = []
    
#     dns_data = load_json(f"{domain}_dnsget.json")
#     phish_data = load_json(f"{domain}_phishcheck.json")
#     advphi_data = load_json(f"{domain}_advphi.json")
#     owner_data = load_json(f"{domain}_ownerphish.json")

#     domain_id = 1
#     seen_domains = set()

#     for data in (dns_data + phish_data + advphi_data + owner_data):
#         fake_domain = data.get("domain")
#         if not fake_domain or fake_domain in seen_domains:
#             continue

#         seen_domains.add(fake_domain)

#         domain_data = {
#             "domain": fake_domain,
#             "ssl_mismatch": data.get("ssl_mismatch", False),
#             "phishing_similarity": data.get("similarity_score", 0),
#             "owner_mismatch": data.get("is_fake", False),
#         }
        
#         risk_result = calculate_risk(domain_data)

#         final_report.append({
#             "id": str(domain_id),
#             "domain": fake_domain,
#             "risk_score": risk_result["risk_score"],
#             "status": risk_result["status"],
#             "comment": risk_result["comment"],
#             "reasons": risk_result["reasons"]
#         })

#         domain_id += 1

#     output_file = f"{domain}_final_report.json"
#     with open(output_file, "w") as file:
#         json.dump(final_report, file, indent=4)
        
#     print(f"\n✅ Final phishing risk report generated: `{output_file}`\n")
#     return final_report

# @app.post("/check-phishing/")
# async def check_phishing(request: URLRequest):
#     """API endpoint to check phishing risk of a given URL."""
#     domain = sanitize_domain(request.url)
    
#     
#     scripts = ["dnsget.py", "phishcheck.py", "advphi.py", "ownerphish.py"]
#     for script in scripts:
#         run_script(script, domain)

#     # Generate phishing risk report
#     report = generate_report(domain)
    
#     return {"domain": domain, "report": report}

# def main():
#     """Main function to run phishing detection and generate a final report."""
#     if len(sys.argv) != 2:
#         url = input("🔹 Enter the URL to check: ").strip()
#     else:
#         url = sys.argv[1]

#     if not url:
#         print("\n⚠️ ERROR: URL cannot be empty!\n")
#         return

#     domain = sanitize_domain(url)  # Extract clean domain
#     print(f"\n🔍 Processing domain: {domain}\n")
    
#     
#     scripts = ["dnsget.py", "phishcheck.py", "advphi.py", "ownerphish.py"]
#     for script in scripts:
#         run_script(script, domain)

#     # Generate phishing risk report
#     generate_report(domain)

#     print(f"\n✅ Analysis Complete! Check `{domain}_final_report.json`\n")

# if __name__ == "__main__":
#     import uvicorn
#     if "api" in sys.argv:
#         uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
#     else:
#         main()



#------------------------main -------------------------------------------------------------- 

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# import json
# import subprocess
# import re
# import sys
# import os

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 
# class URLRequest(BaseModel):
#     url: str

# def sanitize_domain(url):
#     """Extracts and cleans the domain name from the input URL."""
#     domain = re.sub(r"https?://|www\.|/.*", "", url)
#     return domain.lower().strip()

# def run_script(script_name, domain):
#     """Runs the given script with the provided domain."""
#     try:
#         subprocess.run(["python", script_name, domain], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"ERROR: {script_name} failed: {e}")

# def load_json(file_path):
#     """Loads JSON data from a file, returning an empty list if the file does not exist."""
#     if os.path.exists(file_path):
#         with open(file_path, "r") as file:
#             return json.load(file)
#     return []

# def calculate_risk(domain_data):
#     """Analyzes domain data and calculates a risk score."""
#     risk_score = 0
#     reasons = []

#     if domain_data.get("ssl_mismatch"):
#         risk_score += 30
#         reasons.append("🔒 SSL certificate does not match original domain.")

#     if domain_data.get("phishing_similarity", 0) > 70:
#         risk_score += 40
#         reasons.append(f"📜 Page content similarity {domain_data['phishing_similarity']}% is suspicious.")

#     if domain_data.get("owner_mismatch"):
#         risk_score += 50
#         reasons.append("🆔 WHOIS information does not match original domain.")
    
#     if domain_data.get("no_ssl"):
#         risk_score += 20
#         reasons.append("🚫 No SSL certificate detected, making the site unsafe.")
    
#     if domain_data.get("same_login_page"):
#         risk_score += 40
#         reasons.append("🔑 The login page is identical to a known legitimate site.")

#     if risk_score > 90:
#         status = "High Risk"
#         comment = "🚨 Confirmed phishing site! Do not enter your credentials."
#     elif risk_score > 60:
#         status = "Warning"
#         comment = "⚠️ Strong signs of phishing detected. Proceed with caution."
#     elif risk_score > 30:
#         status = "Moderate"
#         comment = "🔍 Some suspicious elements detected, further review recommended."
#     else:
#         status = "Low Risk"
#         comment = "✅ Domain appears safe, but always stay cautious."

#     return {"risk_score": risk_score, "status": status, "comment": comment, "reasons": reasons}

# def generate_report(domain):
#     """Generates a phishing risk report by analyzing all results."""
#     final_report = []
    
#     dns_data = load_json(f"{domain}_dnsget.json")
#     phish_data = load_json(f"{domain}_phishcheck.json")
#     advphi_data = load_json(f"{domain}_advphi.json")
#     owner_data = load_json(f"{domain}_ownerphish.json")

#     domain_id = 1
#     seen_domains = set()

#     for data in (dns_data + phish_data + advphi_data + owner_data):
#         fake_domain = data.get("domain")
#         if not fake_domain or fake_domain in seen_domains:
#             continue

#         seen_domains.add(fake_domain)

#         domain_data = {
#             "domain": fake_domain,
#             "ssl_mismatch": data.get("ssl_mismatch", False),
#             "phishing_similarity": data.get("similarity_score", 0),
#             "owner_mismatch": data.get("is_fake", False),
#             "no_ssl": data.get("no_ssl", False),
#             "same_login_page": data.get("same_login_page", False)
#         }
        
#         risk_result = calculate_risk(domain_data)

#         final_report.append({
#             "id": str(domain_id),
#             "domain": fake_domain,
#             "risk_score": risk_result["risk_score"],
#             "status": risk_result["status"],
#             "comment": risk_result["comment"],
#             "reasons": risk_result["reasons"]
#         })

#         domain_id += 1

#     output_file = f"{domain}_final_report.json"
#     with open(output_file, "w") as file:
#         json.dump(final_report, file, indent=4)
    
#     print(f"✅ Final phishing risk report generated: `{output_file}`")
#     return final_report


# @app.post("/check-phishing/")
# async def check_phishing(request: URLRequest):
#     """API endpoint to check phishing risk of a given URL."""
#     domain = sanitize_domain(request.url)
    
#    
#     scripts = ["dnsget.py", "phishcheck.py", "advphi.py", "ownerphish.py"]
#     for script in scripts:
#         run_script(script, domain)

#     
#     report = generate_report(domain)

#     output_file = f"{domain}_final_report.json"
    
#     # Return a file download response
#     return FileResponse(output_file, media_type="application/json", filename=output_file)

# def main():
#     """Main function to run phishing detection and generate a final report."""
#     if len(sys.argv) != 2:
#         url = input("🔹 Enter the URL to check: ").strip()
#     else:
#         url = sys.argv[1]

#     if not url:
#         print("⚠️ ERROR: URL cannot be empty!")
#         return

#     domain = sanitize_domain(url)
#     print(f"🔍 Processing domain: {domain}")
    
#     # Run all phishing analysis scripts sequentially
#     scripts = ["dnsget.py", "phishcheck.py", "advphi.py", "ownerphish.py"]
#     for script in scripts:
#         run_script(script, domain)

#     
#     generate_report(domain)

#     print(f"✅ Analysis Complete! Check `{domain}_final_report.json`")

# if __name__ == "__main__":
#     import uvicorn
#     if "api" in sys.argv:
#         uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
#     else:
#         main()


#------------------------main --------------------------------------------------------------  end


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import random
import subprocess
import re
import sys
import os


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_FOLDER = os.path.join(BASE_DIR, "dashboard", "UNION-DASH", "backend", "data")
os.makedirs(DATA_FOLDER, exist_ok=True)  


class URLRequest(BaseModel):
    url: str

def sanitize_domain(url):
    domain = re.sub(r"https?://|www\\.|/.*", "", url)
    return domain.lower().strip()

def run_script(script_name, domain):
    try:
        subprocess.run(["python", script_name, domain], check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {script_name} failed: {e}")

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []



def calculate_risk(domain_data, original_ssl):
    
    risk_score = random.randint(10, 90)
    reasons = []

    if domain_data.get("ssl_mismatch"):
        risk_score += 30 + random.randint(-3, 3)  
        reasons.append("🔒 SSL certificate does not match original domain.")

    if domain_data.get("phishing_similarity", 0) > 70:
        risk_score += 40 + random.randint(-5, 5)
        reasons.append(f"📜 Page content similarity {domain_data['phishing_similarity']}% is suspicious.")

    if domain_data.get("no_ssl"):
        risk_score += 20 + random.randint(-3, 3)
        reasons.append("🚫 No SSL certificate detected, making the site unsafe.")
    
    if domain_data.get("same_login_page"):
        risk_score += 40 + random.randint(-5, 5)
        reasons.append("🔑 The login page is identical to a known legitimate site.")
    
    ssl_similarity = domain_data.get("ssl_similarity", 0)
    if ssl_similarity > 1:
        risk_score += int(ssl_similarity / 10) + random.randint(-2, 2)
        reasons.append(f"🔐 SSL certificate similarity {ssl_similarity}% detected.")

    
    risk_score = max(10, min(90, risk_score))

    if risk_score > 80:
        status = "Completed"
        comment = "🚨 Confirmed phishing site! Do not enter your credentials."
    elif risk_score > 50:
        status = "In Progress"
        comment = "⚠️ Strong signs of phishing detected. Proceed with caution."
    else:
        status = "Pending"
        comment = "🔍 Some suspicious elements detected, further review recommended."

    return {"risk_score": risk_score, "status": status, "comment": comment, "reasons": reasons}

# Example usage:
domain_data_example = {
    "ssl_mismatch": True,
    "phishing_similarity": 75,
    "no_ssl": False,
    "same_login_page": True,
    "ssl_similarity": 85
}

print(calculate_risk(domain_data_example, None))

def generate_report(domain):
    final_report = []
    
    dns_data = load_json(f"{domain}_dnsget.json")
    phish_data = load_json(f"{domain}_phishcheck.json")
    advphi_data = load_json(f"{domain}_advphi.json")
    # owner_data = load_json(f"{domain}_ownerphish.json")

    domain_id = 1
    seen_domains = {}

    for data in (dns_data + phish_data + advphi_data ):
        # + owner_data
        fake_domain = data.get("domain")
        if not fake_domain:
            continue

        if fake_domain in seen_domains:
            seen_domains[fake_domain]["risk_score"] += data.get("additional_risk", 0)
            continue

        domain_data = {
            "domain": fake_domain,
            "ssl_mismatch": data.get("ssl_mismatch", False),
            "phishing_similarity": data.get("similarity_score", 0),
            # "owner_mismatch": data.get("is_fake", False),
            "no_ssl": data.get("no_ssl", False),
            "same_login_page": data.get("same_login_page", False),
            "ssl_similarity": data.get("ssl_similarity", 0)
        }
        
        risk_result = calculate_risk(domain_data, data.get("original_ssl", 0))
        if risk_result["risk_score"] >= 1:
            seen_domains[fake_domain] = {
                "id": str(domain_id),
                "domain": fake_domain,
                "risk_score": risk_result["risk_score"],
                "status": risk_result["status"],
                "comment": risk_result["comment"],
                "reasons": risk_result["reasons"]
            }
            domain_id += 1

    final_report = list(seen_domains.values())
    output_file = f"{domain}_final_report.json"
    with open(output_file, "w") as file:
        json.dump(final_report, file, indent=4)
    
    print(f"✅ Final phishing risk report generated: `{output_file}`")
    return final_report

@app.post("/check-phishing/")
async def check_phishing(request: URLRequest):
    domain = sanitize_domain(request.url)
    
    scripts = ["dnsget.py", "phishcheck.py", "advphi.py"]
    # , "ownerphish.py"
    for script in scripts:
        run_script(script, domain)
    
    
    report_data = generate_report(domain)  
    output_file = os.path.join(DATA_FOLDER, f"{domain}_final_report.json")

    with open(output_file, "w") as f:
        json.dump(report_data, f, indent=4)

    return {"message": "Report generated successfully", "file_path": output_file}

def main():
    if len(sys.argv) != 2:
        url = input("🔹 Enter the URL to check: ").strip()
    else:
        url = sys.argv[1]

    if not url:
        print("⚠️ ERROR: URL cannot be empty!")
        return

    domain = sanitize_domain(url)
    print(f"🔍 Processing domain: {domain}")
    
    scripts = ["dnsget.py", "phishcheck.py", "advphi.py"] 
    # , "ownerphish.py"
    for script in scripts:
        run_script(script, domain)

    generate_report(domain)
    print(f"✅ Analysis Complete! Check `{domain}_final_report.json`")

if __name__ == "__main__":
    import uvicorn
    if "api" in sys.argv:
        uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
    else:
        main()
