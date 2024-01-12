import requests
from bs4 import BeautifulSoup
import json

# URL of the target website
url = "https://portal.permit.pcta.org/availability/mexican-border.php"

# Send an HTTP request to the website and get the HTML content
try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    with requests.Session() as session:
        response = session.get(url, headers=headers)
    # response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response code: {response.status_code}")
except requests.exceptions.RequestException as req_err:
    print(f"Request error occurred: {req_err}")
except Exception as err:
    print(f"An unexpected error occurred: {err}")
# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the per day limit
per_day_limit_element = soup.find('p', style=lambda style: 'color: red' in style)
per_day_limit = int(per_day_limit_element.get_text().split(':')[-1].strip())

# Extract data from the JavaScript variable 'data'
data_script = soup.find('script', string=lambda s: 'var data =' in s).string
data_start = data_script.find('{"limit"')
data_end = data_script.rfind('};') + 1
calendar_data = json.loads(data_script[data_start:data_end])

# Highlight dates with a limit of 50 or less
for entry in calendar_data['calendar']:
    start_date = entry['start_date']
    num_applications = int(entry['num'])
    
    # Check if the number of applications is 50 or less
    if num_applications <= per_day_limit:
        print(f"Date: {start_date}, Applications: {num_applications} (Highlighted)")
    else:
        print(f"Date: {start_date}, Applications: {num_applications}")
