from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
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
        browser.implicitly_wait(10)
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

def get_details(links_of_product):
    list_of_details = []
    for link in links_of_product:
        details = details_of_product(link)
        prdt_df = pd.DataFrame(details, index=[0])
        list_of_details.append(prdt_df)
        if len(list_of_details) == 3:
            break
    return list_of_details

def preprocess_product_details(list_of_details):
    prdt_table = pd.concat(list_of_details, ignore_index=True)
    prdt_table = prdt_table.reset_index(drop=True)
    prdt_table.fillna('N.A', inplace=True)
    prdt_table['Best Sellers Rank'] = prdt_table['Best Sellers Rank'].str.replace('#', '').replace('\n', ' ')
    prdt_table = prdt_table.drop('Customer Reviews', axis=1)
    return prdt_table

# Set page header
st.title('Top ranked Products')


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
    list_of_details = get_details(links_of_product)

    prdt_table = preprocess_product_details(list_of_details)
    # Display the data table
    st.write(prdt_table)
    return prdt_table
prdt_table=show_data()


# Add visualizations
st.subheader('Visualizations')

# Generate distribution plot for Rating Out of 5
hist_data_rating = [prdt_table['Rating Out of 5'].tolist()]
group_labels_rating = ['Rating Out of 5']
fig_dist_rating = ff.create_distplot(hist_data_rating, group_labels_rating)

# Generate distribution plot for Price
hist_data_price = [prdt_table['Price'].tolist()]
group_labels_price = ['Price']
fig_dist_price = ff.create_distplot(hist_data_price, group_labels_price, bin_size=0.5)

# Generate bar plot for Price distribution
column_data = prdt_table['Price']
column_distribution = column_data.value_counts().reset_index()
column_distribution.columns = ['Value', 'Count']
fig_bar = px.bar(column_distribution, x='Value', y='Count', title='Distribution of Price')
# Generate scatter plot
fig_scatter = px.scatter(prdt_table, x='Price', y='Rating Out of 5', color='Rating Out of 5', hover_data=[prdt_table['Name'].tolist()])

# Generate histogram plot
fig_hist = px.histogram(prdt_table, x='Rating Out of 5', color='Rating Out of 5', nbins=10, marginal='rug', hover_data=prdt_table.columns)


# Display all visualizations in a single page
st.plotly_chart(fig_scatter)
st.plotly_chart(fig_hist)
st.plotly_chart(fig_dist_rating)
st.plotly_chart(fig_dist_price)
st.plotly_chart(fig_bar)
