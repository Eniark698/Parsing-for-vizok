import json, re
import pandas as pd
import time
import random
import math
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from multiprocessing import Process, Lock
from datetime import date
from random import randint
import subprocess
import http.client as httplib


def have_internet() -> bool:
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


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
    split_dfs = [df.iloc[i * avg : (i + 1) * avg] for i in range(num_splits)]
    return split_dfs


def del_uah(price):
    match = re.search(r"([\d\s,]+)", price)
    if match:
        number_str = (
            match.group(1).replace(" ", "").replace(",", ".").replace("\xa0", "")
        )
        number_float = float(number_str)
    else:
        number_float = None
    return number_float


def del_deliver(price):
    a = price.find(":")
    b = price.find("грн")
    try:
        if a == -1 or b == -1:
            price = 0
        else:
            price = float(price[a + 1 : b - 1].replace(" ", "").replace(",", "."))
            if price == None:
                price = 0
    except:
        price = 0
    return price


def request_scrap(param_item, user_dir, i1, lock):
    with sync_playwright() as p:
        with lock:
            time.sleep(5)

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        ]

        # params = {
        #     "q": param_item,
        #     "hl": "uk",     # language
        #     "gl": "ua",     # country of the search, US -> USA
        #     "tbm": "shop",   # google search shopping tab
        # }

        # proxy={"server": f'socks5://10.0.100.12:9050'}
        browser = p.firefox.launch_persistent_context(
            user_dir,
            headless=True,
            base_url="https://www.google.com",
            viewport={"width": 1280, "height": 920},
            user_agent=random.choice(user_agents),
            permissions=["geolocation"],
            geolocation={"latitude": 49.842957, "longitude": 24.031111},
            locale="uk-UA",
            timezone_id="Europe/Kyiv",
        )
        page = browser.pages[0]
        stealth_sync(page)
        try:
            page.goto("https://www.google.com", wait_until="domcontentloaded")
            time.sleep(random.uniform(1.5, 5.9))
            page.click('textarea[name="q"]')
            time.sleep(random.uniform(1.5, 3.9))
            page.type('textarea[name="q"]', param_item)
            page.keyboard.press("Enter")
            time.sleep(random.uniform(1.5, 2.9))

            # Click the "Shopping" tab
            page.click("text=Покупки")
            time.sleep(random.uniform(1.5, 4.9))
        except:
            page.screenshot(path=f"./screenshot_{i1}.png")

        def get_suggested_search_data():
            google_shopping_data = []

            for result in page.query_selector_all(".Qlx7of .i0X6df"):
                title = extract_text(result, ".tAxDx")

                product_link = "https://www.google.com" + result.query_selector(
                    ".Lq5OHe"
                ).get_attribute("href")
                product_rating = extract_text(result, ".NzUzee .Rsc7Yb")
                product_reviews = extract_text(result, ".NzUzee > div")
                price = extract_text(result, ".a8Pemb")
                old_price = extract_text(result, ".zY3Xhe")
                old_price1 = extract_text(result, ".nSfGAb")
                store = extract_text(result, ".aULzUe")
                try:
                    store_link_element = result.query_selector(".eaGTj div a")
                except:
                    store_link_element = None
                store_link = (
                    "https://www.google.com" + store_link_element.get_attribute("href")
                    if store_link_element
                    else None
                )
                delivery = extract_text(result, ".vEjMR")
                try:
                    compare_prices_link_value = result.query_selector(
                        ".Ldx8hd .iXEZD"
                    ).get_attribute("href")
                except:
                    compare_prices_link_value = None

                compare_prices_link = (
                    "https://www.google.com" + compare_prices_link_value
                    if compare_prices_link_value
                    else compare_prices_link_value
                )

                google_shopping_data.append(
                    {
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
                    }
                )
            return json.dumps(google_shopping_data, indent=2, ensure_ascii=False)

        data = []
        while True:
            page.wait_for_load_state("load")
            temp = json.loads(get_suggested_search_data())

            data.extend(temp)

            try:
                page.keyboard.press("End")
                page.click("a#pnnext", timeout=10000)
            except:
                break

        browser.close()

        return data


