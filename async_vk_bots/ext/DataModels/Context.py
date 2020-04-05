from async_vk_bots.api.API import API


class Context:
    def __init__(self, message, state):
        self.event = message
        self.api = API.api
        self.state = state

    async def reply(self, message, **kwargs):
        await self.api.send(peer_id=self.event["object"]["message"]["peer_id"], message=message, **kwargs)
