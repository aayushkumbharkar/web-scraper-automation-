# Code for web scraper

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)
driver = webdriver.Chrome(options=options)

# Function to scrape Google Maps search results
def scrape_google_maps(search_query):
    url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    # Extract business details
    businesses = []
    listings = driver.find_elements("xpath", "//div[contains(@class, 'Nv2PK')]")
    
    for listing in listings[:10]:  # Scrape first 10 results
        try:
            name = listing.find_element("xpath", ".//h3").text
            rating = listing.find_element("xpath", ".//span[contains(@aria-label, 'stars')]").text
            address = listing.find_element("xpath", ".//span[contains(@class, 'UsdlK')]").text
            businesses.append({"name": name, "rating": rating, "address": address})
        except:
            continue

    return businesses

# Scrape data for a sample query
data = scrape_google_maps("coffee shops in New York")

# Save as JSON
with open("business_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("Scraping Completed! Data saved to business_data.json")

driver.quit()

# Code for Automation

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Upload JSON file
file = drive.CreateFile({'title': 'business_data.json'})
file.SetContentFile('business_data.json')
file.Upload()

print("File successfully uploaded to Google Drive!")
