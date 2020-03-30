import json
from .Context import Context


def create_handler(handlers):
    def handler(button_type):
        def decorator(func):
            handlers[button_type] = func
            return func
        return decorator
    return handler


class Scenario:
    handlers = None

    def __init__(self, bot):
        self.bot = bot
        self._handlers = []

    async def check_handlers(self, event):
        if "payload" in event["object"]["message"]:
            payload = json.loads(event["object"]["message"]["payload"])
            if "button" in payload:
                for button_type in self.handlers:
                    if button_type == payload["button"]:
                        ctx = Context(event, 0)
                        await self.handlers[button_type](self, ctx)
                        return True
                for button_type in self._handlers:
                    if button_type == payload["button"]:
                        ctx = Context(event, 0)
                        await self._handlers[button_type](ctx)
                        return True
        return False

    def add_handler(self, button_type, func):
        self._handlers[button_type] = func

    def handler(self, button_type):
        def decorator(func):
            self.add_handler(button_type, func)
            return func
        return decorator
