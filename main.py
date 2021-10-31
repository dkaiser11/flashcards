from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

with WebDriver() as driver:
    driver.get("https://www.kanjidamage.com/kanji/")
    WebDriverWait(driver, 1)
    driver.close()