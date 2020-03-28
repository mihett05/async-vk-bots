import json


class Color:
    Positive = "positive"
    Negative = "negative"
    Primary = "primary"
    Secondary = "secondary"


class KeyBoardMaker:
    def __init__(self, one_time=True, inline=False):
        if inline:
            self.config = {
                "buttons": [],
                "inline": True
            }
        else:
            self.config = {
                "one_time": one_time,
                "buttons": []
            }
        self.row = []

    def add_row(self):
        self.config["buttons"].append(self.row.copy())
        self.row.clear()
        return self

    def add_button(self, text: str, color: str, payload: str):
        self.row.append({
            "action": {
                "type": "text",
                "label": text,
                "payload": payload
            },
            "color": color
        })
        return self

    def add_link(self, label: str, link: str, payload: dict = None):
        self.row.append({
            "action": {
                "type": "open_link",
                "label": label,
                "link": link,
                "payload": payload if payload else json.dumps({"button": "0"})
            }
        })
        return self

    def generate(self):
        self.add_row()
        return json.dumps(self.config)
