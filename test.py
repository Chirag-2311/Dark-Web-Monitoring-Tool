import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
import time
import os
from main import classify
import sqlite3
import subprocess
import sys




def get_url(url):
    proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }
    try:
        response = requests.get(url, proxies=proxies)
        
        if response.status_code == 200:
            print("Successfully reached the onion site.")
            return response.content
        
        else:
            print("Failed to reach the onion site. Status code:", response.status_code)

    except requests.RequestException as e:
        print("Error reaching the onion site:", e)
        


def captcha_check(content):
    captcha_keywords = ["Captcha", "Verification", "Human", "Challenge","Security", "Authentication", "Verification code", "Access control","Turing test", "Puzzle", "Solving", "Image recognition","Character recognition", "Anti-bot", "Proof of humanity","Confirm identity", "Distorted text", "Click verification","Select all images", "Solve this puzzle", "Verify yourself","Are you human?", "Confirm you're not a robot", "Enter the code", "Complete the challenge", "Pass the test", "Identity confirmation", "Human interaction", "Challenge-response","Queue","Select "]
    
    soup = BeautifulSoup(content, 'html.parser')
    text_content = soup.get_text().lower()

    for keyword in captcha_keywords:
        if keyword.lower() in text_content:
            print("This Page Contains Captcha")
            return True
    
    return False
        

def sele_captcha(url):
    firefox_options = webdriver.FirefoxOptions()

    # Define the proxy settings for Tor
    firefox_options.set_preference("network.proxy.type", 1)
    firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
    firefox_options.set_preference("network.proxy.socks_port", 9050)
    firefox_options.set_preference('network.proxy.socks_remote_dns', True)
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    
    try:
        if driver.find_element("xpath", "//*[contains(text(), '{}')]".format("Queue")):
            init_0_cookies = driver.get_cookies()
            init_cookies = driver.get_cookies()
            
            while init_0_cookies == init_cookies:
                time.sleep(3)
                init_cookies = driver.get_cookies()
    except:
        pass        
    
    init_cookies = driver.get_cookies()
    
    captcha_solved = False
    
    while not(captcha_solved):
        current_cookies = driver.get_cookies()
        
        if current_cookies != init_cookies:
            cookies = driver.get_cookies()
            captcha_solved = True
            time.sleep(3)
            
        else:
            print("Captcha was not solved successfully.")
            time.sleep(2)
        
        cookies = driver.get_cookies()
        time.sleep(1)
    
    return cookies

def scrape_bs4(response):
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                if '.onion' in href:
                	with open("link.txt","a") as handle:
                		handle.write(str(href)+"\n")
            
            return "Links Collected"
        else:
            print("Failed to fetch the content from the URL")
            return []
    except Exception as e:
        print("An error occurred:", str(e))
        return []


def exif_images(url, response, save_dir="images"):
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img', src=True)
            image_links = [img['src'] for img in img_tags]
            
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            for img_link in image_links:
                img_link = f"{url}/{img_link}"
                img_name = img_link.split('/')[-1]
                img_path = os.path.join(save_dir, img_name)
                proxies = {
                    'http': 'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'
                }
                
                img_response = requests.get(img_link, proxies=proxies)
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                
                # Run exiftool command to extract exif data
                exiftool_command = ['exiftool', img_path]
                exif_process = subprocess.run(exiftool_command, capture_output=True, text=True)
                exif_output = exif_process.stdout
                
                # Store the exif data in the database
                cursor.execute('''INSERT INTO ImageDetails (ImageURL, EXIFResponse) VALUES (?, ?)''', (img_link, exif_output))
                conn.commit()
                
                print(f"Exif data extracted and stored for {img_name}")
        else:
            print("Failed to fetch the content from the URL")
    except Exception as e:
        print("An error occurred:", str(e))



def crawl(url):
    proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }

    

    response = get_url(url)
    if response != None:
        
        if captcha_check(response):
            cookies = sele_captcha(url)
            session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}
            response = requests.get(url, cookies=session_cookies, proxies=proxies)
        else:
            response = requests.get(url, proxies=proxies)
        headers = response.headers
        server_details = headers.get('Server', 'Server details not available')
        print("Server Details:", server_details)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        site_name = title_tag.text
    
    proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }
    
    session = requests.Session()
    session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
    response = session.get(url)
    if response.status_code == 200:
    	response_text = response.text
    	
    
    classification_result = classify(response_text)
    
    print("Classify result: ",classify(response_text))
    
    print(scrape_bs4(response))
    
    exif_response = exif_images(url,response)
    conn = sqlite3.connect('site_data.db')
    
    cursor = conn.cursor()
    
    try:
    	cursor.execute('''INSERT INTO SiteDetails (URL, SiteName, ServerName, ClassificationResult) 
        	          VALUES (?, ?, ?, ?)''', (url, site_name, server_details, str(classification_result)))
    
    	#cursor.execute("SELECT ID FROM SiteDetails WHERE URL = ?", (url,))
    
    	cursor.execute('''INSERT INTO ImageDetails (ImageURL, EXIFResponse) 
        	          VALUES (?, ?)''', (url, str(exif_response)))
    except:
    	pass
    conn.commit()
    conn.close()
    
    
# test.py


def process_url(url):
    print(f"Received URL: {url}")
    # Your code to process the URL goes here





if __name__ == "__main__":
    
    conn = sqlite3.connect('site_data.db')
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT URL FROM SiteDetails")
    urls = cursor.fetchall()
    url_list = [url[0] for url in urls]
    
    

    if sys.argv[1]:
        url = sys.argv[1]
        crawl(url)
        
        if url in url_list:
        	print("Already scanned")
        	cursor.execute("Select * from SiteDetails where URL == ?",(url))
        	print(cursor.fetchall())
        
    else:
        visited_urls = set()  # Initialize a set to store visited URLs
        
        with open("link.txt", "r") as handle:
            read = handle.readlines()
            count = 2
            for i in read:
                if i.strip() not in visited_urls:  # Check if the URL has not been visited before
                    crawl(i.strip())
                    visited_urls.add(i.strip())  # Add the URL to the set of visited URLs
                    count -= 1
                    if count == 0:
                        break
    
    
	
