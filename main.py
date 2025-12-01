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


# Taxi Category scraping

url = "https://ukbusinessportal.co.uk/category/taxis/"

res = requests.get(url)

print(res.status_code)

driver.get(url)

time.sleep(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')

taxis = soup.find_all('div',  class_='pl-4')


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





# Plumbers Category scraping

plumbers_name = []
plumbers_website = []
plumbers_phone = []
plumbers_email = []

url_plumbers = "https://ukbusinessportal.co.uk/category/plumbers/"

res = requests.get(url_plumbers)

# print(res.status_code)

driver.get(url_plumbers)


soup = BeautifulSoup(driver.page_source, 'html.parser')

plumbers = soup.find_all('div',  class_='pl-4')

for plumber in plumbers:
    try:
        name = plumber.find('h3').text.strip() if taxi.find('h3') else None
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




# Photography Category scraping

photographers_name = []
photographers_website = []
photographers_phone = []
photographers_email = []

url_photo = "https://ukbusinessportal.co.uk/category/photographers/"
res = requests.get(url_photo)
driver.get(url_photo)
soup = BeautifulSoup(driver.page_source, 'html.parser')
photographers = soup.find_all('div', class_='pl-4')

for photographer in photographers:
    try:
        name = photographer.find('h3').text.strip() if taxi.find('h3') else None
    except AttributeError:
        name = ''
    # get all <a> tags
    links = photographer.find_all('a')

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


    photographers_name.append(name)
    photographers_website.append(website)
    photographers_phone.append(phone)
    photographers_email.append(email)


driver.quit()

taxi_data = {
    'Taxis_Name': taxis_name,
    'Taxis_Website': taxis_website,
    'Taxis_Phone': taxis_phone,
    'Taxis_Email': taxis_email
}

plumber_data = {
    'Plumbers_Name': plumbers_name,
    'Plumbers_website': plumbers_website,
    'Plumbers_Phone': plumbers_phone,
    'Plumbers_email': plumbers_email
}


photographer_data = {
    'Photographers_Name': photographers_name,
    'Photographers_website': photographers_website,
    'Photographers_Phone': photographers_phone,
    'Photographers_email': photographers_email
}


# Adding to dataframe


df_taxis = pd.DataFrame(taxi_data)
df_plumber = pd.DataFrame(plumber_data)
df_photogropher = pd.DataFrame(photographer_data)


#Convert to csv file

df_taxis.to_csv('taxis.csv', index=False)
df_plumber.to_csv('plumbers.csv', index=False)
df_photogropher.to_csv('photographers.csv', index=False)

