import sys
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import os
import time
import datetime
import csv
from xlsxwriter import Workbook

columns = [
    "Icon URL",
    "Title",
    "Long Description",
    "ListingName",
    "Listing URL",
    "ListingScrapeDate",
    "ListingRank",
    "ListingSellerName",
]
web_url = "https://www.accelo.com/integrations"
url_prefix = ""
website_name = "Accelo"
WAIT_TIME = 2
HEADLESS_MODE = True


def save_csv(data, filepath, columns):
    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)

def save_excel(data, filepath, columns):
    with Workbook(filepath) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write_row(row=0, col=0, data=columns)
        for index, item in enumerate(data):
            row = map(lambda x: item.get(x, ""), columns)
            worksheet.write_row(row=index + 1, col=0, data=row)


def today(fmt:str="%Y-%m-%d")->str:
    dt = datetime.datetime.now()
    return dt.strftime(fmt)


def accelo_scrape(output_dir="./output", log_dir="./logs"):
    parent_dir = os.path.abspath("/home/ec2-user/scraping")
    if log_dir is None:
        log_dir = os.path.join(parent_dir, 'log')
    if output_dir is None:
        output_dir = os.path.join(parent_dir, 'output')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    logging.basicConfig(filename=f"{log_dir}/{website_name}.log", level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
    
    webdriver_service = Service('D:\\chromedriver-win64\\chromedriver.exe') # replace with your chromedriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    dt = today()

    driver = Chrome(service=webdriver_service, options=chrome_options)
    driver.get(web_url)
    time.sleep(2)
    items = driver.find_elements(By.XPATH, "//div[@class='flex-4col-centered__item w-dyn-item']")
    result = []
    rank = 1
    for item in items:
        icon_url = item.find_element(By.XPATH, ".//img[@class='card__icon is--xxl']").get_attribute("src")
        name = item.find_element(By.XPATH, './/h2[@fs-cmsfilter-field="title"]').text
        long_description = item.find_element(By.XPATH, './/div[@fs-cmsfilter-field="desc"]').text
        listing_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        row = {
            "Icon URL": icon_url,
            "Title": name,
            "Long Description": long_description,
            "ListingName": name,
            "Listing URL": web_url+str(listing_url),
            "ListingScrapeDate": dt,
            "ListingRank": f"main-{rank}",
            "ListingSellerName": "",
        }
        logging.debug(row)
        result.append(row)
        rank+=1
    save_excel(result, os.path.join(output_dir, f"{website_name}{today('%Y%m%d%H%M%S')}.xlsx"), columns)

if __name__ == "__main__":
    '''
    sys.argv[1]: output_path
    sys.argv[2]: log_path
    '''
    if len(sys.argv) == 3:
        accelo_scrape(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        accelo_scrape(sys.argv[1])
    else:
        accelo_scrape()
    logging.info("scraping done")

