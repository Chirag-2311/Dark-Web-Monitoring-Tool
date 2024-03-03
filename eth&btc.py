import requests
from bs4 import BeautifulSoup
import re

# Define a function to find cryptocurrency addresses and usernames
def find_crypto_addresses_and_usernames(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Regex for Bitcoin and Ethereum addresses
    btc_regex = re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b')
    eth_regex = re.compile(r'\b0x[a-fA-F0-9]{40}\b')

    # Find all strings that match the BTC and ETH regex patterns
    btc_addresses = soup.find_all(string=btc_regex)
    eth_addresses = soup.find_all(string=eth_regex)

    # Assuming the username is in a nearby element; adjust based on actual HTML structure
    # This example attempts to find a previous sibling or parent that matches the /d/username pattern
    user_paths = []
    for address in btc_addresses + eth_addresses:
        user_path = address.find_previous(string=re.compile(r'\/d\/[a-zA-Z0-9_]+'))
        if user_path:
            user_paths.append((user_path.strip(), address.strip()))
    return user_paths


# Function to construct URL with keywords for search
def construct_url_with_keywords():
    num_keywords = int(input("How many keywords do you want to use? "))
    keywords = []
    for i in range(num_keywords):
        keyword = input(f"Enter keyword {i + 1}: ")
        keywords.append(keyword)
    query = '%20'.join(keywords)
    url = f'http://g66ol3eb5ujdckzqqfmjsbpdjufmjd5nsgdipvxmsh7rckzlhywlzlqd.onion/search/?q={query}&fuzziness=auto'
    return url


# Proxy and cookies setup remains the same
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050',
}
cookies = {
    'dcap': 'LATEST COOKIE of dcap field',
    'dread': 'LATEST COOKIE of dread field'
}

# Call the function to construct URL with keywords
url = construct_url_with_keywords()

# Make a request to the URL
try:
    response = requests.get(url, proxies=proxies, cookies=cookies)
    if response.status_code == 200:
        crypto_addresses_and_usernames = find_crypto_addresses_and_usernames(response.text)
        for user_path, address in crypto_addresses_and_usernames:
            print(f"User path: {user_path} has address: {address}")
    else:
        print("Failed to retrieve the webpage content.")
except requests.exceptions.ConnectionError as e:
    print("Failed to connect. Make sure Tor is running and check your proxy settings.", e)
