import os
import logging
import pandas as pd
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Lấy thông tin từ người dùng
main_category = input("Nhập main_category: ")
sub_category = input("Nhập sub_category: ")
numberpage = int(input("Nhập số lượng trang cần cào: "))

# Cấu hình Selenium WebDriver với ChromeOptions
chrome_options = Options()
ua = UserAgent()
chrome_options.add_argument(f"user-agent={ua.random}")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--enable-unsafe-swiftshader")  # Cho phép SwiftShader xử lý WebGL

# Khởi tạo WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Danh sách lưu dữ liệu
data = []

# URL của Amazon
base_url = "https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A172456&ref=nav_em__nav_desktop_sa_intl_computer_accessories_and_peripherals_0_2_7_2"

# Hàm cào dữ liệu
def scrape_data():
    url = base_url
    for i in tqdm(range(1, numberpage + 1), desc="Crawling Amazon"):
        logging.info(f"Đang lấy dữ liệu trang {i}...")

        driver.get(url)

        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))
        except Exception as e:
            logging.error(f"Lỗi khi tải trang: {e}")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all('div', class_='s-result-item')

        if not products:
            logging.warning("Không tìm thấy sản phẩm nào! Có thể bị Amazon chặn.")
            break

        for item in products:
            # Lấy tên sản phẩm
            product = item.find('h2', class_="a-size-base-plus a-spacing-none a-color-base a-text-normal")
            name = product.text.strip() if product else None

            # Lấy link sản phẩm
            link = item.find('a', class_="a-link-normal s-no-outline")
            product_link = f"https://www.amazon.com{link.get('href')}" if link else None

            # Lấy giá
            price = item.find('span', class_="a-price-whole")
            price_text = price.text.strip() if price else None

            # Lấy rating
            rate = item.find('span', class_="a-icon-alt")
            rating = rate.text.split()[0] if rate else None

            # Lấy số lượng review
            review = item.find('span', class_="a-size-base s-underline-text")
            review_count = review.text.strip() if review else None

            # Chỉ thêm nếu sản phẩm có link (tránh bị trùng)
            if product_link and product_link not in [d['Link'] for d in data]:
                data.append({
                    'Product Name': name,
                    'Price': price_text,
                    'Rating': rating,
                    'Review': review_count,
                    'Link': product_link
                })

        # Tìm link chuyển sang trang tiếp theo
        next_page = soup.find('a', class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator")
        if next_page and "href" in next_page.attrs:
            url = f"https://www.amazon.com{next_page['href']}"
        else:
            logging.info("Không tìm thấy trang tiếp theo, dừng crawl.")
            break

    save_to_csv()

# Hàm lưu dữ liệu vào CSV
def save_to_csv():
    df = pd.DataFrame(data)

    folder_path = r'D:\LNTP ở HUST\Học tập\Năm 4\20242\ĐATN\Amazon - Data Source'
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'part1_data_{main_category}_{sub_category}.csv')
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

    logging.info(f"Dữ liệu đã lưu vào: {file_path}")

# Bắt đầu crawl
scrape_data()

# Đóng trình duyệt
driver.quit()
