import datetime
import json
import random

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

BASE_URL = "https://www.kanjidamage.com/kanji/"

# load data
with open("cards.json", "r") as doc:
    data = json.loads(doc.read())


# update data
def update():
    with open("cards.json", "w") as doc:
        doc.write(json.dumps(data))


# add one set of cards
def add():
    data["learned"] += 1
    for card in range(10*(data["learned"] - 1) + 1, 10*data["learned"] + 1):
        data["boxes"][0]["cards"].append(card)
    update()


def box(i: int):
    return data["boxes"][i]


# moves card from box i to box j
def move(card: int, i: int, j: int):
    # normalize indeces
    if i < 0:
        i = 0
    elif j < 0:
        j = 0
    elif i >= len(data["boxes"]):
        i = len(data["boxes"]) - 1
    elif j >= len(data["boxes"]):
        j = len(data["boxes"]) - 1

    # move card
    box(i)["cards"].remove(card)
    box(j)["cards"].append(card)

    update()


input_ = input()

with WebDriver() as driver:
    # load kanji list
    def load_main():
        driver.get(BASE_URL)

    # load kanji in box
    def load(i):
        box_ = box(i)

        for card in random.sample(box_["cards"], len(box_["cards"])):
            load_main()
            number = driver.find_element(
                By.XPATH, f"//td[contains(text(), '{card}')]")
            number.location_once_scrolled_into_view
            print(str(card))
            input()
            driver.get(BASE_URL + str(card))

            # sort cards by if they were learned
            known = input()
            if known == "no" or known == "n":
                move(card, i, i - 1)
            else:
                move(card, i, i + 1)

    if input_ == "add":
        add()
        for i in range(len(data["boxes"]) - 1, -1, -1):
            day = int(datetime.datetime.now().strftime("%j"))
            if day % box(i)["repetition_time"] == 0:
                load(i)
    else:
        load(0)
