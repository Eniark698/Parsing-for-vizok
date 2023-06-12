from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
#from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import xpath
import dateparser
import datetime
import os
from alive_progress import alive_bar

from traceback import format_exc
import os
from warnings import filterwarnings
filterwarnings("ignore")


# get the current working directory
current_working_directory = os.getcwd()










# Your profile path
profile_path = 'C:/Users/nmozol/AppData/Local/Google/Chrome/User Data/Default'

# Setup selenium webdriver with a profile
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--profile-directory=Default")
options.add_argument("--incognito")
options.add_argument("--disable-plugins-discovery")
options.add_argument("--start-maximized")
options.add_argument("user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
s=Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=s, options=options)

            
driver.get('https://rozetka.com.ua/ua/chehli-dlya-manikyurnih-instrumentov/c4660489/')



# Wait until page is loaded
time.sleep(5)

# Define list to store reviews data
reviews = []




# Clicking the button to load more reviews
while True:
    try:
        wait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//rz-load-more[@class='ng-star-inserted']"))).click()
        time.sleep(3)
    except:
        break

# Get page source and parse it
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Get all review containers
containers = soup.find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')


#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pagination ng-star-inserted']/a[1]"))).click()
#quit()




# Extract data from each container
for container in containers:
    
    block = container.find('a', class_='goods-tile__picture ng-star-inserted').attrs['href']
    driver.execute_script(f'''window.open("{block}","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(block)
    time.sleep(3)



    soup1 = BeautifulSoup(driver.page_source, 'html.parser')

    code=soup1.find('p', class_='product__code detail-code').text.replace(' ', '')
    code_i=code.find(':')
    code=code[code_i+2:]
    name=soup1.find('h1', class_='product__title').text



    #finding review count
    try:
        review_number=int(soup1.find('span', class_='tabs__link-text ng-star-inserted').text.replace(' ', ''))
    except:
        review_number=None

    #finding seller name
    try:
        seller_parent=soup1.find('p', class_='product-seller__title')
        seller=seller_parent.find('img').attrs['alt']
    except:
        seller=None

    #finding current_price and old_price
    try:
        price=soup1.find('p', class_='product-price__big product-price__big-color-red').text
    except:
        try:
            price=soup1.find('p', class_='product-price__big').text
        except:
            price=None
    try:
        old_price=soup1.find('p', class_='product-price__small ng-star-inserted').text
    except:
        old_price=None

    #getting likes
    try:
        likes_count=int(soup1.find('p', class_='wish-count-text ng-star-inserted').text)
    except:
        likes_count=None

    
    #finding status
    try:
        status=soup1.find('p', class_='status-label status-label--green ng-star-inserted').text.lstrip()
    except:
        status=None



    try:
        number_of_questions=int(soup1.find('span', class_='tabs__link-text ng-star-inserted').text)
    except:
        number_of_questions=None



    try:
        formula=soup1.find('div', class_='recount ng-star-inserted').text
    except:
        formula=None

    try:
        delivery=soup1.find('div', class_='product-about__block-heading').text.lstrip()
    except:
        delivery=None

    stars_group1=soup1.find('ul', class_='product-stars')
    stars_group=stars_group1.find_all('li', class_='product-stars__item ng-star-inserted')
    s=0
    for star_icon in stars_group:
        s+=float(star_icon.find('stop').attrs['offset'])
    

    reviews={"code":code
            ,"stars":s
            ,"name":name
            ,"review_number":review_number
            ,"seller":seller
            ,"price":price
            ,"old_price":old_price
            ,"likes_count":likes_count
            ,"status":status
            ,"number_of_questions":number_of_questions
            ,"formula":formula
            ,"delivery":delivery
            }

    

    # time.sleep(3)
    #driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    #driver.execute_script(f'window.close("{block}","_blank");')
    time.sleep(3)



time.sleep(3)





# Create dataframe
df = pd.DataFrame(reviews)
df=df.drop_duplicates()

# Save to csv
df.to_csv(current_working_directory+'/here.csv', index=False, sep='\t', encoding='utf-16')
