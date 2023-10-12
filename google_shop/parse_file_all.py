import json, re
import pandas as pd
import time
import random
import math
import sys
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from threading import Thread
from multiprocessing import Process
from datetime import date



def extract_text(element, selector):
    sub_element = element.query_selector(selector)
    return sub_element.inner_text() if sub_element else None


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
    

    
    with sync_playwright() as p:
            
        


        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
            ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
            ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
            ,'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
        ]
        






        # params = {
        #     "q": param_item,
        #     "hl": "uk",     # language
        #     "gl": "ua",     # country of the search, US -> USA
        #     "tbm": "shop",   # google search shopping tab
        # }
       

        #proxy={"server": f'socks5://10.0.100.12:9050'}
        browser=p.firefox.launch_persistent_context('./temp/', headless = True, base_url='https://www.google.com', viewport={ 'width': 1280, 'height': 920 }, user_agent=random.choice(user_agents),permissions=['geolocation'],geolocation={'latitude':49.842957,"longitude":24.031111}, locale='uk-UA',timezone_id='Europe/Kyiv')
        page=browser.pages[0]
        stealth_sync(page)
        page.goto('https://www.google.com', wait_until='domcontentloaded')
        time.sleep(random.uniform(1.5, 5.9))
        page.click('textarea[name="q"]')
        time.sleep(random.uniform(1.5, 3.9))
        page.type('textarea[name="q"]', param_item) 
        page.keyboard.press("Enter")
        time.sleep(random.uniform(1.5, 2.9))
        
         # Click the "Shopping" tab
        page.click('text=Покупки')
        time.sleep(random.uniform(1.5, 4.9))



        def get_suggested_search_data():
            google_shopping_data = []
            
            

            for result in page.query_selector_all(".Qlx7of .i0X6df"):
                title = extract_text(result, ".tAxDx")

                product_link = "https://www.google.com" + result.query_selector(".Lq5OHe").get_attribute("href")
                product_rating = extract_text(result,".NzUzee .Rsc7Yb")
                product_reviews = extract_text(result,".NzUzee > div")
                price = extract_text(result,".a8Pemb")
                old_price = extract_text(result,".zY3Xhe")
                old_price1 = extract_text(result,".nSfGAb")
                store = extract_text(result,".aULzUe")
                try:
                    store_link_element = result.query_selector(".eaGTj div a")
                except:
                    store_link_element=None
                store_link = "https://www.google.com" + store_link_element.get_attribute("href") if store_link_element else None
                delivery = extract_text(result,".vEjMR")
                try:
                    compare_prices_link_value = result.query_selector(".Ldx8hd .iXEZD").get_attribute("href")
                except:
                    compare_prices_link_value=None

                compare_prices_link = "https://www.google.com" + compare_prices_link_value if compare_prices_link_value else compare_prices_link_value


                google_shopping_data.append({
                    "title": title,
                    "product_link": product_link,
                    "product_rating": product_rating,
                    "product_reviews": product_reviews,
                    "price": price,
                    "old_price": old_price,
                    "old_price1": old_price1,
                    "store": store,
                    "store_link": store_link,
                    "delivery": delivery,
                    "compare_prices_link": compare_prices_link,
                })
            return json.dumps(google_shopping_data, indent=2, ensure_ascii=False)


        
      
        data=[]
        while True:
            page.wait_for_load_state('load')
            temp=json.loads(get_suggested_search_data())

            data.extend(temp)
            

            try:
                page.keyboard.press("End")
                page.click('a#pnnext', timeout=10000)
            except:
                break

            
        browser.close()


        
        return data
 



def run(df):
    import sqlite3
    con=sqlite3.connect('./google_shop/temp_name_all.db') 
    cur=con.cursor()
    today = date.today()

    for index, row in df.iterrows():
        
        large_str=request_scrap(row['name'])
       

        for product in large_str:

            SearchInfoName=row['name'].strip()

            SearchInfoCode=None
            SearchInfoCode=str(row['code']).strip()

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
                OldPrice=del_uah(product['old_price'])
            except:
                try:
                    temp=re.findall(r'[\d,.]+',product['old_price1'])
                    OldPrice=float(temp[0].replace(',', '.'))
                except:

                    OldPrice=None

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

            data=(today,SearchInfoName,SearchInfoCode,Name, Seller,ItemOnStoreUrl,ItemOnGoogleShopUrl, Price, OldPrice, DeliveryPrice, DeliveryInfo, ProductRating,ComparePricesLink )
        
            cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
            
            con.commit()



def main(num_processes = 1):
    
    import sqlite3
    con=sqlite3.connect('./google_shop/temp_name_all.db')
    #con.isolation_level=None
    cur=con.cursor()
    
    cur.execute('''create table if not exists temp_table(
                        scrap_date date,
                        search_info_name nvarchar(500),
                        search_info_code varchar(250),
                        title nvarchar(500),
                        store nvarchar(255),
                        item_on_store_url varchar(3000),
                        item_on_google_shop_url varchar(3000),
                        price float,
                        old_price float,
                        delivery_price float,
                        delivery_info nvarchar(500),
                        product_rating float,
                        compare_prices_link nvarchar(4000)
                        );
                        ''')

    con.commit()
    cur.execute('''delete from  temp_table;''')

    con.commit()


    
    





    
   

    num_processes = 3
    
    dataframe=pd.read_excel('./google_shop/file_temp_all.xlsx',dtype=str)
    # Convert your global 'links' list to a list that can be shared between processes
    #dataframe['code'] = dataframe['code'].astype(str)
    # Split the URLs into 10 separate chunks
    split_df = split_dataframe(dataframe, num_processes)

    # Create 10 separate processes
    threads = []
    for i in range(num_processes):
        t = Process(target=run, args=(split_df[i],))
        threads.append(t)

    
    # Start all the processes
    for t in threads:
        t.start()
    
    # Wait for all processes to complete
    for t in threads:
        t.join()

    
    print("All processes are complete in parse_all.")