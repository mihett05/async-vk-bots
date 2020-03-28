import random
import json
import aiohttp
from .APIError import APIError


class API:
    api = None  # Singleton
    
    def __new__(cls, *args, **kwargs):
        if not cls.api:
            cls.api = super(API, cls).__new__(cls)
        return cls.api

    def __init__(self, token, version, event_loop):
        self._token = token
        self._v = version
        self.loop = event_loop
        self.session = None

    async def fetch(self, url: str):
        if not self.session:
            self.session = aiohttp.ClientSession(loop=self.loop)
        async with self.session.get(url) as response:
            return await response.json()

    async def call(self, method: str, **params):
        params = dict(map(lambda x: (x, params[x]), filter(lambda x: bool(params[x]), params.keys())))
        return await self.fetch("https://api.vk.com/method/{}?{}&access_token={}&v={}"
                                .format(method, "&".join(map(lambda x: "{}={}".format(x, params[x]), params)),
                                        self._token, self._v))

    async def send(self, peer_id: int, message: str, attachment: str = None, reply_to: int = None,
                   forward_messages: list = None, sticker_id: int = None, keyboard: dict = None, payload: dict = None,
                   dont_parse_links: bool = True, disable_mentions: bool = False):
        params = {
            "peer_id": peer_id,
            "message": message,
            "random_id": random.randint(0, 18446744073709551615),
            "attachment": attachment,
            "reply_to": reply_to,
            "forward_messages": forward_messages,
            "sticker_id": sticker_id,
            "keyboard": keyboard,
            "payload": payload,
            "dont_parse_links": int(dont_parse_links),
            "disable_mentions": int(disable_mentions)
        }
        resp = await self.call("messages.send", **params)
        if "error" in resp:
            raise APIError(json.dumps(resp["error"]))
