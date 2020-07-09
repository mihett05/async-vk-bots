import json
from .DataModels.Message.MessageEvent import MessageEvent


class Event:
    payload = ""

    def __init__(self, api, bot=None):
        if bot:
            self.connect(bot)
        self.api = api

    @classmethod
    def get_data(cls, text):
        return bool(cls.payload == text), text

    async def answer(self, event: MessageEvent):
        pass

    async def handle(self, obj):
        model = MessageEvent(obj)
        event_data = await self.answer(model)
        if isinstance(event_data, dict):
            event_data = json.dumps(event_data)
        else:
            event_data = str(event_data)
        if event_data:
            await self.api.send_message_event_answer(model.event_id, model.user_id, model.peer_id, event_data)

    @classmethod
    def connect(cls, bot):
        bot.add_event(cls)
