import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# import undetected_chromedriver as uc
import os


def chrome_driver():
    driver_path = ChromeDriverManager().install()
    print("Driver path:", driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security
    # Check if it's actually executable
    if not os.access(driver_path, os.X_OK):
        print("❌ Not executable. Trying to locate the real binary.")
        for root, dirs, files in os.walk(os.path.dirname(driver_path)):
            for file in files:
                if "chromedriver" in file and not file.endswith(".chromedriver"):
                    potential_path = os.path.join(root, file)
                    print("✅ Found likely candidate:", potential_path)
                    driver_path = potential_path
                    break

    return webdriver.Chrome(service=ChromeService(driver_path), options=options)


driver = chrome_driver()

taxis_name = []
taxis_website = []
taxis_phone = []
taxis_email = []



url = "https://ukbusinessportal.co.uk/category/taxis/"

res = requests.get(url)

# print(res.status_code)

driver.get(url)

time.sleep(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')


taxis = soup.find_all('div',  class_='pl-4')

# print(taxi_info.text)

for taxi in taxis:
    try:
        name = taxi.find('h3').text.strip() if taxi.find('h3') else None
    except AttributeError:
        name = ''

    # get all <a> tags
    links = taxi.find_all('a')

    try: 
        website = links[1]['href'] if len(links) > 1 else None
    except AttributeError:
        website = ''

    try:
        phone = links[2].text.strip() if len(links) > 2 else None
    except AttributeError:
        phone = ''
    try: 
        email = links[3].text if len(links) > 3 else None
    except AttributeError:
        email = ''


    taxis_name.append(name)
    taxis_website.append(website)
    taxis_phone.append(phone)
    taxis_email.append(email)

driver.quit()

data = {
    'Taxis_Name': taxis_name,
    'Taxis_Website': taxis_website,
    'Taxis_Phone': taxis_phone,
    'Taxis_Email': taxis_email
}


df = pd.DataFrame(data)



print(df)
