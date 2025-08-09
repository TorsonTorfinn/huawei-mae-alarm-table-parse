from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

now_datetime = datetime.now()
today = now_datetime.strftime('%Y-%m-%d %H:%M:%S')
yesterday = (now_datetime - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')


env_path = load_dotenv(dotenv_path='.env')

nce_username = os.getenv('NCE_USERNAME')
nce_password = os.getenv('NCE_PASSWORD')
chrome_driver_path = os.getenv('chrome_driver')
nce_download_path = os.getenv('NCE_DOWNLOAD_FILE')
log_url = os.getenv('NCE_LOG_URL')
hist_alarms_url = os.getenv('NCE_HISTORICAL_ALARMS')

chrome_service = Service(chrome_driver_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-autofill')

chrome_options.add_experimental_option(
    'prefs',
    {
        'download.default_directory': nce_download_path,
        'download.prompt_for_download': False,
        'download:directory_upgrade': True,
        'safebrowsing.enabled': True
    }
)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    driver.get(log_url)

    username_field = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    username_field.send_keys(nce_username)
    time.sleep(1)
    password_field = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="value"]')))
    password_field.send_keys(nce_password)
    time.sleep(1)
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitDataverify"]'))).click()
    time.sleep(7)

    driver.get(hist_alarms_url)
    css_selector = '#smartQueryFilterTitle > span'

    try:
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        close_button.click()
        print("Кнопка закрытия нажата успешно.")
    except Exception as e:
        print(f"Не удалось нажать на кнопку: {e}")

    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fm_btn_shrink"]'))) # //*[@id="smartQueryFilterTitle"]/span
    time.sleep(3)
    driver.quit()
except Exception as e:
    print(f"Error end: {e}")



# Filter //*[@id="fm_btn_shrink"]