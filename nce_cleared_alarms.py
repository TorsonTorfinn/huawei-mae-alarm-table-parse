import logging
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#configures logging for detailed step tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# defines the current date and yesterday's date for filtering purposes
now_datetime = datetime.now()
yesterday_date = now_datetime - timedelta(days=1)
start_of_yesterday = datetime.combine(yesterday_date, time.min)
end_of_yesterday = datetime.combine(yesterday_date, time.max)
start_of_yesterday_str = start_of_yesterday.strftime('%Y-%m-%d %H:%M:%S')
end_of_yesterday_str = end_of_yesterday.strftime('%Y-%m-%d %H:%M:%S')

# loads environment variables from a .env file
load_dotenv(dotenv_path='.env')

# retrieves configuration from environment variables
USERNAME = os.getenv('NCE_USERNAME')
PASSWORD = os.getenv('NCE_PASSWORD')
DRIVER_PATH = os.getenv('chrome_driver')
DOWNLOAD_PATH = os.getenv('NCE_DOWNLOAD_FILE')
NCE_LOG_URL = os.getenv('NCE_LOG_URL')
NCE_HISTORICAL_ALARMS = os.getenv('NCE_HISTORICAL_ALARMS')
CSS_SELECTOR_FILTER = os.getenv('CSS_SELECTOR_FILTER')
CLEARED_ON_SELECTOR = os.getenv('CLEARED_ON_SELECTOR')
FROM_DATE = os.getenv('FROM_DATE')
FROM_DATE_CONFIRM_BTN = os.getenv('FROM_DATE_CONFIRM_BTN')
TO_DATE = os.getenv('TO_DATE')
TO_DATE_CONFIRM_BTN = os.getenv('TO_DATE_CONFIRM_BTN')
OK_DATE_BTN = os.getenv('OK_DATE_BTN')
OK_FILTER_BTN = os.getenv('OK_FILTER_BTN')
EXPORT_BTN = os.getenv('EXPORT_BTN')
EXPORT_ALL_BTN = os.getenv('EXPORT_ALL_BTN')
EXP_FIELDS_RADIO = os.getenv('EXP_FIELDS_RADIO')
FILE_FORMAT_RADIO = os.getenv('FILE_FORMAT_RADIO')
EXPORT_CONFIRM_BTN = os.getenv('EXPORT_CONFIRM_BTN')
FORMAT_RADIO_XPATH = os.getenv('FORMAT_RADIO_XPATH')

#configures Chrome options for Selenium execution
chrome_service = Service(DRIVER_PATH)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-autofill')

chrome_options.add_experimental_option(
    'prefs',
    {
        'download.default_directory': DOWNLOAD_PATH,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    }
)

