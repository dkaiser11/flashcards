from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import json

#load data
with open("cards.json", "r") as doc:
    data = json.loads(doc.read())

#update data
def update():
    #check for each card if it is still to learn or add
    for box in data["boxes"]:
        cards = list(box["cards"])
        for card in cards:
            if card > data["learned"]*10:
                box["cards"].remove(card)
    with open("cards.json", "w") as doc:
        doc.write(json.dumps(data))

def add():
    for card in range(10*(data["learned"] - 1) + 1, 10*data["learned"] + 1):
        data["boxes"][0]["cards"].append(card)

#add/remove kanji to learn
input = input()

if  input == "add":
    data["learned"] += 1
    add()
elif input == "rm":
    data["learned"] -= 1
    if data["learned"] < 0:
        data["learned"] = 0
update()

with WebDriver() as driver:
    driver.get("https://www.kanjidamage.com/kanji/")
    WebDriverWait(driver, 1)
    driver.close()