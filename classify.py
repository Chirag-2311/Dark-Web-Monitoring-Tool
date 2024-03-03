import requests
from main import classify

def get_html_content(url):
    try:
        session = requests.Session()
        session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
        response = session.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to retrieve HTML content from the URL:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred while fetching HTML content:", e)
        return None

if __name__ == "__main__":
    url = input("Enter the URL to classify: ")
    html_content = get_html_content(url)
    if html_content:
        result = classify(html_content)
        print("Classification result:", result)

