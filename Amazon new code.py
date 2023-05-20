from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
import time
import pandas as pd
import pymysql

options = Options()
options.headless = True

# Function to find the links of products from Amazon website
def find_links(given_product):
    # Initialize a Chrome web browser
    browser = webdriver.Chrome(options=options)
    # Open Amazon website
    browser.get('https://www.amazon.in')
    # Find the search bar and enter the given product name
    elem = browser.find_element(By.ID, 'twotabsearchtextbox')
    elem.send_keys(given_product)
    # Click the search button
    elem2 = browser.find_element(By.ID, 'nav-search-submit-button')
    elem2.click()

    links=[]
    # Loop through the first three pages of the search result
    for product in range(1):
        # Find the product links on the page
        products = list(set(browser.find_elements(By.CLASS_NAME, 'a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))
        for product in products:
            # Append the links to the list
            links.append(product.get_attribute('href'))
        # Click the next page button
        browser.find_element(By.CLASS_NAME, 's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator').click()
        # Wait for 15 seconds
        browser.implicitly_wait(15)
    # Close the browser
    browser.close()
    # Return the list of product links
    return links


# Function to extract details of the product from the product link
def details_of_product(link_of_product):
    # Initialize a dictionary to store the product details
    product_details = {}
    # Initialize a Chrome web browser
    browser = webdriver.Chrome()
    # Open the product link
    product = browser.get(link_of_product)
    # Extract the name of the product
    name = browser.find_element(By.XPATH,'//span[@id="productTitle"]')
    prdt_name = name.text
    # Add the name of the product to the dictionary
    product_details['Name'] = prdt_name
    
    # Try to extract the rating of the product
    try:
        rating = browser.find_element(By.XPATH,'//span[@class="a-size-base a-nowrap"]')
        pr_rating = float(rating.text.split()[0])
    # If the rating is not found, add N.A. to the dictionary
    except:
        pr_rating = 'N.A'
    
    # Try to extract the number of ratings of the product
    try:
        numrating = browser.find_element(By.XPATH,'//span[@id="acrCustomerReviewText"]')
        prdt_numrating = float(numrating.text.split()[0].replace(',',''))
    except:
        prdt_numrating = 'N.A'
    try:
        # Find the table with class "a-keyvalue prodDetTable"
        table = browser.find_elements(By.XPATH,'//table[@class="a-keyvalue prodDetTable"]')[1]
        # Find all the rows (tr elements) in the table
        rows = table.find_elements(By.TAG_NAME,'tr')
        # Iterate through each row
        for row in rows:
            # Retrieve the text of the header cell (th element)
            Add_info_name = row.find_element(By.TAG_NAME,'th').text
            # Retrieve the text of the value cell (td element)
            Add_info_value = row.find_element(By.TAG_NAME,'td').text
            # Add the header and value to the dictionary
            product_details[Add_info_name] = Add_info_value
    # If the table is not found, add N.A. to the dictionary
    except:
        product_details['Additional Information'] = 'N.A'
    
    # Close the browser
    browser.close()
    # Return the product details dictionary
    return product_details


# Function to scrape Amazon and save product details to a MySQL database
def scrape_amazon_save_mysql(product_name, num_products):
    # Find the links of the products
    product_links = find_links(product_name)[:num_products]
    
    # Initialize a list to store the product details
    product_details_list = []
    
    # Iterate through each product link
    for link in product_links:
        # Extract the details of the product
        product_details = details_of_product(link)
        # Append the product details to the list
        product_details_list.append(product_details)
    
    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(product_details_list)
    
    # Create a MySQL connection
    engine = create_engine('mysql+pymysql://username:password@localhost:port/database')
    
    # Save the DataFrame to MySQL
    df.to_sql('products', con=engine, if_exists='replace', index=False)


# Example usage:
product_name = 'laptop'
num_products = 10

scrape_amazon_save_mysql(product_name, num_products)