import time
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    logger.info("The script starts and navigates to the login URL...")
    driver.get(NCE_LOG_URL)

    logger.info("The script waits for and enters the username...")
    username_field = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    username_field.send_keys(USERNAME)
    time.sleep(1)

    logger.info("The script waits for and enters the password...")
    password_field = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="value"]')))
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    logger.info("The script waits for and clicks the submit button...")
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitDataverify"]'))).click()
    time.sleep(10)

    logger.info("The script navigates to the historical alarms URL...")
    driver.get(NCE_HISTORICAL_ALARMS)
    time.sleep(20)

    logger.info("The script waits for and clicks the Filter button...")
    filter_span = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_FILTER)))
    filter_span.click()

    logger.info("The script waits for and selects the 'Cleared On' option...")
    cleared_span = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CLEARED_ON_SELECTOR)))
    cleared_span.click()

    logger.info("The script waits for and enters the start date...")
    from_date_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, FROM_DATE)))
    from_date_field.send_keys(start_of_yesterday_str)
    time.sleep(1)

    logger.info("The script waits for and confirms the start date...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, FROM_DATE_CONFIRM_BTN))).click()
    time.sleep(1)

    logger.info("The script waits for and enters the end date...")
    to_date_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, TO_DATE)))
    to_date_field.send_keys(end_of_yesterday_str)
    time.sleep(1)

    logger.info("The script waits for and confirms the end date...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, TO_DATE_CONFIRM_BTN))).click()
    time.sleep(1)

    logger.info("The script waits for and clicks 'OK' for the date range...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, OK_DATE_BTN))).click()

    logger.info("The script waits for and applies the filter...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, OK_FILTER_BTN))).click()
    time.sleep(12)

    logger.info("The script waits for and initiates the export process...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, EXPORT_BTN))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, EXPORT_ALL_BTN))).click()
    time.sleep(2)

    logger.info("The script waits for and selects the file format radio...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, FORMAT_RADIO_XPATH))).click()
    time.sleep(2)

    logger.info("The script waits for and confirms the export...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, EXPORT_CONFIRM_BTN))).click()
    time.sleep(180)

    logger.info("The script successfully downloads the file...")
    logger.info('File Successfully Downloaded')

except Exception as e:
    logger.error(f"The script encountered an error: {e}")
    logger.error(f"Exception details captured: {e}")

finally:
    logger.info("The script prepares to close the browser...")
    time.sleep(5)
    driver.quit()






























    
# from dotenv import load_dotenv
# import os
# from datetime import datetime, timedelta, time
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

# from datetime import datetime, timedelta, time
# now_datetime = datetime.now()
# yesterday_date = now_datetime - timedelta(days=1)
# start_of_yesterday = datetime.combine(yesterday_date, time.min)
# end_of_yesterday = datetime.combine(yesterday_date, time.max)
# start_of_yesterday_str = start_of_yesterday.strftime('%Y-%m-%d %H:%M:%S')
# end_of_yesterday_str = end_of_yesterday.strftime('%Y-%m-%d %H:%M:%S')

# env_path = load_dotenv(dotenv_path='.env')

# nce_username = os.getenv('NCE_USERNAME')
# nce_password = os.getenv('NCE_PASSWORD')
# chrome_driver_path = os.getenv('chrome_driver')
# nce_download_path = os.getenv('NCE_DOWNLOAD_FILE')
# log_url = os.getenv('NCE_LOG_URL')
# hist_alarms_url = os.getenv('NCE_HISTORICAL_ALARMS')

# chrome_service = Service(chrome_driver_path)
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--ignore-ssl-errors')
# chrome_options.add_argument('--disable-autofill')

# chrome_options.add_experimental_option(
#     'prefs',
#     {
#         'download.default_directory': nce_download_path,
#         'download.prompt_for_download': False,
#         'download:directory_upgrade': True,
#         'safebrowsing.enabled': True
#     }
# )

# import time
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# try:
#     driver.get(log_url)

#     username_field = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
#     username_field.send_keys(nce_username)
#     time.sleep(1)
#     password_field = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="value"]')))
#     password_field.send_keys(nce_password)
#     time.sleep(1)
#     WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitDataverify"]'))).click()
#     time.sleep(10)

#     driver.get(hist_alarms_url)
#     css_selector_filter = '#smartQueryFilterTitle > span'
#     cleared_on_selector = '#conditionPanelContainer > div:nth-child(5) > div.conditionRowContent.fm_inline_block.hide_split > div > div.fm_adv_pop_wind_container > div:nth-child(13)'

#     from_date = '#eui_col_10001 > div > input'
#     from_date_confirm_btn = '#topWindow > div:nth-child(46) > div > div > div.eui-datetime-picker-footer > div.eui-datetime-picker-footer-right > button'
#     to_date = '#eui_col_10003 > div > input'
#     to_date_confirm_btn = '#topWindow > div:nth-child(48) > div > div > div.eui-datetime-picker-footer > div.eui-datetime-picker-footer-right > button'

#     ok_date_btn = '#dialog_panel > div.eui_Dialog_ButtonArea > button.eui-btn.eui-btn-primary.eui-btn-normal'
#     ok_filter_btn = '#fm_btn_filter'

#     export_btn = '#exportBtn > button > span'
#     export_all_btn = '#allExport'
#     exp_fields_radio = '#eui_radio_group_10007_radio_1'
#     file_format_radio = '#eui_radio_group_10010_radio_1 > div > span:nth-child(2)'
#     export_confirm_btn = '#confirmBtn'

#     time.sleep(10)

#     try:
#         filter_span = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector_filter)))
#         filter_span.click()

#         cleared_span = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cleared_on_selector)))
#         cleared_span.click()
#         from_date_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, from_date)))
#         from_date_field.send_keys(start_of_yesterday_str)
#         time.sleep(1)
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, from_date_confirm_btn))).click()
#         time.sleep(1)
#         to_date_filed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, to_date)))
#         to_date_filed.send_keys(end_of_yesterday_str)
#         time.sleep(1)
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, to_date_confirm_btn))).click()
#         time.sleep(1)

#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ok_date_btn))).click()
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ok_filter_btn))).click()
#         time.sleep(12)

#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, export_btn))).click()
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, export_all_btn))).click()
#         time.sleep(2)
#         # No need WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, exp_fields_radio))).click() # Export Fields Displayed||All Columns
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="eui_radio_group_10002_radio_1"]/div/span[2]'))).click() # CSV || XLSX || HTML extensions
#         time.sleep(2)
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, export_confirm_btn))).click()  # 
#         time.sleep(180)
#         print('File Successfuly Downloaded')
#     except Exception as e:
#         print(f"Ne удалось нажать на кнопку: {e}")

#     time.sleep(5)
#     driver.quit()
# except Exception as e:
#     print(f"Error end: {e}")
#     print(f"Exception indeed captured as problem: {e}")
