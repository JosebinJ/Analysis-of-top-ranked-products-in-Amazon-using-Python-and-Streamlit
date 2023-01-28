# importing required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import html5lib

# creating user defined function for extraction
def findout(product):
    browser = webdriver.Chrome(r"C:\Users\HP\chromedriver_win32\chromedriver.exe")
    browser.get('https://www.amazon.in')
    elem = browser.find_element(By.ID, 'twotabsearchtextbox')
    elem.send_keys(product)
    elem2 = browser.find_element(By.ID, 'nav-search-submit-button')
    elem2.click()
    link = []
    n_p = int(browser.find_elements(By.CLASS_NAME, 's-pagination-item.s-pagination-disabled')[1].text)
    for j in range(n_p - 1):
        products = browser.find_elements(By.CLASS_NAME, 'a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
        for i in products:
            link.append(i.get_attribute('href'))
            browser.implicitly_wait(15)
        browser.find_element(By.CLASS_NAME, 's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator').click()
    browser.close()
    links_of_products = list(set(link))
    return links_of_products

# creating user defined function for scrapping the product details
def product_details(product_links):
    product_name = []
    product_price = []
    product_rating = []

    for products in product_links:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        r = requests.get(products, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        name = soup.find('h1', attrs={'id': 'title'})
        prdt_name = name.text.strip(" ")
        try:
            price = soup.find('span', attrs={'class': 'a-price-whole'})
            new_price = (price.text.replace(",",""))
        except AttributeError:
            pass
        try:
            rating = soup.find('i', attrs={'class': 'a-icon a-icon-star-medium a-star-medium-4 averageStarRating'})
        except AttributeError:
            pass
        try:
            rating = soup.find('span', attrs={'class': 'a-icon-alt'})
        except ValueError:
            pass
        crt_rating = rating.text.split(' ')
        product_name.append(prdt_name)
        product_price.append(float(new_price))
        product_rating.append(float(crt_rating[0]))
    return product_name, product_price, product_rating

# feeding user defined keyword to the function
name = input('State the name of the product:')
list_of_product = findout(name)
details = product_details(list_of_product)
print(details)