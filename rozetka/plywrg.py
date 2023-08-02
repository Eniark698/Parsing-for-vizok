from playwright.sync_api import sync_playwright
import time
from site_list import links
from bs4 import BeautifulSoup
from traceback import format_exc
from datetime import datetime
from alive_progress import alive_bar
from os import getcwd


def run(playwright):
    
    import sqlite3
    con=sqlite3.connect(getcwd()+'/temp.db')
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
                likes_count int,
                status nvarchar(255),
                number_of_questions int,
                formula nvarchar(255),
                delivery nvarchar(255),
                preorder nvarchar(255),
                new_code int,
                category nvarchar(255)
    )''')

    con.commit()




    viewport_size = {"width": 1920, "height": 1080}  # replace with your screen resolution
    global browser
    browser = playwright.chromium.launch(headless=True)

    
    context = browser.new_context()#viewport=viewport_size)
    
    for key, urls in links.items():
        for url in urls:
            page = context.new_page()
            page.goto(url) 


            while True:
                try:
                    # Wait for a certain condition to be true
                    button = page.wait_for_selector('rz-load-more.ng-star-inserted', timeout=7500)  # wait for 5 seconds
                    page.wait_for_function("document.querySelector('rz-load-more.ng-star-inserted').getAttribute('disabled') === null")
                    
                    page.click('rz-load-more.ng-star-inserted')
                except:  # the button is no longer found or clickable
                    break
            

            soup = BeautifulSoup(page.content(), 'html.parser')
            # Get all review containers
            containers = soup.find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')

            with alive_bar(len(containers)) as bar:
                for container in containers:
                    # Extract the href attribute from the 'a' tag
                    block = container.find('a', class_='goods-tile__picture ng-star-inserted').attrs['href']

                    # Open a new page and navigate to the URL
                    new_page = context.new_page()
                    new_page.goto(block)

                    h1_element=new_page.wait_for_selector('xpath=//h1', timeout=3000)


                    soup1 = BeautifulSoup(new_page.content(), 'html.parser')
                    try:
                        code=soup1.find('p', class_='product__code detail-code').text.replace(' ', '')
                        code_i=code.find(':')
                        code=code[code_i+2:]
                    except:
                        new_page.close()
                        
                    name=soup1.find('h1', class_='product__title').text

                    try:
                        new_code=name[name.find("(")+1:name.find(")")]
                    except:
                        new_code=None



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
                        try:
                            seller=seller_parent.find('strong', class_='ng-star-inserted').text
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
                        preorder=soup1.find('div', class_='preorder-text-item ng-star-inserted').text
                    except:
                        preorder=None

                    

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
                    s=round(s,2)

                    data=(code
                                ,s
                                ,name
                                ,review_number
                                ,seller
                                ,price
                                ,old_price
                                ,likes_count
                                ,status
                                ,number_of_questions
                                ,formula
                                ,delivery
                                ,preorder
                                ,new_code
                                ,key)
                        

                    cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
                    con.commit()


                    # Close the new page
                    new_page.close()
                    bar()

                

        
    browser.close()  # Close the browser





try:
    with sync_playwright() as playwright:
        run(playwright)
except:
    try:
        browser.close()
    except:
        pass
    f=open(getcwd()+'/log.txt', 'a')
    f.write('----------------------------------------\n')
    f.write(format_exc())
    f.write('occurred on ' + str(datetime.now())+ '\n')
    f.write('----------------------------------------\n\n\n')
    f.close()