import json
from .APIError import APIError


class Color:
    Positive = "positive"
    Negative = "negative"
    Primary = "primary"
    Secondary = "secondary"


class KeyBoardMaker:
    def __init__(self, one_time=True, inline=False, bot=None):
        self.bot = bot
        self.__callbacks = dict()
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

    def bind(self, bot):
        self.bot = bot

    def callback(self, label, color, payload):
        def decorator(func):
            self.__callbacks[payload] = func
            return self
        payload = json.dumps(payload) if isinstance(payload, dict) else str(payload)
        if len(payload) > 255:
            raise APIError("Max length of payload is 255 symbols")
        self.row.append({
            "color": color,
            "action": {
                "type": "callback",
                "payload": payload,
                "label": label
            }
        })
        return decorator

    def generate(self, bot=None):
        if not self.bot:
            self.bot = bot
        if len(self.__callbacks) > 0 and not self.bot:
            raise Exception("Can't generate callbacks without providing bot")
        for callback in self.__callbacks:
            self.bot.event(callback)(self.__callbacks[callback])
        self.add_row()
        return json.dumps(self.config)