def run(df, user_dir, i, lock):
    import sqlite3

    con = sqlite3.connect("./google_shop/temp_name.db")
    cur = con.cursor()
    today = date.today()

    for index, row in df.iterrows():
        large_str = request_scrap(row["name"], user_dir, i, lock)

        for product in large_str:
            SearchInfoName = row["name"].strip()

            SearchInfoCode = None
            SearchInfoCode = str(row["code"]).strip()

            try:
                Name = product["title"].strip()
            except:
                Name = None

            try:
                Seller = product["store"].strip()
            except:
                Seller = None

            try:
                ItemOnStoreUrl = product["store_link"].strip()
            except:
                ItemOnStoreUrl = None

            try:
                ItemOnGoogleShopUrl = product["product_link"].strip()
            except:
                ItemOnGoogleShopUrl = None

            try:
                Price = del_uah(product["price"])
            except:
                Price = None

            try:
                OldPrice = del_uah(product["old_price"])
            except:
                try:
                    temp = re.findall(r"[\d,.]+", product["old_price1"])
                    OldPrice = float(temp[0].replace(",", "."))
                except:
                    OldPrice = None

            try:
                DeliveryPrice = del_deliver(product["delivery"])
            except:
                DeliveryPrice = None

            try:
                DeliveryInfo = product["delivery"].strip()
            except:
                DeliveryInfo = None

            try:
                ProductRating = float(
                    product["product_rating"].strip().replace(",", ".")
                )
            except:
                ProductRating = None

            try:
                ComparePricesLink = product["compare_prices_link"].strip()
            except:
                ComparePricesLink = None

            data = (
                today,
                SearchInfoName,
                SearchInfoCode,
                Name,
                Seller,
                ItemOnStoreUrl,
                ItemOnGoogleShopUrl,
                Price,
                OldPrice,
                DeliveryPrice,
                DeliveryInfo,
                ProductRating,
                ComparePricesLink,
            )

            cur.execute(
                """ insert into temp_table values (?,?,?,?,?,?,?,?,?,?,?,?,?)""", data
            )

            con.commit()


def main(logging, num_processes=1):
    import sqlite3

    con = sqlite3.connect("./google_shop/temp_name.db")
    # con.isolation_level=None
    cur = con.cursor()

    cur.execute(
        """create table if not exists temp_table(
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
                        """
    )

    con.commit()
    cur.execute("""delete from  temp_table;""")

    con.commit()

    lock = Lock()

    user_dirs = [f"./user_dir_{i+1}/" for i in range(num_processes)]

    dataframe = pd.read_excel("./google_shop/file_temp.xlsx", dtype=str)

    if len(dataframe) < num_processes:
        num_processes = 1
    user_dirs = [f"./user_dir_{i+1}/" for i in range(num_processes)]

    dataframe = dataframe.sample(frac=1, random_state=None)

    split_df = split_dataframe(dataframe, num_processes)
    lock.acquire()

    # Create 10 separate processes
    threads = []
    for i in range(num_processes):
        t = Process(
            target=run,
            args=(
                split_df[i],
                user_dirs[i],
                i,
                lock,
            ),
        )
        threads.append(t)

    # Start all the processes
    for t in threads:
        t.start()

    while True:
        if lock:
            pass
        else:
            lock.acquire()
        time.sleep(10)

        while True:
            try:
                vpn_process.terminate()
                vpn_process.wait()
            except:
                pass

            vpn_process = subprocess.Popen(
                [
                    "openvpn",
                    "--config",
                    f"ovpn_udp/ua{randint(51,64)}.nordvpn.com.udp.ovpn",
                    "--auth-user-pass",
                    "temp_cred.txt",
                ]
            )

            time.sleep(10)
            if have_internet() == True:
                break

        if lock:
            lock.release()

        time.sleep(300)
        check_list_to_complite = [0 for i in range(num_processes)]
        for i, proc in enumerate(threads):
            if proc.is_alive():
                check_list_to_complite[i] = 1
            else:
                pass
        if not (any(check_list_to_complite)):
            break
    # Wait for all processes to complete
    for t in threads:
        t.join()

    vpn_process.terminate()

    vpn_process.wait()

    pattern = "openvpn --config ovpn_udp/ua[5-7][0-9].nordvpn.com.udp.ovpn --auth-user-pass temp_cred.txt"
    kill_command = ["pkill", "-9", "-f", pattern]
    result = subprocess.run(
        kill_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # Check the return code to determine if the kill command was successful
    if result.returncode == 0:
        pass
    elif result.returncode == 1:
        pass
    else:
        logging.critical(
            f"An error occurred while trying to kill the process: {result.stderr.decode().strip()}"
        )

    logging.info({'SUCCESS':"parse part done"})

