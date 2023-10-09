import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
pd.options.mode.chained_assignment = None
def delay():
    """Function to add a random delay."""
    time.sleep(random.randint(3, 10))
def lazy_loading():
    """Function for lazy loading."""
    element = driver.find_element(By.TAG_NAME, 'body')
    count = 0
    while count < 20:
        element.send_keys(Keys.PAGE_DOWN)
        delay()
        count += 1
def extract_content(url):
    """Function to fetch page content."""
    base_url = 'https://silverstones.pk'
    if not url.startswith('http'):
        url = base_url + url
    print("Attempting to visit:", url)
    try:
        driver.get(url)
        page_content = driver.page_source
        product_soup = BeautifulSoup(page_content, 'html.parser')
        return product_soup
    except Exception as e:
        print(f"Error while visiting {url}: {e}")
        return None
def extract_product_details(soup):
    """Function to extract product details."""
    details = {
        'Name': 'N/A',
        'Regular price': 'N/A',
        'SKU': 'N/A',
        'Description': 'N/A',
        'Categories': 'N/A',
        'Images': 'N/A',
        'URL': 'N/A'
    }
    # Product Name
    product_name_element = soup.find('h1', {'class': 'product_title'})
    details['Name'] = product_name_element.text.strip() if product_name_element else 'N/A'
    # Product Price
    product_price_element = soup.find('span', {'class': 'woocommerce-Price-amount'})
    details['Regular price'] = product_price_element.text.strip() if product_price_element else 'N/A'
    # SKU
    sku_element = soup.find('span', {'class': 'sku'})
    details['SKU'] = sku_element.text.strip() if sku_element else 'N/A'
    tab_description_element = soup.find(id='tab-description')
    details['Long Description'] = tab_description_element.text.strip() if tab_description_element else 'N/A'
    # Categories
    category_element = soup.find('span', {'class': 'posted_in'})
    details['Categories'] = category_element.text.strip() if category_element else 'N/A'
    # Images
    product_image_element = soup.find('img', {'class': 'wp-post-image'})
    details['Images'] = product_image_element['src'] if product_image_element else 'N/A'
    return details
# List of Jewelry website links
urls = [
    'https://silverstones.pk'
]
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
all_product_details = []
for start_url in urls:
    driver.get(start_url)
    lazy_loading()
    content = driver.page_source
    homepage_soup = BeautifulSoup(content, 'html.parser')
    product_links = homepage_soup.find_all('a', {'class': 'woocommerce-LoopProduct-link'})
    for link in product_links:
        if not link:
            continue
        product_content = extract_content(link['href'])
        if product_content:
            product_details = extract_product_details(product_content)
            product_details['URL'] = link['href']
            all_product_details.append(product_details)
data = pd.DataFrame(all_product_details)
# Adding the ID column
data['ID'] = range(1, len(data) + 1)
# Reordering columns so ID comes first
cols = ['ID'] + [col for col in data if col != 'ID']
data = data[cols]
data.to_csv('woocommerce_data.csv', index=False)
print("Scraping complete!")
driver.close()
