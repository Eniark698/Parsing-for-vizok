import json, re
#from parsel import Selector
import numpy as np
import pandas as pd
import time
import random
import math
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
#from selenium_recaptcha_solver import RecaptchaSolver

from threading import Thread
from bs4 import BeautifulSoup
#from captcha_bypass import solve_captcha




def split_dataframe(df, num_splits):
    """
    Splits the DataFrame into a specified number of chunks.

    Parameters:
        df (DataFrame): The DataFrame to be split.
        num_splits (int): The number of chunks to split the DataFrame into.

    Returns:
        list: A list of chunks, where each chunk is a DataFrame.
    """
    avg = math.ceil(len(df) / num_splits)
    split_dfs = [df.iloc[i * avg: (i + 1) * avg] for i in range(num_splits)]
    return split_dfs


def del_uah(price):
    match = re.search(r'([\d\s,]+)', price)
    if match:
        number_str = match.group(1).replace(' ', '').replace(',', '.').replace('\xa0', '')
        number_float = float(number_str)
    else:
        number_float=None
    return number_float



def del_deliver(price):
    a=price.find(":")
    b=price.find('грн')
    try:
        if a==-1 or b==-1: 
            price=0
        else:
            price=float(price[a+1:b-1].replace(' ', '').replace(',', '.'))
            if price==None:
                price=0
    except:
        price=0
    return price

def request_scrap(param_item):
    

   
    # proxies_choose=random.choice(proxy_list)
    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
    ]

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    # }
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls



    # params = {
    #     "q": param_item.replace(' ', '+'),
    #     "hl": "uk",     # language
    #     "gl": "ua",     # country of the search, UA -> Ukraine
    #     "tbm": "shop"   # google search shopping tab
    # }
    
    

    # chrome_options = Options()
    # chrome_options.add_argument("--user-data-dir=C:/Users/nmozol/AppData/Local/Google/Chrome/User Data/Default")
    # chrome_options.add_argument(f"--proxy-server=http://localhost:16379")
    # chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--remote-debugging-port=9222")
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--disable-extensions")

    # chrome_options.binary_location='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

    #browser = webdriver.Chrome(options=chrome_options)


    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", random.choice(user_agents))
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", "localhost")
    profile.set_preference("network.proxy.http_port", 16379)
    options = webdriver.FirefoxOptions()
    options.profile = profile
    options.add_argument('--kiosk')
    options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)


    # # Set Firefox options
    # firefox_options = Options()
    # firefox_options.add_argument("--start-maximized")
    # # Specify the path to the Firefox profile
    # firefox_profile = webdriver.FirefoxProfile(r'C:/Users/nmozol/AppData/Local/Mozilla/Firefox/Profiles/4lbtvq9g.default-release')

    # # Add custom user agent
    # firefox_profile.set_preference("general.useragent.override", random.choice(user_agents))

    # # Set other preferences (example with proxy)
    # firefox_profile.set_preference("network.proxy.type", 1)
    # firefox_profile.set_preference("network.proxy.http", "localhost")
    # firefox_profile.set_preference("network.proxy.http_port", 16379)

    # # Add the profile to the options
    # firefox_options.profile = firefox_profile

    # # Create a new instance of the Firefox driver
    # browser = webdriver.Firefox()

    browser.set_page_load_timeout(30)
    browser.implicitly_wait(5)

    # with open('./temp/cookies.txt', 'r') as f:
    #     cookies=json.load(f)
    # # Convert your cookies object to a list of cookie dictionaries
    # #cookies_list = [{'name': name, 'value': value} for name, value in cookies.items()]
    # for el in cookies:
    #     el['sameSite']='Lax'

    # context.add_cookies(cookies)

    #page.set_user_agent(random.choice(user_agents))
    #url = "https://www.google.com/search?" + "&".join([f"{k}={v}" for k, v in params.items()])
    url='https://www.google.com/?tbm=shop'
    browser.get(url)

    time.sleep(random.uniform(1,2))
    #driver_login(browser)
    time.sleep(random.uniform(1,2))
    search_input=browser.find_element(By.NAME, 'q')
    time.sleep(random.uniform(1,2))
    search_input.send_keys(param_item)
    time.sleep(random.uniform(1,2))
    search_input.send_keys(Keys.RETURN)
    time.sleep(random.uniform(2,4))
    # solver = RecaptchaSolver(driver=browser)
    # recaptcha_iframe = browser.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
   
    # result = captcha_bypass.solve_captcha(browser, recaptcha_iframe)




    # Wait until the "Shopping" link is present in the DOM
    # wait = WebDriverWait(browser, 30)
    # shopping_button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space(text())='Покупки']")))

    # # Click the button
    # shopping_button.click()

    # time.sleep(random.uniform(1,3))

    info=[]
    while True:
        # Get page source to use with BeautifulSoup
        page_source = browser.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Get all style elements
        styles = soup.find_all('style')
        
        # Get CSS as a single string
        css = '\n'.join([style.get_text() for style in styles])







        def get_original_images(soup):
            all_script_tags = "".join(
            [str(script).replace("</script>", "</script>\n") for script in soup.select("script")]
        )

            image_urls = []

            for result in soup.select(".Qlx7of .sh-dgr__grid-result"):
                data_pck = result.attrs.get('data-pck', '')
                url_with_unicode = re.findall(rf"var\s?_u='(.*?)';var\s?_i='{data_pck}';", all_script_tags)

                if url_with_unicode:
                    url_decode = bytes(url_with_unicode[0], 'ascii').decode('unicode-escape')
                    image_urls.append(url_decode)

            return image_urls

        def get_suggested_search_data():
            google_shopping_data = []
            
            for result in soup.select(".Qlx7of .i0X6df"):
                title = result.select_one(".tAxDx").get_text(strip=True) if result.select_one(".tAxDx") else None
                product_link = "https://www.google.com" + result.select_one(".Lq5OHe")["href"] if result.select_one(".Lq5OHe") else None

                product_rating_element = result.select_one(".NzUzee .Rsc7Yb")
                product_rating = product_rating_element.get_text(strip=True) if product_rating_element else None

                product_reviews_element = result.select_one(".NzUzee > div")
                product_reviews = product_reviews_element.get_text(strip=True) if product_reviews_element else None

                price_element = result.select_one(".a8Pemb")
                price = price_element.get_text(strip=True) if price_element else None

                store_element = result.select_one(".aULzUe")
                store = store_element.get_text(strip=True) if store_element else None

                store_link_element = result.select_one(".eaGTj div a")
                store_link = "https://www.google.com" + store_link_element["href"] if store_link_element else None

                delivery_element = result.select_one(".vEjMR")
                delivery = delivery_element.get_text(strip=True) if delivery_element else None

                compare_prices_link_element = result.select_one(".Ldx8hd .iXEZD")
                compare_prices_link_value = compare_prices_link_element["href"] if compare_prices_link_element else None
                compare_prices_link = "https://www.google.com" + compare_prices_link_value if compare_prices_link_value else None

                google_shopping_data.append({
                    "title": title,
                    "product_link": product_link,
                    "product_rating": product_rating,
                    "product_reviews": product_reviews,
                    "price": price,
                    "store": store,
                    "store_link": store_link,
                    "delivery": delivery,
                    "compare_prices_link": compare_prices_link,
                })
                
            return google_shopping_data
        
        try:
            next_page_button = browser.find_element(By.XPATH,'//span[contains(text(), "Уперед")]')
        except NoSuchElementException:
            # If no "next page" button is found, break out of the loop
            break

        
        next_page_button.click()


    info.extend(get_suggested_search_data())
    browser.quit()
    #json.dumps(google_shopping_data, indent=2, ensure_ascii=False)
    #return get_suggested_search_data()
    return info


