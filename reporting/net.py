import requests
from bs4 import BeautifulSoup


REPORT_URL = 'https://report.netcraft.com/report'
YOUR_EMAIL = 'your@email.com'  
MALICIOUS_URL = 'https://suspicious-site.com' 


with requests.Session() as session:
    
    response = session.get(REPORT_URL)  
    soup = BeautifulSoup(response.text, 'html.parser')

    
    form_data = {
        'email': YOUR_EMAIL,
        'url': MALICIOUS_URL
    }

   
    for hidden in soup.find_all('input', type='hidden'):
        if hidden['name']:
            form_data[hidden['name']] = hidden.get('value', '')

    
    response = session.post(
        REPORT_URL,
        data=form_data,
        headers={
            'Referer': REPORT_URL,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )

   
    if response.status_code == 200:
        print("Report submitted successfully!")
        print("Check your email for confirmation.")
    else:
        print(f"Submission failed. Status code: {response.status_code}")