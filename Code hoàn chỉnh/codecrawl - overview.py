from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Cấu hình trình duyệt
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy ẩn danh
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Khởi tạo WebDriver
service = Service("chromedriver")  # Đường dẫn đến chromedriver
browser = webdriver.Chrome(options=chrome_options)

url = "https://www.amazon.com/ref=nav_logo"
browser.get(url)
time.sleep(10)  # Đợi trang tải

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")

# Lấy tất cả các menu từ data-menu-id="6" đến data-menu-id="27"
categories = []
for menu_id in range(6, 28):
    menu = soup.find("ul", {"class": "hmenu hmenu-translateX-right", "data-menu-id": str(menu_id)})
    if menu:
        department = menu.find_previous("a", {"class": "hmenu-item"})
        department_name = department.text.strip() if department else "Unknown"
        
        for sub in menu.find_all("a", {"class": "hmenu-item"}):
            sub_department = sub.text.strip()
            sub_url = sub.get("href", "")
            if sub_url and sub_department:
                full_url = "https://www.amazon.com" + sub_url if sub_url.startswith("/") else sub_url
                categories.append([department_name, sub_department, full_url])

browser.quit()

# Lưu vào CSV
with open("amazon_categories.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["department", "sub_department", "url department"])
    writer.writerows(categories)

print("Dữ liệu đã được lưu vào amazon_categories.csv")
