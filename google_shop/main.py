import numpy as np
import pandas as pd
import os
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time


pwd=os.getcwd()


import sqlite3
con=sqlite3.connect(pwd+'/google_shop/temp_name.db')
#con.isolation_level=None
cur=con.cursor()
cur.execute('''create table if not exists temp_table(
                    search_info nvarchar(500),
                    page_url nvarchar(500),
                    code nvarchar(50),
                    name nvarchar(500),
                    price float,
                    seller nvarchar(255),
                    item_url nvarchar(500),
                    true_match bit);
                    ''')

con.commit()


def del_uah(price):
    match = re.search(r'([\d\s,]+)', price)
    if match:
        number_str = match.group(1).replace(' ', '').replace(',', '.')
        number_float = float(number_str)
    else:
        number_float=None
    return number_float

df=pd.read_excel(pwd+'/google_shop/file.xlsx',)
df.rename(columns={'ТОП SKU для тесту Google shopping':'name'}, inplace=True)

df['code'] = df['name'].str.extract(r'\((.*?)\)')
df['name_without_barcode'] = df['name'].str.replace(r'\(.*?\)', '', regex=True).str.strip()


def scrap_google_shop(search_info,code):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"https://www.google.com/search?tbm=shop&q={search_info}")
        page_url=page.url
        soup = BeautifulSoup(page.content(), 'html.parser')
        containers = soup.find_all('div', class_='KZmu8e Ehwxtb')
       
        match_var=True
        for container in containers:
            #time.sleep(100)
            try:
                full_name = container.find('h3', class_='sh-np__product-title translate-content').text.strip()
            except:
                full_name=None
            
            try:
                price=container.find('b', class_='translate-content').text.strip().replace('\xa0', '')
                
                price=del_uah(price)
            except:
                price=None

            try:
                seller = container.find('span', class_='E5ocAb').text.strip()
            except:
                seller=None

            try:
                item_url=container.find('a', class_='shntl').attrs['href']
                pos=item_url.find('https://')
                item_url=item_url[pos:]
            except:
                item_url=None

            # try:
            #     list_sites=container.find('a', class_='iXEZD')
            # except:
            #     try:

            #         with page.expect_popup() as popup_info:
            #             page.click('h3.sh-np__product-title.translate-content')
            #             print('waiting')

            #         new_page = popup_info.page

            #         item_url=new_page.url
            #         new_page.close()
            #     except:
            #         item_url=None
                
                
            # else:
            #     try:

            #         with page.expect_popup() as popup_info:
            #             page.click('div. _-c- main-image')
            #             print('waiting too')

            #         new_page = popup_info.page

            #         item_url=new_page.url
            #         new_page.close()
            #     except:
            #         item_url=None





                # with page.expect_popup() as popup_info:
                #     page.click('a.iXEZD')
                # new_page = popup_info.page
                # soup1 = BeautifulSoup(new_page.content(), 'html.parser')
                # prices=[]
                # sellers=[]

                # containers_new = soup.find_all('tr', class_='sh-osd__offer-row')

                # try:
                #     full_name=soup1.find('a', class_='BvQan sh-t__title sh-t__title-pdp translate-content').text
                # except:
                #     full_name=None
                # for container_new in containers_new:
                #     try:
                #         seller = container_new.find('a', class_='b5ycib shntl').text.strip()
                #     except:
                #         seller=None

                #     try:
                #         price=container.find('span', class_='g9WBQb fObmGc').text.strip().replace('\xa0', '')
                        
                #         price=del_uah(price)
                #     except:
                #         price=None

                #     try:
                #         with new_page.expect_popup() as popup_info_new:
                #             new_page.click('div.Kl9jM UKKY9')
                #         new_page1 = popup_info_new.new_page
                #         item_url=new_page1.url
                #     except:
                #         item_url=None

                #     data=(search_info,page_url,code,full_name,price,seller,item_url,match_var)
                #     cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?)""", data)
                #     con.commit()
                



            data=(search_info,page_url,code,full_name,price,seller,item_url,match_var)
            cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?)""", data)
            con.commit()
                
            
        
        match_var=False
        containers = soup.find_all('div', class_='sh-dgr__gr-auto sh-dgr__grid-result')
        for container in containers:
            
            try:
                full_name = container.find('h3', class_='tAxDx').text.strip()
            except:
                full_name=None
            
            try:
                price=container.find('span', class_='a8Pemb OFFNJ').text.strip().replace('\xa0', '')
                price=del_uah(price)
            except:
                price=None
                

            try:
                seller = container.find('div', class_='aULzUe IuHnof').text.strip()
            except:
                seller=None
            # try:

            #     with page.expect_popup() as popup_info:
            #         page.click('h3.tAxDx')

            #     new_page = popup_info.page

            #     item_url=new_page.url
            #     new_page.close()
            # except:
            #     item_url=None
            try:
                item_url=container.find('a', class_='shntl').attrs['href']
                pos=item_url.find('https://')
                item_url=item_url[pos:]
            except:
                item_url=None
            data=(search_info,page_url,code,full_name,price,seller,item_url, match_var)
            cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?)""", data)
            con.commit()



       
        
        # Always remember to close the browser
        browser.close()
    return None




for index, row in df.iterrows():
    scrap_google_shop(row['name'],row['code'])