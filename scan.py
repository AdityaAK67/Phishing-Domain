
import json
import os
import requests


API_KEY = "97e2b2f9cffed79ee508e5654dad4c83775573b35fc6ec6df1451dbdda66db15"
VT_URL = "https://www.virustotal.com/api/v3/urls"

def load_json_file(file_path):
    """Loads JSON data from a file, handling missing or empty files."""
    if not os.path.exists(file_path):
        print(f"⚠️ Error: File '{file_path}' not found.")
        return None  

    if os.path.getsize(file_path) == 0:
        print(f"⚠️ Error: File '{file_path}' is empty.")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"⚠️ Error: File '{file_path}' contains invalid JSON.")
        return None

def check_url_virustotal(url):
    """Checks a URL on VirusTotal and returns its detection status."""
    headers = {"x-apikey": API_KEY}
    data = {"url": url}

    response = requests.post(VT_URL, headers=headers, data=data)

    if response.status_code == 200:
        json_response = response.json()
        analysis_id = json_response["data"]["id"]

        
        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        response = requests.get(analysis_url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            stats = result["data"]["attributes"]["stats"]
            malicious_count = stats.get("malicious", 0)
            return malicious_count > 0  
        else:
            print(f"⚠️ Error fetching analysis results: {response.status_code}")
            return None

    elif response.status_code == 400:
        print(f"⚠️ Bad request. Check API key and URL format: {url}")
        return None
    elif response.status_code == 403:
        print("⚠️ Access forbidden. Your API key might be invalid or expired.")
        return None
    elif response.status_code == 429:
        print("⚠️ Rate limit exceeded. Try again later.")
        return None
    else:
        print(f"⚠️ Unexpected error ({response.status_code}) for URL: {url}")
        return None

def save_json_file(data, output_path):
    """Saves JSON data to an output file."""
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"✅ Output saved successfully to '{output_path}'")
    except Exception as e:
        print(f"⚠️ Error: Unable to save output file. {e}")

def main():
    """Main function to check URLs in a JSON file using VirusTotal."""
    input_file = input("Enter input JSON file path: ")
    output_file = input("Enter output JSON file path: ")

    data = load_json_file(input_file)

    if data is None:
        print("⚠️ Cannot proceed. Fix the JSON file and retry.")
        return

    checked_urls = []

    if isinstance(data, list):  # JSON is a list of URLs
        for url in data:
            is_blocked = check_url_virustotal(url)
            checked_urls.append({"url": url, "blocked": is_blocked})
    elif isinstance(data, dict):  # JSON is a dictionary with URLs inside
        for key, url in data.items():
            is_blocked = check_url_virustotal(url)
            checked_urls.append({"url": url, "blocked": is_blocked})
    else:
        print("⚠️ Unsupported JSON format. Expected a list or dictionary.")
        return

    save_json_file(checked_urls, output_file)

if __name__ == "__main__":
    main()
