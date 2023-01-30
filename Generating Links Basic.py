#!/usr/bin/env python
# coding: utf-8

# In[33]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# In[34]:


browser=webdriver.Chrome()
browser.get('https://www.amazon.in')


# In[35]:


elem=browser.find_element(By.ID,'twotabsearchtextbox')
elem.send_keys("phone")


# In[30]:


elem


# In[36]:


elem2=browser.find_element(By.ID,'nav-search-submit-button')
elem2.click()


# In[44]:


n_p=int(browser.find_elements(By.CLASS_NAME,'s-pagination-item.s-pagination-disabled')[1].text)


# In[42]:


n_p


# In[45]:


product=browser.find_element(By.CLASS_NAME,'a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')


# In[46]:


product


# In[47]:


product.get_attribute('href')


# In[ ]:





# In[ ]:




