import requests, json, re
from parsel import Selector
import numpy as np
import pandas as pd
import os
import time
import random
from datetime import datetime
from multiprocessing import Process
import math





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

    proxies = [
    {'HTTPS': '144.49.99.190:8080'},
    {'HTTPS': '144.49.99.170:8080'},
    {'HTTPS': '144.49.99.215:8080'},
    {'HTTPS': '103.22.238.173:8080'},
    {'HTTPS': '8.219.97.248:80'},
    {'HTTPS':'91.107.247.115:4000'},
    ]
    proxies_choose=random.choice(proxies)
    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": param_item,
        "hl": "uk",     # language
        "gl": "ua",     # country of the search, US -> USA
        "tbm": "shop"   # google search shopping tab
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30, proxies=proxies_choose)
    selector = Selector(html.text)

    def get_original_images():
        all_script_tags = "".join(
            [
                script.replace("</script>", "</script>\n")
                for script in selector.css("script").getall()
            ]
        )
        
        image_urls = []
        
        for result in selector.css(".Qlx7of .sh-dgr__grid-result"):
            # https://regex101.com/r/udjFUq/1
            url_with_unicode = re.findall(rf"var\s?_u='(.*?)';var\s?_i='{result.attrib['data-pck']}';", all_script_tags)

            if url_with_unicode:
                url_decode = bytes(url_with_unicode[0], 'ascii').decode('unicode-escape')
                image_urls.append(url_decode)
                
        return image_urls

    def get_suggested_search_data():
        google_shopping_data = []

        for result, thumbnail in zip(selector.css(".Qlx7of .i0X6df"), get_original_images()):
            title = result.css(".tAxDx::text").get()        
            product_link = "https://www.google.com" + result.css(".Lq5OHe::attr(href)").get()   
            product_rating = result.css(".NzUzee .Rsc7Yb::text").get()      
            product_reviews = result.css(".NzUzee > div::text").get()       
            price = result.css(".a8Pemb::text").get()       
            store = result.css(".aULzUe::text").get()     
            try:  
                store_link = "https://www.google.com" + result.css(".eaGTj div a::attr(href)").get()   
            except:
                store_link= None
            delivery = result.css(".vEjMR::text").get()

           
            compare_prices_link_value = result.css(".Ldx8hd .iXEZD::attr(href)").get()      
            compare_prices_link = "https://www.google.com" + compare_prices_link_value if compare_prices_link_value else compare_prices_link_value

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
        return json.dumps(google_shopping_data, indent=2, ensure_ascii=False)
    return get_suggested_search_data()
 


def run(df):
    import sqlite3
    con=sqlite3.connect('./google_shop/temp_name_all.db') 
    cur=con.cursor()

    for index, row in df.iterrows():
    
        large_str=json.loads(request_scrap(row['name']))
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


    num_processes = 10

    dataframe=pd.read_excel('./google_shop/file_temp.xlsx',dtype=str)
    # Convert your global 'links' list to a list that can be shared between processes
    #dataframe['code'] = dataframe['code'].astype(str)
    # Split the URLs into 10 separate chunks
    split_df = split_dataframe(dataframe, num_processes)

    # Create 10 separate processes
    processes = []
    for i in range(num_processes):
        p = Process(target=run, args=(split_df[i],))
        processes.append(p)
    
    # Start all the processes
    for p in processes:
        p.start()
    
    # Wait for all processes to complete
    for p in processes:
        p.join()


    print("All processes are complete in main2.")