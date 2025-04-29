import csv
import datetime
import logging
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
ua = UserAgent()
user_agents = ua.random
def calculate_shipping_days(estimated_delivery_date_str, crawl_date_str):
    try:
        estimated_delivery_date = datetime.datetime.strptime(estimated_delivery_date_str, '%A, %B %d')
        crawl_date = datetime.datetime.strptime(crawl_date_str, '%A, %B %d')
        return (estimated_delivery_date - crawl_date).days
    except ValueError:
        return 'N/A'
def clean_text(text):
    return re.sub(r'[\u200e]', '', text)
def detailproduct_bucket(soup, divs2I):
    dimension = asinid = datefirstavailable = manufactures = country = sellerrank = color = modelnumber = weight = price = priceamzship = eic = shipping_days = 'None'
    divs3 = divs2I.findall('span', class='a-text-bold')
    for div in divs3:
        if 'Package Dimensions' in div.text.strip() or 'Dimensions' in div.text.strip():
            div4 = div.find_next_sibling('span')
            dimension = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Item model number' in div.text.strip():
            div4 = div.find_next_sibling('span')
            modelnumber = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Date First Available' in div.text.strip():
            div4 = div.find_next_sibling('span')
            datefirstavailable = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Manufacturer' in div.text.strip():
            div4 = div.find_next_sibling('span')
            manufactures = clean_text(div4.text.strip() if div4 else 'None')
        elif 'ASIN' in div.text.strip():
            div4 = div.find_next_sibling('span')
            asinid = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Country of Origin' in div.text.strip():
            div4 = div.find_next_sibling('span')
            country = clean_text(div4.text.strip() if div4 else 'None')
        elif 'Best Sellers Rank' in div.text.strip():
            parent_tag = div.parent
            sellerrank = clean_text(parent_tag.get_text(strip=True))
        elif 'Color' in div.text.strip():
            div4 = div.find_next_sibling('span')
            color = cleantext(div4.text.strip() if div4 else 'Not Given')
    divs2Ia = soup.find('div', class='a-popover-preload', id='a-popover-agShipMsgPopover')
    if (divs2Ia):
        table = divs2Ia.find('table', class_='a-lineitem')
        if (table):
            lines = table.findall('td', class='a-span9 a-text-left')
            for td in lines:
                if 'Price' in td.text:
                    divsprice = td.find_nextsibling('td', class='a-span2 a-text-right')
                    price = clean_text(divsprice.text.strip() if divsprice else 'None')
                if 'AmazonGlobal Shipping' in td.text:
                    divsamzship = td.find_nextsibling('td', class='a-span2 a-text-right')
                    priceamzship = clean_text(divsamzship.text.strip() if divsamzship else 'None')
                if 'Estimated Import Charges' in td.text:
                    diveic = td.find_nextsibling('td', class='a-span2 a-text-right')
                    eic = clean_text(diveic.text.strip() if diveic else 'None')
    estimated_delivery_datetag = soup.find('span', class='a-text-bold')
    estimated_delivery_date = clean_text(estimated_delivery_date_tag.text.strip() if estimated_delivery_date_tag else 'N/A')
    crawl_date = datetime.datetime.now().strftime('%A, %B %d')
    shipping_days = calculate_shipping_days(estimated_delivery_date, crawl_date)

    return {
        "Dimension": dimension,
        "ASIN": asinid,
        "Date First Available": datefirstavailable,
        "Manufacturer": manufactures,
        "Country of Origin": country,
        "Best Sellers Rank": sellerrank,
        "Color": color,
        "Item Model Number": modelnumber,
        "Item Weight": weight,
        "Price": price,
        "AmazonGlobal Shipping": priceamzship,
        "Estimated Import Charges": eic,
        "Day Delivered": str(shipping_days)
    }
