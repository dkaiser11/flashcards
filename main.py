import pathlib
import random
import os

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from data_models import *


def input_(prompt: str) -> str:
    input_read = input(prompt)
    if input_read == "q":
        quit()
    return input_read


def cls() -> None:
    os.system("cls")


BASE_URL = "https://www.kanjidamage.com/kanji/"
PATH = str(pathlib.Path().resolve()) + "\\cards.json"

with open(PATH, "r") as rdoc:
    try:
        data = Data(rdoc.read())
    except:
        with open(PATH, "w") as wdoc:
            wdoc.write(Data().to_json())


def update():
    with open(PATH, "w") as wdoc:
        wdoc.write(data.to_json())


def add():
    data.add()
    update()


def move(card: int, i: int, j: int) -> None:
    data.move(card, i, j)
    update()


options = Options()
options.add_argument("--log-level=3")

with WebDriver(options=options) as driver:
    def load(i: int = None, data_: Data = None) -> None:
        i = 0 if i == None else i

        data_ = Data(data.to_json()) if data_ == None else data_
        box_ = data_.boxes[i]
        cards_ = list(random.sample(box_.cards, len(box_.cards)))

        for card in cards_:
            learn(card, i)

    def load_all() -> None:
        data_ = Data(data.to_json())
        for i in range(len(data_.boxes)):
            if data_.learned % data_.boxes[i].repetition_time == 0:
                load(i, data_)

    def learn(card: int, i: int) -> None:
        cls()
        print(card)

        if card != 1:
            number = driver.find_element(
                By.XPATH, f"//td[contains(text(), '{card - 1}')]")
        number.location_once_scrolled_into_view

        input_("Hit any key when ready")
        cls()

        link = driver.find_element(
            By.XPATH, f"//td[contains(text(), '{card}')]").find_element(By.XPATH, "./..").find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.get(link)

        number = driver.find_element(
            By.XPATH, f"//a[contains(text(), 'Next')]")
        number.location_once_scrolled_into_view

        learned = input_("Did you know the answer? (y/n) \n")
        cls()

        options = {
            "": 1,
            "j": 1,
            "y": 1,
            "n": -1
        }

        move(card, i, i + options[learned])

        driver.get(BASE_URL)

    driver.get(BASE_URL)

    cls()

    mode = input_("What mode do you want to start in? (q to quit) \n")

    modes = {
        "a": [add],
        "al": [add, load],
        "l": [load],
        "lf": [load],
        "ala": [add, load_all],
        "la": [load_all],
        "": [load_all]
    }

    [func() for func in modes[mode]]

quit()
