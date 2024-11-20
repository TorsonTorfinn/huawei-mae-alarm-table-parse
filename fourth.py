from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

username = os.getenv('USERNAME_MAE')
password = os.getenv('PASSWORD_MAE')
chrome_driver_env = os.getenv('chrome_driver')
download_path_env = os.getenv('file_download_path')
url_env = os.getenv('url')
url_contains_env= os.getenv('url_contains')


# Указываем путь к ChromeDriver
chrome_service = Service(chrome_driver_env)


# Настраиваем ChromeOptions для игнорирования ошибок SSL
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-autofill')

chrome_options.add_experimental_option(
    'prefs',
    {
        'download.default_directory': download_path_env,
        'download.prompt_for_download': False,
        'download:directory_upgrade': True,
        'safebrowsing.enabled': True
    }
)

# Создаем объект WebDriver с опциями
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # Переход на сайт
    driver.get(url_env)

    username_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    username_field.send_keys(username)

    # Ввод пароля
    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="value"]')))
    password_field.send_keys(password)

    # Нажатие на кнопку "Log In"
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="submitDataverify"]'))
    ).click()

    # Ожидание загрузки страницы после авторизации
    WebDriverWait(driver, 20).until(EC.url_contains(url_contains_env))


    iframe = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    # Нахождение и клик на кнопку Export
    # time.sleep(10)
    export_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="exportBtn"]/button'))
    )
    export_button.click()

    # Выбор "All" в выпадающем меню
    all_option = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "allExport"))
    )
    all_option.click()

    # выбор экзель файла
    excel_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="eui_radio_group_10000_radio_1"]/div/span[1]'))
    )
    excel_option.click()

    # ok BTNNNNN
    ok_excel_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmBtn"]'))
    )
    ok_excel_btn.click()

    # Ожидание завершения экспорта
    time.sleep(27)

finally:
    driver.quit()