from .DataModels.Message.Message import Message


class View:
    def __init__(self, api, event, data):
        self.api = api
        self.event = event
        self.message = Message(event["message"])
        self.data = data

    async def reply(self, message, **kwargs):
        await self.api.send(peer_id=self.message.peer_id, message=message, **kwargs)

    async def get(self):
        pass

    async def post(self):
        pass

    async def all(self):
        pass

    async def view(self):
        await self.all()
        if "payload" in self.event["message"]:
            await self.post()
        else:
            await self.get()

    @classmethod
    def as_view(cls):
        async def view(api, event, data):
            await cls(api, event, data).view()
        return view
