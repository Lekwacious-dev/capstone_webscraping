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


# Plumbers Category scraping

plumbers_name = []
plumbers_website = []
plumbers_phone = []
plumbers_email = []

url_plumbers = "https://ukbusinessportal.co.uk/category/plumbers/"

res = requests.get(url_plumbers)

print(res.status_code)

driver.get(url_plumbers)
time.sleep(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')

plumbers = soup.find_all('div',  class_='pl-4')

for plumber in plumbers:
    try:
        name = plumber.find('h3').text.strip() if plumber.find('h3') else None
    except AttributeError:
        name = ''

    # get all <a> tags
    links = plumber.find_all('a')

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


    plumbers_name.append(name)
    plumbers_website.append(website)
    plumbers_phone.append(phone)
    plumbers_email.append(email)


driver.quit()

plumber_data = {
    'Plumbers_Name': plumbers_name,
    'Plumbers_website': plumbers_website,
    'Plumbers_Phone': plumbers_phone,
    'Plumbers_email': plumbers_email
}

df_plumber = pd.DataFrame(plumber_data)



df_plumber.to_csv('plumbers.csv', index=False)