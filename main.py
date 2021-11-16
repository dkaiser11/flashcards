import os
import pathlib
import random
from copy import deepcopy
from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from data_models import Data


def input_(prompt: str) -> str:
    input_read = input(prompt)
    if input_read == "q":
        quit()
    return input_read


def cls() -> None:
    os.system("cls")


BASE_URL = "https://www.kanjidamage.com/kanji/"
PATH = str(pathlib.Path().resolve()) + "\\cards.json"

try:
    with open(PATH, "r") as rdoc:
        data = Data(rdoc.read())
except Exception:
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
    def load(i: int = None, data_: Data = None, move_: bool = True) -> None:
        i = 0 if i == None else i

        data_ = deepcopy(data) if data_ == None else data_
        box_ = data_.boxes[i]
        cards_ = random.sample(box_.cards, len(box_.cards))

        for card in cards_:
            learn(card, i, move_)

    def load_new() -> None:
        load_all(data.new(), False)

    def load_session(data_: Data = None, move_: bool = True) -> None:
        if data_ == None:
            data_ = deepcopy(data)

        for i in range(len(data_.boxes)):
            if data_.learned % data_.boxes[i].repetition_time == 0:
                load(i, data_, move_)

    def load_all(data_: Data = None, move_: bool = True):
        if data_ == None:
            data_ = deepcopy(data)

        for i in range(len(data_.boxes)):
            load(i, data_, move_)

    def learn(card: int, i: int, move_: bool = True) -> None:
        cls()
        print(card)

        txt = driver.find_element(
            By.XPATH, f"//tr/td[1][contains(text(), '{card}')]/../*[4]")

        driver.execute_script("""
            var txt = arguments[0];
            txt.parentNode.removeChild(txt);
            """, txt)

        if card != 1:
            number = driver.find_element(
                By.XPATH, f"//tr/td[1][contains(text(), '{card - 1}')]")
            number.location_once_scrolled_into_view

        input_("Hit any key when ready")
        cls()

        link = driver.find_element(
            By.XPATH, f"//tr/td[1][contains(text(), '{card}')]/../td/a").get_attribute("href")
        driver.get(link)

        next_ = driver.find_element(
            By.XPATH, f"//a[contains(text(), 'Next')]")
        next_.location_once_scrolled_into_view

        learned = input_("Did you know the answer? (y/n) \n")
        cls()

        options = {
            "": 1,
            "j": 1,
            "y": 1,
            "n": -1
        }

        if move_:
            move(card, i, i + options[learned])

        driver.get(BASE_URL)

    while True:
        driver.get(BASE_URL)

        cls()

        mode = input_(
            f"What mode do you want to start in? ({len(data.boxes[0].cards)} in first box) \n(a: add, l: load session, n: load new (no progress), la: load all, q: quit) \n")

        modes = {
            "a": [add],
            "al": [add, load_session],
            "an": [add, load_new],
            "": [load_session],
            "l": [load_session],
            "n": [load_new],
            "la": [load_all]
        }

        try:
            [func() for func in modes[mode]]
        except Exception:
            cls()
            print("Please use a valid input")
            sleep(1)
