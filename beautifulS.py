# importing the required libraries
import requests
import html5lib
from bs4 import BeautifulSoup

# parsing the url
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
url = "https://www.amazon.in/Samsung-Galaxy-Storage-MediaTek-Battery/dp/B0BMGC6LHP/ref=sr_1_1_sspa?crid=GD6UGMLR6SNJ&keywords=smartphone&qid=1674811928&sprefix=smartphone%2Caps%2C229&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY"
r = requests.get(url, headers=headers)

# printing the content
print(r.content)

# beautifying the html codes
soup = BeautifulSoup(r.content, 'html5lib')


# scrapping the name of the product
name = soup.find('h1',attrs = {'id':'title'})
print(name.text)

# scrapping the price of the product
price = soup.find('span', attrs = {'class':'a-offscreen'})
print(price.text)

# scrapping the rating of the product
rating = soup.find('span', attrs = {'class':'a-size-medium a-color-base'})
print(rating.text)

# taking the required part of the rating and converting it to integer
rat_ing = rating.text[0]
print(rat_ing)
