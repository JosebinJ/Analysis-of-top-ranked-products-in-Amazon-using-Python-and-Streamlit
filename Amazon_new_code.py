from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
options = Options()
options.headless = True

import streamlit as st


# Function to find the links of products from Amazon website
def find_links(given_product):
    # Initialize a Chrome web browser
    browser = webdriver.Chrome(options=options)
    # Open Amazon website
    browser.get('https://www.amazon.in')
    # Find the search bar and enter the given product name
    elem = browser.find_element(By.ID, 'twotabsearchtextbox')
    elem.send_keys(given_product)
    # Click the search buttontry:
    elem2 = browser.find_element(By.ID, 'nav-search-submit-button')
    elem2.click()

    #n_p = int(browser.find_elements(By.CLASS_NAME, 's-pagination-item.s-pagination-disabled')[1].text)
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
    browser = webdriver.Chrome(options=options)
    # Open the product link
    product = browser.get(link_of_product)
    # Extract the name of the product
    try:
        name = browser.find_element(By.XPATH,'//span[@id="productTitle"]')
        prdt_name = name.text
    except:
        name = browser.find_element(By.XPATH,'//span[@class="a-size-medium product-title-word-break product-title-resize"]')
        prdt_name = name.text
    # Add the name of the product to the dictionary
    product_details['Name'] = prdt_name
    
    # Try to extract the rating of the product
    try:
        rating = browser.find_element(By.XPATH,'//span[@class="a-size-base a-nowrap"]')
        pr_rating = float(rating.text.split()[0])
    # If the rating is not found, add N.A. to the dictionary
    except:
        pr_rating = 0.0
    product_details['Rating Out of 5'] = pr_rating
    
    # Try to extract the number of ratings of the product
    try:
        numrating = browser.find_element(By.XPATH,'//span[@id="acrCustomerReviewText"]')
        prdt_numrating = float(numrating.text.split()[0].replace(',',''))
    except:
        prdt_numrating = 0.0
    product_details['No.of ratings'] = prdt_numrating
    
    try:
        price = browser.find_element(By.XPATH,'//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]')
        new_price = float(price.text.strip('₹').replace(',',''))
    except:
        new_price = 0.0
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


# Take the name of the product as input from the user
name_of_product = input('State the product:')

# Find the links of the product using the find_links function
links_of_product = find_links(name_of_product)

# Initialize an empty list to store the details of all products
list_of_details = []

# Loop through each link to get details of the product
def getdetails(links_of_product):
    for link in links_of_product:
        # Get the details of the product using the details_of_product function
        details = details_of_product(link)
        # Create a pandas dataframe with the details
        prdt_df = pd.DataFrame(details, index=[0])
    
        # Append the details to the list_of_details
        list_of_details.append(prdt_df)
    return list_of_details

details=getdetails(links_of_product)


def preprocess_product_details(list_of_details):
    # Concatenate the details of all products into a single dataframe
    prdt_table = pd.concat(list_of_details, ignore_index=True)

    # Reset the index of the final dataframe
    prdt_table = prdt_table.reset_index(drop=True)

    # Fill NaN values with 'N.A'
    prdt_table.fillna('N.A', inplace=True)

    # Modify the 'Best Sellers Rank' column
    prdt_table['Best Sellers Rank'] = prdt_table['Best Sellers Rank'].str.replace('#', '').replace('\n', ' ')

    # Drop the 'Customer Reviews' column
    prdt_table = prdt_table.drop('Customer Reviews', axis=1)

    return prdt_table

preprocess_product_details(list_of_details)


fig = px.scatter(prdt_table,x ='Price', y='Rating Out of 5', color='Rating Out of 5', hover_data=[prdt_table['Name'].tolist()])
fig.show()




fig = px.histogram(prdt_table, x='Rating Out of 5', color='Rating Out of 5', nbins=10,marginal='rug',hover_data=prdt_table.columns)
fig.show()



hist_data = [prdt_table['Rating Out of 5'].tolist()]
group_lables = ['Rating Out of 5']
chrt = ff.create_distplot(hist_data, group_lables)
chrt.show()




hist_data = [prdt_table['Price'].tolist()]
group_lables = ['Price']
chrt = ff.create_distplot(hist_data, group_lables, bin_size=0.5)
chrt.show()



column_data = prdt_table['Price']

# Find the distribution of the column
column_distribution = column_data.value_counts().reset_index()
column_distribution.columns = ['Value', 'Count']

# Visualize the distribution using a bar plot
fig = px.bar(column_distribution, x='Value', y='Count', title='Distribution of {}'.format('Price'))
fig.show()


# Display the DataFrame in Streamlit
st.dataframe(prdt_table)

# Display the scatter plot in Streamlit
st.plotly_chart(fig)