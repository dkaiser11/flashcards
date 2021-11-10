import datetime
import json
import random
import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from data_models import Data

BASE_URL = "https://www.kanjidamage.com/kanji/"
PATH = "cards.json"

# load data
with open(PATH, "r") as rdoc:
    try:
        data = Data(json.loads(rdoc.read()))
    except:
        with open(PATH, "w") as wdoc:
            wdoc.write(Data().to_json())


def update():
    with open(PATH, "w") as wdoc:
        wdoc.write(data.to_json())


def add():
    data.learned += 1
    [data.boxes[0].append(i) for i in range(
        10*(data.learned - 1) + 1, 10*data.learned + 1)]
    update()


options = Options()
options.add_argument("--log-level=3")

with WebDriver(options=options) as driver:

    driver.get(BASE_URL)

    number = driver.find_element(
        By.XPATH, f"//td[contains(text(), '{card if card == 1 else card - 1}')]")
    number.location_once_scrolled_into_view

    os.system("cls")
    driver.get(BASE_URL + str(card))

    number = driver.find_element(
        By.XPATH, f"//a[contains(text(), 'Next')]")
    number.location_once_scrolled_into_view
