# importing required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# creating user defined function for extraction
def findout(product):
    browser = webdriver.Chrome()
    browser.get('https://www.amazon.in')
    elem = browser.find_element(By.ID,'twotabsearchtextbox')
    elem.send_keys(product)
    elem2 = browser.find_element(By.ID,'nav-search-submit-button')
    elem2.click()
    link = []
    n_p = int(browser.find_elements(By.CLASS_NAME,'s-pagination-item.s-pagination-disabled')[1].text)
    for j in range(n_p - 1):
        products = browser.find_elements(By.CLASS_NAME,'a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
        for i in products:
            link.append(i.get_attribute('href'))
            browser.implicitly_wait(15)
        browser.find_element(By.CLASS_NAME,'s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator').click()
        browser.close()
    return link


# feeding user defined keyword to the function
name = input('State the name of the product:')
list_of_product = findout(name)
print(list_of_product)
