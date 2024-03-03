import requests
import re
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}
url = 'http://3d4xyfihl6ox2rmyfnskmqfubpdl5nlhau22s6qlsd37wbjsfiknfsid.onion/'
def find_bitcoin_addresses(html_content):
    btc_pattern = re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b')
    btc_addresses = set(btc_pattern.findall(html_content))
    return btc_addresses
try:
    response = requests.get(url, proxies=proxies)
    if response.status_code == 200:
        page_text = response.text
        bitcoin_addresses = find_bitcoin_addresses(page_text)
        if bitcoin_addresses:
            print("Found Bitcoin addresses:")
            for address in bitcoin_addresses:
                print(address)
        else:
            print("No Bitcoin addresses found.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
