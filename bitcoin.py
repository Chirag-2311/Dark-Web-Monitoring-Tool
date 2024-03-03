import requests
from bs4 import BeautifulSoup
import re

def find_btc_and_usernames(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    btc_addresses = soup.find_all(string=re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'))
    user_paths = []

    for btc_address in btc_addresses:
        user_path = btc_address.find_previous(string=re.compile(r'\/d\/[a-zA-Z0-9_]+'))
        if user_path:
            user_paths.append((user_path.strip(), btc_address.strip()))

    return user_paths

def construct_url_with_keywords():
    url = 'http://g66ol3eb5ujdckzqqfmjsbpdjufmjd5nsgdipvxmsh7rckzlhywlzlqd.onion/search/?q=drugs'
    return url

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050',
}

cookies = {
    'dcap': 'LATEST COOKIE of dcap field',
    'dread': 'LATEST COOKIE of dread field'
}

url = construct_url_with_keywords()

try:
    response = requests.get(url, proxies=proxies, cookies=cookies)
    print(response.text)  # For debugging
    if response.status_code == 200:
        btc_and_usernames = find_btc_and_usernames(response.text)
        for user_path, btc_address in btc_and_usernames:
            print(f"User path: {user_path} has BTC address: {btc_address}")
    else:
        print("Failed to retrieve the webpage content.")
except requests.exceptions.ConnectionError as e:
    print("Failed to connect. Make sure Tor is running and check your proxy settings.", e)

