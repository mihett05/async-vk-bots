import json


class CarouselMaker:
    def __init__(self):
        self.template = {
            "type": "carousel",
            "elements": []
        }

    def add_element(self, title: str, description: str, link: str, buttons: list = None):
        self.template["elements"].append({
            "title": title,
            "description": description,
            "buttons": buttons if buttons is not None else list(),
            "action": {
                "type": "open_link",
                "link": link
            }
        })
        return self

    def add_button(self, text: str, payload: str):
        button = {
            "action": {
                "type": "text",
                "label": text,
                "payload": payload
            }
        }
        if len(self.template["elements"]) > 0:
            self.template["elements"][-1]["buttons"].append(button)
        else:
            return button
        return self

    def generate(self):
        return json.dumps(self.template)






