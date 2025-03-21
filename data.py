import requests
import json


API_KEY = "69eb44a393ab49842eef21724d5d2946f8661047d436281dd4c6bf2d4ddd5e7c"

def get_virustotal_report(url):
    api_url = "https://www.virustotal.com/api/v3/urls"
    headers = {
        "x-apikey": API_KEY
    }
    
    
    data = {"url": url}
    response = requests.post(api_url, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        url_id = result["data"]["id"]
        
        
        report_url = f"https://www.virustotal.com/api/v3/analyses/{url_id}"
        report_response = requests.get(report_url, headers=headers)
        
        if report_response.status_code == 200:
            return report_response.json()
        else:
            return {"error": "Failed to fetch report", "status_code": report_response.status_code}
    else:
        return {"error": "Failed to submit URL", "status_code": response.status_code}

if __name__ == "__main__":
    url_to_check = "sanjivanicoe.org.in"  
    report = get_virustotal_report(url_to_check)
    print(json.dumps(report, indent=4))