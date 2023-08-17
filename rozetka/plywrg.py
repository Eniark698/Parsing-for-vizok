from multiprocessing import Process, Manager
import math 
from new_list import links 
from playwright.sync_api import sync_playwright
import barcodenumber
import time
from bs4 import BeautifulSoup
from traceback import format_exc
from datetime import datetime
from alive_progress import alive_bar
from os import getcwd
import re



def split_urls(urls, num_splits):
    """
    Splits the list of URLs into a specified number of chunks.
    
    Parameters:
        urls (list): The list of URLs to be split.
        num_splits (int): The number of chunks to split the URLs into.
    
    Returns:
        list: A list of chunks, where each chunk is a list of URLs.
    """
    avg = math.ceil(len(urls) / num_splits)
    split_urls = [urls[i * avg: (i + 1) * avg] for i in range(num_splits)]
    return split_urls



def find_indices_str(input_string, substring):
    return [i for i in range(len(input_string)) if input_string.startswith(substring, i)]


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

def del_uah(price):
    if price != None:
        #index_uah=price.find('₴')
        price =int(float(price.replace(' ', '').replace('\xa0', '')[:-1]))
    else:
        price=None
    return price

def run(links_subset,shared_links):
    """
    Your existing run function, modified to accept a 'links_subset' parameter,
    which is the subset of URLs this process will work on.
    """
    with sync_playwright() as playwright:
        def rebuild(browser):

            try:
                browser.close()
            except:
                pass
            viewport_size = {"width": 1920, "height": 1080} 


            browser = playwright.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-webgl', '--disable-extensions', '--disable-gpu'])
            context = browser.new_context(viewport=viewport_size, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            return browser, context
    

        import sqlite3
        con=sqlite3.connect(getcwd()+'/rozetka/temp.db')
        #con.isolation_level=None
        cur=con.cursor()

        cur.execute('''create table if not exists temp_table(
                    code nvarchar(255),
                    stars float,
                    name nvarchar(255),
                    review_number int,
                    seller nvarchar(255),
                    price int,
                    old_price int,
                    likes_count int,
                    status nvarchar(255),
                    number_of_questions int,
                    formula nvarchar(255),
                    delivery nvarchar(255),
                    preorder nvarchar(1000),
                    new_code nvarchar(255),
                    renew_code nvarchar(255),
                    category_1st_lvl nvarchar(255),
                    category_2nd_lvl nvarchar(255),
                    category_3rd_lvl nvarchar(255),
                    category_4th_lvl nvarchar(255),
                    url nvarchar(500),
                    Barcodetype_url nvarchar(15),
                    Barcodetype_name nvarchar(15));
                    ''')

        con.commit()





        
        browser=None

        browser,context = rebuild(browser)
        
    
        
            
        for url in links_subset:


            
            browser,context = rebuild(browser)
            print('rebuilding')
            start = time.time()

            page = context.new_page()
            page.set_default_timeout(600000)
            page.wait_for_load_state('networkidle', timeout=600000)
            page.goto(url) 
            
            



            j=0
            while True:
                try:
                    button = page.wait_for_selector('rz-load-more.ng-star-inserted', timeout=30000)
                    page.wait_for_function("document.querySelector('rz-load-more.ng-star-inserted').getAttribute('disabled') === null")
                    button = page.wait_for_selector('rz-load-more.ng-star-inserted', timeout=30000)  # wait for 5 seconds
                    page.click('rz-load-more.ng-star-inserted')


                    j+=1
                except:
                    # the button is no longer found or clickable
                    break
                
            

            soup = BeautifulSoup(page.content(), 'html.parser')
            last_cat=soup.find('h1', class_='catalog-heading ng-star-inserted').text

            mult_cat=[]
            temp_array=soup.find_all('a', class_='breadcrumbs__link')
            for el in temp_array:
                if el.text =='На головну':
                    continue
                mult_cat.append(el.text)
            mult_cat.append(last_cat)

            print('\nclicked ' + str(j)+ ' times on ', mult_cat , '\n')
            try:
                mult_cat[0]
            except:
                mult_cat.append(None)


            try:
                mult_cat[1]
            except:
                mult_cat.append(None)

            try:
                mult_cat[2]
            except:
                mult_cat.append(None)


            try:
                mult_cat[3]
            except:
                mult_cat.append(None)



            # Get all review containers
            containers = soup.find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')
            iterator=0
            
            for container in containers:

                # Extract the href attribute from the 'a' tag
                block = container.find('a', class_='goods-tile__picture ng-star-inserted').attrs['href']

                # Open a new page and navigate to the URL
                new_page = context.new_page()
                new_page.set_default_timeout(600000)
                new_page.wait_for_load_state('networkidle', timeout=600000)
                new_page.goto(block)


                
                new_page.wait_for_load_state('networkidle',timeout=300000)
                h1_element=new_page.wait_for_selector('xpath=//h1', timeout=300000)
                
                
                
                
                cur_url=new_page.url
                array_index_1=find_indices(cur_url, '/')
                part_url=cur_url[array_index_1[-3]+1:array_index_1[-2]]

                array_index_2=find_indices(part_url, '_')
                array_index_3=find_indices(part_url, '-')
                
                
                if array_index_2!=[]:
                    renew_code=part_url[array_index_2[-1]+1:]
                elif array_index_3!=[]:
                    renew_code=part_url[array_index_3[-1]+1:]
                else:
                    renew_code=part_url
                

                soup1 = BeautifulSoup(new_page.content(), 'html.parser')
                try:
                    code=soup1.find('p', class_='product__code detail-code').text.replace(' ', '')
                    code_i=code.find(':')
                    code=code[code_i+2:]
                except:
                    code=None

                
                try: 
                    name=soup1.find('h1', class_='product__title').text.strip()
                except:
                    try:
                        name=soup1.find('h1', class_='product__title-left product__title-collapsed ng-star-inserted').text.strip()
                    except Exception as e:
                        new_page.screenshot(path="./screenshot.png")

                        print(e)
                        print(url)
                        name=None
                    # new_page.close()
                    # continue

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



                if new_code==None:
                    code_array_1=[None]
                else:
                    code_array_1=[]
                    code_array=new_code.split('/')

    
                    for iter in code_array:
                        array_new=iter.split('_')
                        for item in array_new:
                            code_array_1.append(item)

                    try:
                        code_array_1.remove('1')
                    except:
                        pass
                






                

                #finding seller name
                try:
                    seller_parent=soup1.find('p', class_='product-seller__title')
                    seller=seller_parent.find('img').attrs['alt']
                except:
                    try:
                        seller=seller_parent.find('strong', class_='ng-star-inserted').text.strip()
                    except:
                        try:
                            seller=seller_parent.find('span', class_='ng-star-inserted').text.strip()
                        except:
                            seller=None
            
                
                #finding current_price and old_price
                try:
                    price1=soup1.find('p', class_='product-price__big product-price__big-color-red').text.strip()
                except:
                    try:
                        price1=soup1.find('p', class_='product-price__big').text.strip()
                    except:
                        price1=None
                



                
                try:
                    old_price1=soup1.find('p', class_='product-price__small ng-star-inserted').text.strip()
                except:
                    old_price1=None


                try:
                    price=del_uah(price1)
                    old_price=del_uah(old_price1)
                except:
                    price=None
                    old_price=None



                #getting likes
                try:
                    #p1_element=new_page.wait_for_selector('xpath=/html/body/app-root/div/div/rz-product/div/rz-product-tab-main/div[1]/div[1]/div[2]/rz-product-main-info/div[1]/div[1]/div[2]/app-goods-wishlist/div/p', timeout=10000)
                    likes_count=int(soup1.find('p', class_='wish-count-text ng-star-inserted').text)
                except:
                    likes_count=None
                

                #finding status
                try:
                    status=soup1.find('p', class_='status-label status-label--green ng-star-inserted').text.lstrip()
                except:
                    try:
                        status=soup1.find('p', class_='status-label status-label--orange ng-star-inserted').text.lstrip()
                    except:
                        status=None
                
                try:
                    preorder=soup1.find('div', class_='preorder-text-item ng-star-inserted').text
                except:
                    preorder=None

                
                tabs=soup1.find_all('li', class_='tabs__item ng-star-inserted')
                try:
                    number_of_questions=int(tabs[3].find('span', class_='tabs__link-text ng-star-inserted').text.strip().replace(' ', ''))
                    
                except:
                    number_of_questions=None


                #finding review count
                try:
                    review_number=int(tabs[2].find('span', class_='tabs__link-text ng-star-inserted').text.strip().replace(' ', ''))
                except:
                    review_number=None
            
                
                

                try:
                    formula=soup1.find('div', class_='recount ng-star-inserted').text
                except:
                    formula=None

                try:
                    delivery=soup1.find('p', class_='product-delivery__heading-text').text.strip()
                except:
                    delivery=None
                

                try:
                    s=soup1.find('div', class_='stars__rating').attrs['style']
                    li=s.find('(')
                    ri=s.find('%')
                    s=round(float(s[li+1:ri])/20,2)
                except:
                    s=None
                try:
                    if barcodenumber.check_code('code39',renew_code):
                        Barcodetype_url='code39'
                    elif barcodenumber.check_code('ean13',renew_code):
                        Barcodetype_url='ean13'
                    else:
                        Barcodetype_url=None
                except:
                    Barcodetype_url=None
                






                for new_code in code_array_1:

                    try:
                        if barcodenumber.check_code('code39',new_code):
                            Barcodetype_name='code39'
                        elif barcodenumber.check_code('ean13',new_code):
                            Barcodetype_name='ean13'
                        else:
                            Barcodetype_name=None
                    except:
                        Barcodetype_name=None



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
                                ,renew_code
                                ,mult_cat[0]
                                ,mult_cat[1]
                                ,mult_cat[2]
                                ,mult_cat[3]
                                ,cur_url
                                ,Barcodetype_url
                                ,Barcodetype_name
                                )
                    

                    cur.execute(""" insert into temp_table values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
                    con.commit()
                

                    # Close the new page
                new_page.close()
                iterator+=1
                
                    

                        
            end = time.time()
            total=end-start
            print('category done,', 'clicked on ' ,iterator,' unique items from ', url)
            print('total time is ', total)
            print('time per item = ', total/iterator)
            page.close()

            try:
                shared_links.remove(url)
                print('removed', url)
            except:
                print('already removed', url)


            
        browser.close()  # Close the browser
        





    
    

if __name__ == "__main__":
    try:
        num_processes = 5
        manager = Manager()


        # Convert your global 'links' list to a list that can be shared between processes
        shared_links = manager.list(links)

        # Split the URLs into 10 separate chunks
        split_links = split_urls(shared_links, num_processes)

        # Create 10 separate processes
        processes = []
        for i in range(num_processes):
            p = Process(target=run, args=(split_links[i],shared_links))
            processes.append(p)
        
        # Start all the processes
        for p in processes:
            p.start()
        
        # Wait for all processes to complete
        for p in processes:
            p.join()


        shared_links=set(shared_links)
        with open('./rozetka/result_url.py','w') as file_write:
            file_write.write('links=[\n')
            for urls in shared_links:
                file_write.write("'"+urls + "',\n")
            file_write.write(']\n')



        print("All processes are complete.")
    except:
        f=open(getcwd()+'/rozetka/log.txt', 'a')
        f.write('----------------------------------------\n')
        f.write(format_exc())
        f.write('occurred on ' + str(datetime.now())+ '\n')
        f.write('----------------------------------------\n\n\n')
        f.close()