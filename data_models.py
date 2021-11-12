import json


class Data:
    def __init__(self, json_: str = None) -> None:
        if json_ == None:
            self.learned = 0
            self.boxes = [Box(i) for i in [1, 3, 7, 30, 100, 1000]]
        else:
            json_ = json.loads(json_)
            self.learned = json_["learned"]
            self.boxes = [Box(box["repetition_time"], box["cards"])
                          for box in json_["boxes"]]

    def to_json(self) -> str:
        return json.dumps({"learned": self.learned, "boxes": [
            {"repetition_time": box.repetition_time, "cards": box.cards} for box in self.boxes]})

    def add(self) -> None:
        self.learned += 1
        for i in range(10*(self.learned - 1) + 1, 10*self.learned + 1):
            self.boxes[0].cards.append(i)

    def move(self, card: int, i: int, j: int) -> None:
        i = 0 if i < 0 else i
        i = len(self.boxes) - 1 if i > len(self.boxes) - 1 else i
        j = 0 if j < 0 else j
        j = len(self.boxes) - 1 if j > len(self.boxes) - 1 else j

        self.boxes[i].cards.remove(card)
        self.boxes[j].cards.append(card)

    def new(self):
        new = range(10*(self.learned - 1) + 1, 10*self.learned + 1)
        data_ = Data()
        data_.learned = self.learned
        for i, box in enumerate(self.boxes):
            data_.boxes[i].repetition_time = 1
            for card in box.cards:
                if card in new:
                    data_.boxes[i].cards.append(card)
        return data_


class Box:
    def __init__(self, repetition_time: int, cards: list = None) -> None:
        self.repetition_time = int(repetition_time)
        self.cards = [] if cards == None else cards