def run(df):
    import sqlite3
    con=sqlite3.connect('./google_shop/temp_name_all.db') 
    cur=con.cursor()

    for index, row in df.iterrows():
        file=request_scrap(row['name'])

        try:
            large_str=json.loads(file)
        except:
            continue

        for product in large_str:

            SearchInfoName=row['name']

            SearchInfoCode=str(row['code'])

            try:
                Name=product['title'].strip()
            except:
                Name=None

            try:
                Seller=product['store'].strip()
            except:
                Seller=None


            try:
                ItemOnStoreUrl=product['store_link'].strip()
            except:
                ItemOnStoreUrl=None

            try:
                ItemOnGoogleShopUrl=product['product_link'].strip()
            except:
                ItemOnGoogleShopUrl=None

            try:
                Price=del_uah(product['price'])
            except:
                Price=None

            try:
                DeliveryPrice=del_deliver(product['delivery'])
            except:
                DeliveryPrice=None

            try:
                DeliveryInfo=product['delivery'].strip()
            except:
                DeliveryInfo=None

            try:
                ProductRating=float(product['product_rating'].strip().replace(',', '.'))
            except:
                ProductRating=None

            
            try:
                ComparePricesLink=product['compare_prices_link'].strip()
            except:
                ComparePricesLink=None

            data=(SearchInfoName,SearchInfoCode,Name, Seller,ItemOnStoreUrl,ItemOnGoogleShopUrl, Price,DeliveryPrice, DeliveryInfo, ProductRating,ComparePricesLink )
            #print(product['product_rating'])
            #print(product['product_reviews'])
            #print(product['store_rating'])
            #print(product['store_reviews'])
            cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?,?,?,?)""", data)
            
            con.commit()



def main():
    
    import sqlite3
    con=sqlite3.connect('./google_shop/temp_name_all.db')
    #con.isolation_level=None
    cur=con.cursor()
    
    cur.execute('''create table if not exists temp_table(
                        search_info_name nvarchar(500),
                        search_info_code varchar(250),
                        title nvarchar(500),
                        store nvarchar(255),
                        item_on_store_url varchar(3000),
                        item_on_google_shop_url varchar(3000),
                        price float,
                        delivery_price float,
                        delivery_info nvarchar(500),
                        product_rating float,
                        compare_prices_link nvarchar(4000)
                        );
                        ''')

    con.commit()
    cur.execute('''delete from  temp_table;''')

    con.commit()


    
    






    
    num_processes = 1
    
    dataframe=pd.read_excel('./google_shop/file_temp.xlsx',dtype=str)
    # Convert your global 'links' list to a list that can be shared between processes
    #dataframe['code'] = dataframe['code'].astype(str)
    # Split the URLs into 10 separate chunks
    split_df = split_dataframe(dataframe, num_processes)

    # Create 10 separate processes
    threads = []
    for i in range(num_processes):
        t = Thread(target=run, args=(split_df[i],))
        threads.append(t)

    
    # Start all the processes
    for t in threads:
        t.start()
    
    # Wait for all processes to complete
    for t in threads:
        t.join()

    
    print("All processes are complete in main2.")