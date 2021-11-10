class Data:
    def __init__(self, json: dict = None) -> None:
        if json == None:
            self.learned = 0
            self.boxes = [Box(i) for i in [1, 3, 7, 30, 100, 1000]]
        else:
            self.learned = json["learned"]
            self.boxes = [Box(box) for box in json["boxes"]]

    def to_json(self) -> dict:
        return {"learned": self.learned, "boxes": [
            {"repetition_time": box.repetition_time, "cards": box.cards} for box in self.boxes]}


class Box:
    def __init__(self, box: dict) -> None:
        self.repetition_time = int(box["repetition_time"])
        self.cards = list(box["cards"])

    def __init__(self, repetition_time: int) -> None:
        self.repetition_time = repetition_time
