from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from traceback import format_exc
from datetime import datetime
from alive_progress import alive_bar
from re import findall as re_findall
from progress.bar import Bar
from tqdm import tqdm
from os import getcwd
import re

def find_indices(input_string, symbol):
    return [i for i, char in enumerate(input_string) if char == symbol]

def check_string(input_string):
    # The Ukrainian alphabet consists of the following characters:
    # А-Я, а-я, Є, є, Ґ, ґ, І, і, Ї, ї
    pattern = r'[А-Яа-яЄєҐґІіЇї]'
    if re.search(pattern, input_string):
        return False
    else:
        return True

def run(playwright):
    import sqlite3
    con=sqlite3.connect(getcwd()+'/maudau/temp.db')
    #con.isolation_level=None
    cur=con.cursor()

    cur.execute('''create table if not exists temp_table(
                code nvarchar(255),
                stars float,
                name nvarchar(255),
                review_number int,
                seller nvarchar(255),
                price nvarchar(255),
                old_price nvarchar(255),
                status nvarchar(255),
                new_code int,
                category_name nvarchar(255),
                subcategory_name nvarchar(255)
    )''')

    con.commit()




    viewport_size = {"width": 1920, "height": 1080}  # replace with your screen resolution
    global browser
    browser = playwright.chromium.launch(headless=False)

    
    context = browser.new_context(viewport=viewport_size)
    page = context.new_page()
    page.set_default_timeout(300000)
    base='https://maudau.com.ua/'
    page.goto(base) 
    page.wait_for_load_state('load')


    soup = BeautifulSoup(page.content(), 'html.parser')
    categories = soup.find_all('a', class_='category-link')
    bar = Bar('Processing', max=len(categories))

    for category in categories:
        category_url = category.attrs['href']
        if category_url == '/category/alkohol-i-napoi':
            continue
        category_url=base[:-1]+category_url
        page1=context.new_page()
        page1.set_default_timeout(300000)
        page1.goto(category_url)
        page1.wait_for_load_state('load')

        
        soup1 = BeautifulSoup(page1.content(), 'html.parser')
        category_name=soup1.find('div', class_='title').text

        subcategories = soup1.find_all('div', class_='wrapper__content')
        j1=0
        for subcategory in subcategories:
            subcategory_url=subcategory.find('a', class_='card__show-all').attrs['href']
            subcategory_url=base[:-1]+subcategory_url
            page2=context.new_page()
            page2.set_default_timeout(300000)
            page2.goto(subcategory_url)
            page2.wait_for_load_state('load')


            
            h1_element=page2.wait_for_selector('div.category-pagination-button', timeout=300000)
            j=0
            

            while True:
                try:
                    button = page2.wait_for_selector('div.category-pagination-button', timeout=30000)
                    page2.wait_for_function("document.querySelector('div.category-pagination-button').getAttribute('disabled') === null")
                    button = page2.wait_for_selector('div.category-pagination-button', timeout=30000)  # wait for 5 seconds
                    page2.click('div.category-pagination-button')
                    j+=1
                except:
                  # the button is no longer found or clickable
                    break

            print('\nclicked ' + str(j)+ ' times\n')

            soup2 = BeautifulSoup(page2.content(), 'html.parser')
            subcategory_name=soup2.find('h1').text


            containers = soup2.find_all('div', class_='product product-tile product-tile')
            for container in containers:
                subcontainer=container.find('a', class_='no-underline product-link-image').attrs['href']
                subcontainer=base[:-1]+subcontainer
                page3=context.new_page()
                page3.set_default_timeout(300000)
                page3.goto(subcontainer)
                page3.wait_for_load_state('load')



                soup3 = BeautifulSoup(page3.content(), 'html.parser')
                h1_element=page3.wait_for_selector('xpath=//h1', timeout=300000)

                try:
                    name=soup3.find('h1', class_='product-title').text
                except:
                    page3.close()
                    continue

                try:
                    code=soup3.find('span', class_='article-value').text
                    code=code[10:]
                except:
                    page3.close()


                try:
                    new_code=None
                    lb=find_indices(name, '(')
                    rb=find_indices(name, ')')

                    for iter in range(min(len(lb), len(rb))):
                        try_code=name[lb[iter]+1:rb[iter]]

                        if check_string(try_code):
                            new_code=try_code 
                        else:
                            continue
                except:
                    new_code=None

                try:
                    price=soup3.find('span', class_='price_final price_hot').text.replace(' ', '')
                    price=int(re_findall(r'\d+', price)[0])
                except:
                    price=None
            

                try:
                    old_price=soup3.find('span', class_='price_old').text.replace(' ', '')
                    old_price=int(re_findall(r'\d+', old_price)[0])
                except:
                    old_price=None

                try:
                    status=soup3.find('span', class_='status').text.lstrip()
                except:
                    status=None

                try:
                    seller=soup3.find('span', class_='merchant__name').text.strip()
                except:
                    seller=None

                try:
                    stars=float(soup3.find('span', class_='rating-count').text)
                except:
                    stars=None  
                
                try:
                    review_number=soup3.find('button', class_='rating-btn').text.replace(' ', '')
                    review_number = int(re_findall(r'\d+', review_number)[0])
                except:
                    review_number=None  

                data=(code
                            ,stars
                            ,name
                            ,review_number
                            ,seller
                            ,price
                            ,old_price
                            ,status
                            ,new_code
                            ,category_name
                            ,subcategory_name)
                    

                cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?,?,?,?)""", data)
                con.commit()
                
                page3.close()
                
            page2.close()
        page1.close()
        bar.next()

    bar.finish()
    page.close()   
    browser.close()  # Close the browser





try:
    with sync_playwright() as playwright:
        run(playwright)
except:
    try:
        browser.close()
    except:
        pass
    f=open(getcwd()+'/maudau/log.txt', 'a')
    f.write('----------------------------------------\n')
    f.write(format_exc())
    f.write('occurred on ' + str(datetime.now())+ '\n')
    f.write('----------------------------------------\n\n\n')
    f.close()