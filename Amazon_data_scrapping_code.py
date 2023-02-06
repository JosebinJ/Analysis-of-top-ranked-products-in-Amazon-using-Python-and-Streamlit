from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd



product = input('State the product:')
browser = webdriver.Chrome()
browser.get('https://www.amazon.in')
elem = browser.find_element(By.ID, 'twotabsearchtextbox')
elem.send_keys(product)
elem2 = browser.find_element(By.ID, 'nav-search-submit-button')
elem2.click()

n_p = int(browser.find_elements(By.CLASS_NAME, 's-pagination-item.s-pagination-disabled')[1].text)
links=[]
for product in range(3):
    products = list(set(browser.find_elements(By.CLASS_NAME, 'a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))
    for product in products:
        links.append(product.get_attribute('href'))
    browser.find_element(By.CLASS_NAME, 's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator').click()
    browser.implicitly_wait(15)
    
product_name = []
product_price = []
product_rating = []
number_of_ratings= []
    

for i in range (len(links)):
    pr = browser.get(links[i])
    name = browser.find_element(By.XPATH,'//span[@class="a-size-large product-title-word-break"]')
    prname = name.text
    
    rating = browser.find_element(By.XPATH,'//span[@class="a-size-base a-nowrap"]')
    pr_rating = float(rating.text.split()[0])
    
    numrating = browser.find_element(By.XPATH,'//span[@id="acrCustomerReviewText"]')
    pr_numrating = float(numrating.text.split()[0].replace(',',''))
    try:
        price = browser.find_element(By.XPATH,'//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]')
        new_price = float(price.text.strip('₹').replace(',',''))
    except:
        new_price='N.A'
        pass
    
    product_name.append(prname)
    product_price.append(new_price)
    product_rating.append(pr_rating)
    number_of_ratings.append(pr_numrating)
    
    time.sleep(2)

df = pd.DataFrame({'Product Name': product_name, 'Price': product_price, 'Rating': product_rating ,'Number of Ratings': number_of_ratings})

df.drop_duplicates(subset=None, keep='first', inplace=True)
df


print(df)
