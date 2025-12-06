This Python script scrapes business information (Taxi services, Plumbers, and Photographers) from the website UK Business Portal and saves the collected data into CSV files.

The script uses both Requests and Selenium WebDriver for scraping:
Requests checks the page response status
Selenium loads dynamically rendered HTML content
BeautifulSoup parses and extracts data
Pandas converts the extracted information into CSV files


# Scraping Categories 

This script scrapes data from three business categories:
| Category      | URL                        |
| ------------- | -------------------------- |
| Taxis         | `/category/taxis/`         |
| Plumbers      | `/category/plumbers/`      |
| Photographers | `/category/photographers/` |

For each category, the script extracts:

Business Name

Website URL

Phone Number

Email Address


# Exporting Data 

After scraping all three categories, data is:

Stored into dictionaries

Converted to Pandas DataFrames

Exported as CSV files into the project directory

# Output Files
taxis.csv
plumbers.csv
photographers.csv


# How To Run
pip install selenium webdriver-manager requests pandas beautifulsoup4

python script_name.py


