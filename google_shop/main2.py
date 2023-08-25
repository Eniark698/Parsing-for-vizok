import requests, json, re
from parsel import Selector
import numpy as np
import pandas as pd
import os
import time
from pprint import pprint




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
    price=float(price[a+1:b-1].replace(' ', '').replace(',', '.'))
    return price

def request_scrap(param_item):

    proxies = {
    'HTTPS': '20.219.183.188:3129'
    }
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

    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30, proxies=proxies)
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
            store_link = "https://www.google.com" + result.css(".eaGTj div a::attr(href)").get()        
            delivery = result.css(".vEjMR::text").get()

            store_rating_value = result.css(".zLPF4b .XEeQ2 .QIrs8::text").get()
            # https://regex101.com/r/kAr8I5/1
            store_rating = re.search(r"^\S+", store_rating_value).group() if store_rating_value else store_rating_value

            store_reviews_value = result.css(".zLPF4b .XEeQ2 .ugFiYb::text").get()
            # https://regex101.com/r/axCQAX/1
            store_reviews = re.search(r"^\(?(\S+)", store_reviews_value).group() if store_reviews_value else store_reviews_value

            store_reviews_link_value = result.css(".zLPF4b .XEeQ2 .QhE5Fb::attr(href)").get()
            store_reviews_link = "https://www.google.com" + store_reviews_link_value if store_reviews_link_value else store_reviews_link_value

            compare_prices_link_value = result.css(".Ldx8hd .iXEZD::attr(href)").get()      
            compare_prices_link = "https://www.google.com" + compare_prices_link_value if compare_prices_link_value else compare_prices_link_value

            google_shopping_data.append({
                "title": title,
                "product_link": product_link,
                "product_rating": product_rating,
                "product_reviews": product_reviews,
                "price": price,
                "store": store,
                "thumbnail": thumbnail,
                "store_link": store_link,
                "delivery": delivery,
                "store_rating": store_rating,
                "store_reviews": store_reviews,
                "store_reviews_link": store_reviews_link,
                "compare_prices_link": compare_prices_link,
            })
        return json.dumps(google_shopping_data, indent=2, ensure_ascii=False)
    return get_suggested_search_data()
 

pwd=os.getcwd()


import sqlite3
con=sqlite3.connect(pwd+'/google_shop/temp_name.db')
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
                    product_reviews int,
                    store_rating float,
                    store_reviews int,
                    store_reviews_link varchar(3000),
                    ProductPhotoUrl varchar(3000),
                    compare_prices_link nvarchar(5000)
            );
                    ''')

con.commit()












df=pd.read_excel(pwd+'/google_shop/file.xlsx',)
#df.rename(columns={'ТОП SKU для тесту Google shopping':'name'}, inplace=True)

df['code'] = df['name'].str.extract(r'\((.*?)\)')





for index, row in df.iterrows():
   
    large_str=json.loads(request_scrap(row['name']))
    for product in large_str:

        SearchInfoName=row['name']

        SearchInfoCode=row['code']

        Name=product['title'].strip()

        Seller=product['store'].strip()

        ItemOnStoreUrl=product['store_link'].strip()

        ItemOnGoogleShopUrl=product['product_link'].strip()

        try:
            Price=del_uah(product['price'])
        except:
            Price=None

        try:
            DeliveryPrice=del_deliver(product['delivery'])
        except:
            DeliveryPrice=None

        DeliveryInfo=product['delivery'].strip()

        try:
            ProductRating=float(product['product_rating'].strip().replace(',', '.'))
        except:
            ProductRating=None

        try:
            ProductReviews=int(product['product_reviews'].strip().replace(',', '.'))
        except:
            ProductReviews=None

        try:
            StoreRating=int(product['store_rating'].strip().replace(',', '.'))
        except:
            StoreRating=None

        try:
            StoreReviews=int(product['store_reviews'].strip().replace(',', '.'))
        except:
            StoreReviews=None

        try:
            StoreReviewsLink=product['store_reviews_link'].strip()
        except:
            StoreReviewsLink=None

        try:
            ProductPhotoUrl=product['thumbnail'].strip()
        except:
            ProductPhotoUrl=None

        try:
            ComparePricesLink=product['compare_prices_link'].strip()
        except:
            ComparePricesLink=None

        data=(SearchInfoName,SearchInfoCode,Name, Seller,ItemOnStoreUrl,ItemOnGoogleShopUrl, Price,DeliveryPrice, DeliveryInfo, ProductRating,  ProductReviews, 
              StoreRating,StoreReviews,StoreReviewsLink,ProductPhotoUrl,ComparePricesLink )
        #print(product['product_rating'])
        #print(product['product_reviews'])
        #print(product['store_rating'])
        #print(product['store_reviews'])
        cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
        con.commit()