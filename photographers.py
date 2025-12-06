# Importing Required Libraries
import requests # Fetch webpage HTML
import pandas as pd # Store scraped data into CSV files
import time
# Load dynamic pages that need JavaScript
from bs4 import BeautifulSoup # Parse HTML and extract elements
from selenium.webdriver.common.by import By
from selenium import webdriver
# Automatically download ChromeDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os


# Setting up a Chrome WebDriver
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


# Photography Category scraping

photographers_name = []
photographers_website = []
photographers_phone = []
photographers_email = []

url_photo = "https://ukbusinessportal.co.uk/category/photographers/"
res = requests.get(url_photo)
print(res.status_code)

driver.get(url_photo)
time.sleep(10)
soup = BeautifulSoup(driver.page_source, 'html.parser')
photographers = soup.find_all('div', class_='pl-4')

for photographer in photographers:
    try:
        name = photographer.find('h3').text.strip()
    except AttributeError:
        name = ''
    # get all <a> tags
    links = photographer.find_all('a')

    try: 
        website = links[1]['href']
    except AttributeError:
        website = ''

    try:
        phone = links[2].text.strip()
    except AttributeError:
        phone = ''
    try: 
        email = links[3].text
    except AttributeError:
        email = ''


    photographers_name.append(name)
    photographers_website.append(website)
    photographers_phone.append(phone)
    photographers_email.append(email)


driver.quit()

photographer_data = {
    'Photographers_Name': photographers_name,
    'Photographers_website': photographers_website,
    'Photographers_Phone': photographers_phone,
    'Photographers_email': photographers_email
}

df_photogropher = pd.DataFrame(photographer_data)

df_photogropher.to_csv('photographers.csv', index=False)