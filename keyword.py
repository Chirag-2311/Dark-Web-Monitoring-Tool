import requests
from bs4 import BeautifulSoup
import re


def construct_url_with_keywords():
    num_keywords = int(input("How many keywords do you want to use? "))
    keywords = []
    for i in range(num_keywords):
        keyword = input(f"Enter keyword {i + 1}: ").strip()
        keywords.append(keyword.lower())
    query = '%20'.join(keywords)
    url = f'http://g66ol3eb5ujdckzqqfmjsbpdjufmjd5nsgdipvxmsh7rckzlhywlzlqd.onion/search/?q={query}&fuzziness=auto'
    return url, keywords


proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050',
}

cookies = {
    'dcap': 'VadvNUD7e+BB8ZQfumQMl2+MUCtA6E8zEEDcE0sFGbXWdU7Kd/sDhbep8mV/fVF2M50kcetpCHiSRgYY+b+hLAw5mInSr5x2TAT+nW2qWM4IajhuO5LZbnBitFkg+h46kZOwIuWJstw3N93kFRe5ZBjX5oA3SmGvM6UbEuwc91nubQE=',
    'dread': '9pg21nr7bage5scc7b7fvvvqu3'
}

url, keywords = construct_url_with_keywords()

try:
    response = requests.get(url, proxies=proxies, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming each post is within an 'article' or 'div' and the username is within an 'a' tag
    posts = soup.find_all(['article', 'div'])
    for post in posts:
        username_link = post.find('a', href=re.compile(r'^/d/.*'))
        if username_link and any(keyword in post.text.lower() for keyword in keywords):
            username = username_link.get_text()
            post_text = post.get_text(strip=True)
            print(f"Username: {username}\nPost: {post_text}\n")

except requests.exceptions.ConnectionError as e:
    print("Failed to connect. Make sure Tor is running and check your proxy settings.", e)
