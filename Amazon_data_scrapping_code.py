from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd



# Function to find the links of products from Amazon website
def find_links(given_product):
    # Initialize a Chrome web browser
    browser = webdriver.Chrome()
    # Open Amazon website
    browser.get('https://www.amazon.in')
    # Find the search bar and enter the given product name
    elem = browser.find_element(By.ID, 'twotabsearchtextbox')
    elem.send_keys(given_product)
    # Click the search button
    elem2 = browser.find_element(By.ID, 'nav-search-submit-button')
    elem2.click()

    #n_p = int(browser.find_elements(By.CLASS_NAME, 's-pagination-item.s-pagination-disabled')[1].text)
    links=[]
    # Loop through the first three pages of the search result
    for product in range(2):
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
    name = browser.find_element(By.XPATH,'//span[@class="a-size-large product-title-word-break"]')
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
        prdt_numerating = 'N.A'
    
    #product_details['No.of ratings'] = prdt_numrating
    
    try:
        price = browser.find_element(By.XPATH,'//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]')
        new_price = float(price.text.strip('₹').replace(',',''))
    except:
        new_price='N.A'
    product_details['Price'] = new_price

    try:
        # Find the table with class "a-keyvalue prodDetTable"
        table = browser.find_elements(By.XPATH,'//table[@class="a-keyvalue prodDetTable"]')[1]
        # Find all the rows (tr elements) in the table
        rows = table.find_elements(By.TAG_NAME,'tr')
        # Iterate through each row
        for row in rows:
            # Retrieve the text of the header cell (th element)
            Add_info_name = row.find_element(By.TAG_NAME,'th').text
            # Retrieve the text of the data cell (td element)
            Add_info_value = row.find_element(By.TAG_NAME,'td').text
            # Store the information as key-value pairs in the dictionary
            product_details[Add_info_name] = Add_info_value
    # If the table is not found, catch the exception and continue
    except:
        pass
    
    time.sleep(2)
    browser.close()
    return product_details

import streamlit as st

# Create a function to display the data table
def show_data():
    # Prompt the user to enter the name of the product
    name_of_product = st.text_input('Enter the name of the product:')
    if not name_of_product:
        return
    # Find the links for the product using the find_links function
    links_of_product = find_links(name_of_product)
    if not links_of_product:
        st.write(f"No products found for '{name_of_product}'")
        return
    # Scrape the details of the product using the details_of_product function
    list_of_details = []
    for link in links_of_product:
        details = details_of_product(link)
        prdt_df = pd.DataFrame(details, index=[0])
        list_of_details.append(prdt_df)

    prdt_table = pd.concat(list_of_details, ignore_index=True)
    prdt_table = prdt_table.reset_index(drop=True)
    prdt_table.fillna('N.A',inplace=True)
    #prdt_table.drop(['Manufacturer','Packer','Importer'], axis=1)
    prdt_table['Best Sellers Rank'] = prdt_table['Best Sellers Rank'].str.replace('#','').replace('\n',' ')
    #prdt_table['Customer Reviews'].replace('N.A', 0, inplace=True)
    # Display the data table
    st.write(prdt_table)
    return prdt_table

# Set page title
st.set_page_config(page_title='Analysis of Top ranked products in Amazon')

# Set page header
st.title('Amazon Product Scraper')

# Show the data table
pic=show_data()
print(pic)

import matplotlib.pyplot as plt
import seaborn as sns

# Define functions for visualizations

def show_top_rated_products(pic):
    top_rated = pic.sort_values('Customer Reviews', ascending=False).head(5)
    fig, ax = plt.subplots()
    sns.barplot(x='Name', y='Rating', data=top_rated, ax=ax)
    ax.set_ylabel('Rating')
    ax.set_xlabel('Product Name')
    ax.set_title('Top 5 Rated Products')
    st.pyplot(fig)
def show_num_of_ratings_products(pic):
    #top_rated = pic.sort_values('Customer Reviews', ascending=False).head(5)
    fig, ax = plt.subplots()
    sns.barplot(x='ASIN', y='No.of ratings', data=pic, ax=ax)
    ax.set_ylabel('Rating')
    ax.set_xlabel('Product Name')
    ax.set_title('Number of Ratings v/s ASIN')
    st.pyplot(fig)
def histogram(pic):
   # plot histogram using Seaborn
    sns.histplot(data=pic, x='No.of ratings', bins=25, edgecolor="darkblue")
    plt.xlabel('Number of ratings')
    plt.ylabel('Count')
    st.pyplot()
    
# Add visualizations
st.subheader('Visualizations')
show_top_rated_products(pic)
show_num_of_ratings_products(pic)
histogram(pic)
