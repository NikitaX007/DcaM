from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from bs4 import BeautifulSoup
import csv

# Настройки WebDriver
options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

try:
    # Открытие сайта
    driver.get("https://book24.ru/catalog/business-1671/")

    books = []
    page_count = 0
    while page_count <= 10:
        wait = WebDriverWait(driver, 10)
        try:
            # Дожидаемся загрузки элементов на странице
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='product-card__name']")))
            # Заново получаем все элементы после каждой итерации цикла, чтобы избежать StaleElementReferenceException
            product_links = driver.find_elements(By.XPATH, "//a[@class='product-card__name']")
            for link in product_links:
                books.append(link.get_attribute('href'))
            page_count += 1
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'pagination__item') and contains(@class, '_next')]")))
                # Используем JavaScript для клика
                driver.execute_script("arguments[0].click();", next_button)
            except (ElementClickInterceptedException, TimeoutException):
                break
        except StaleElementReferenceException:
            # Если элемент устарел, обновляем список элементов
            continue

    # Открытие файла для записи данных
    with open("books.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Author", "Price", "About"])
        for url in books:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                # Парсинг данных о книге
                name = soup.find("h1", itemprop="name").get_text(strip=True)
                author = soup.find("a", class_="product-characteristic-link").get_text(strip=True)
                price = soup.find("span", class_="product-sidebar-price__price").get_text(strip=True)
                about = soup.find("div", class_="product-about__text").p.get_text(strip=True)
                writer.writerow([name, author, price, about])
            except AttributeError as e:
                print(f"Ошибка при извлечении данных книги: {e}")
finally:
    # Закрытие WebDriver
    driver.quit()

print("Скрейпинг завершен, данные сохранены в books.csv")