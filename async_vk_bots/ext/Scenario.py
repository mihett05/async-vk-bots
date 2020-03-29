import json
from .Context import Context


class Scenario:

    def __init__(self, entry_points):
        self._entry_points = entry_points
        self._handlers = dict()

    async def check_for_entry_point(self, event):
        if "payload" in event["object"]["message"]:
            payload = json.loads(event["object"]["message"]["payload"])
            if "button" in payload:
                for point in self._entry_points:
                    if point == payload["button"]:
                        ctx = Context(event, self._entry_points[point])
                        res = await self._handlers[self._entry_points[point]](ctx)
                        return True
        return False

    def handler(self, state):
        def decorator(func):
            async def wrapper(ctx):
                return await func(ctx)
            self._handlers[state] = wrapper
            return wrapper
        return decorator

