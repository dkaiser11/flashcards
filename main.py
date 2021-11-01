from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import random
import json
import datetime

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


input_ = input()

with WebDriver() as driver:
    # load kanji list and remove hints
    def load_main():
        driver.get(BASE_URL)
        rows = driver.find_elements(By.TAG_NAME, 'tr')
        txts = [row.find_elements(By.TAG_NAME, 'td')[3] for row in rows]
        for txt in txts:
            driver.execute_script("""
            var txt = arguments[0];
            txt.parentNode.removeChild(txt);
            """, txt)

    # load kanji in box
    def load(box):
        load_main()
        for card in random.sample(box["cards"], len(box["cards"])):
            print(str(card))
            input()
            driver.get(BASE_URL + str(card))

            known = input()
            if known == "no" or known == "n":
                raise NotImplementedError
            else:
                raise NotImplementedError

    if input_ == "add":
        add()

    else:
        load(box(0))