def detailproduct_table(soup, divs2):
    dimension = asinid = datefirstavailable = manufactures = country = sellerrank = color = modelnumber = weight = price = priceamzship = eic = shipping_days = 'None'
    divs3 = divs2.findall('th', class='a-color-secondary a-size-base prodDetSectionEntry')
    for div in divs3:
        if 'Manufacturer' in div.text.strip():
            divs7 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            manufactures = clean_text(divs7.text.strip() if divs7 else 'None')
        if 'Dimensions' in div.text.strip():
            divs4 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            dimension = clean_text(divs4.text.strip() if divs4 else 'None')
        if 'ASIN' in div.text.strip():
            divs5 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            asinid = clean_text(divs5.text.strip() if divs5 else 'None')
        if 'Date First Available' in div.text.strip():
            divs6 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            datefirstavailable = clean_text(divs6.text.strip() if divs6 else 'None')
        if 'Country of Origin' in div.text.strip():
            divs8 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            country = clean_text(divs8.text.strip() if divs8 else 'None')
        if 'Best Sellers Rank' in div.text.strip():
            divs9 = div.find_next_sibling('td')
            sellerrank = clean_text(divs9.text.strip() if divs9 else 'None')
        if 'Color' in div.text.strip():
            divs10 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            color = clean_text(divs10.text.strip() if divs10 else 'Not Given')
        if 'Item model number' in div.text.strip():
            divs11 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            modelnumber = clean_text(divs11.text.strip() if divs11 else 'Not Given')
        if 'Item Weight' in div.text.strip():
            divs12 = div.find_nextsibling('td', class='a-size-base prodDetAttrValue')
            weight = clean_text(divs12.text.strip() if divs12 else 'Not Given')
        # Thông tin giá shipping
        try:
            # Tìm và click vào nút Details
            details_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.a-declarative [role='button']"))
            )
            driver.execute_script("arguments[0].click();", details_button)

            # Đợi cho bảng shipping hiện ra
            shipping_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-lineitem"))
            )

            # Parse thông tin từ bảng mới
            table_html = shipping_table.get_attribute('outerHTML')
            table_soup = BeautifulSoup(table_html, 'html.parser')
            rows = table_soup.find_all('tr')

            for row in rows:
                tdkey = row.find('td', class='a-span9 a-text-left')
                tdvalue = row.find('td', class='a-span2 a-text-right')

                if td_key and td_value:
                    key_span = tdkey.find('span', class='a-size-base a-color-secondary')
                    value_span = tdvalue.find('span', class='a-size-base a-color-base')

                    if key_span and value_span:
                        key_text = key_span.get_text(strip=True)
                        value_text = value_span.get_text(strip=True)

                        if 'Price' in key_text:
                            price = value_text
                        elif 'AmazonGlobal Shipping' in key_text:
                            priceamzship = value_text
                        elif 'Estimated Import Charges' in key_text:
                            eic = value_text

            logging.info(f"Successfully extracted shipping details: Price={price}, Shipping={priceamzship}, Import={eic}")

        except Exception as e:
            logging.warning(f"Could not extract shipping details: {str(e)}")
            price = priceamzship = eic = 'None'
    estimated_delivery_datetag = soup.find('span', class='a-text-bold')
    estimated_delivery_date = clean_text(estimated_delivery_date_tag.text.strip() if estimated_delivery_date_tag else 'N/A')
    crawl_date = datetime.datetime.now().strftime('%A, %B %d')
    shipping_days = calculate_shipping_days(estimated_delivery_date, crawl_date)

    return {
        "Dimension": dimension,
        "ASIN": asinid,
        "Date First Available": datefirstavailable,
        "Manufacturer": manufactures,
        "Country of Origin": country,
        "Best Sellers Rank": sellerrank,
        "Color": color,
        "Item Model Number": modelnumber,
        "Item Weight": weight,
        "Price": price,
        "AmazonGlobal Shipping": priceamzship,
        "Estimated Import Charges": eic,
        "Day Delivered": str(shipping_days)
    }
url_list = pd.read_csv(f'D:\\LNTP ở HUST\\Học tập\\Năm 4\\20242\\ĐATN\\Code\\Part 1\\part1_data_Automotive_Performance Parts & Accessories_20250314.csv')
results = []
retry_limit = 3  # Đặt giới hạn số lần thử lại
def create_driver(user_agent):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--log-level=3")
    return webdriver.Chrome(options=chrome_options)
# Khởi tạo driver đầu tiên
driver = create_driver(user_agents)
count = 0
for urldetail in url_list['Link']:
    count += 1
    retry_count = 0
    success = False
    driver = create_driver(user_agents)  # Khởi tạo driver mới với User-Agent mới

    print(f"Lần lấy thông tin thứ: {count} với User-Agent: {user_agents}")
    while retry_count < retry_limit and not success:
        try:
            driver.get(urldetail)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'prodDetails')) or 
                EC.presence_of_element_located((By.ID, 'detailBulletsWrapper_feature_div'))
            )
            success = True
        except TimeoutException:
            retry_count += 1
            print(f"Timeout while waiting for page to load: {urldetail}. Retrying {retry_count}/{retry_limit}")
            time.sleep(5)  # Chờ 5 giây trước khi thử lại
    if not success:
        print(f"Failed to load page after {retry_limit} attempts: {urldetail}")
        continue
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs2 = soup.find('div', id='prodDetails')
    divs2I = soup.find('div', id='detailBulletsWrapper_feature_div')
    if divs2:
        result = detailproduct_table(soup, divs2)
    elif divs2I:
        result = detailproduct_bucket(soup, divs2I)

    if result:
        results.append(result)

    print(result)
driver.quit()
filename = f"part2_dataDetail.csv"
with open(filename, 'a', newline="", encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=result.keys())
    csv_writer.writeheader()
    csv_writer.writerows(results)
print(f"Completed scraping and saved to {filename}.")