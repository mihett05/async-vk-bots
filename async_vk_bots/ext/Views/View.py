from async_vk_bots.ext.DataModels.Message.Message import Message


class View:
    def __init__(self, api, event, data):
        self.api = api
        self.event = event
        self.message = Message(event["message"])
        self.data = data

    async def reply(self, message, **kwargs):
        await self.api.send(peer_id=self.message.peer_id, message=message, **kwargs)

    async def text(self):
        pass

    async def payload(self):
        pass

    async def all(self):
        pass

    async def view(self):
        await self.all()
        if "payload" in self.event["message"]:
            await self.payload()
        else:
            await self.text()

    @classmethod
    def as_view(cls):
        async def view(api, event, data):
            await cls(api, event, data).view()
        return view
