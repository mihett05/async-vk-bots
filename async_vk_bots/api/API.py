import random
import json
from typing import Optional, Union
import aiohttp
from .APIError import APIError


class API:
    api = None  # Singleton
    
    def __new__(cls, *args, **kwargs):
        if not cls.api:
            cls.api = super(API, cls).__new__(cls)
        return cls.api

    def __init__(self, token, version, group_id, event_loop):
        self._token = token
        self._v = version
        self._group_id = group_id
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

    async def send(self, peer_id: int, message: str,
                   attachment: Optional[str] = None, reply_to: Optional[int] = None,
                   forward_messages: Optional[list] = None, sticker_id: Optional[int] = None,
                   keyboard: Optional[Union[dict, str]] = None,
                   payload: Optional[Union[dict, str]] = None,
                   template: Optional[Union[dict, str]] = None,
                   dont_parse_links: bool = True, disable_mentions: bool = False,
                   lat: Optional[int] = None, long: Optional[int] = None):
        params = {
            "peer_id": peer_id,
            "message": message.replace("+", "%2B"),
            "random_id": random.randint(0, 18446744073709551615),
            "attachment": attachment,
            "reply_to": reply_to,
            "forward_messages": forward_messages,
            "sticker_id": sticker_id,
            "keyboard": json.dumps(keyboard) if isinstance(keyboard, dict) else str(keyboard) if keyboard else None,
            "payload": json.dumps(payload) if isinstance(payload, dict) else str(payload) if payload else None,
            "dont_parse_links": int(dont_parse_links),
            "disable_mentions": int(disable_mentions),
            "template": json.dumps(template) if isinstance(template, dict) else str(template) if template else None,
            "lat": lat,
            "long": long,
            "group_id": self._group_id
        }
        resp = await self.call("messages.send", **params)
        if "error" in resp:
            raise APIError(json.dumps(resp["error"]))

    async def edit(self, peer_id: int, message: str,
                   message_id: int = None,
                   conversation_message_id: int = None,
                   lat: Optional[int] = None, long: Optional[int] = None,
                   attachment: Optional[str] = None,
                   keep_forward_messages: bool = True,
                   keep_snippets: bool = False,
                   dont_parse_links: bool = True,
                   keyboard: Optional[Union[dict, str]] = None,
                   template: Optional[Union[dict, str]] = None):
        if message_id and conversation_message_id:
            raise APIError("Can't use message_id and conversation_message_id at the same time")
        params = {
            "peer_id": peer_id,
            "message": message.replace("+", "%2B"),
            ("message_id" if message_id else "conversation_message_id"):
                (message_id if message_id else conversation_message_id),
            "attachment": attachment,
            "keyboard": json.dumps(keyboard) if isinstance(keyboard, dict) else str(keyboard) if keyboard else None,
            "keep_forward_messages": int(keep_forward_messages),
            "keep_snippets": int(keep_snippets),
            "dont_parse_links": int(dont_parse_links),
            "template": json.dumps(template) if isinstance(template, dict) else str(template) if template else None,
            "lat": lat,
            "long": long,
            "group_id": self._group_id
        }
        resp = await self.call("messages.edit", **params)
        if "error" in resp:
            raise APIError(json.dumps(resp["error"]))

    async def send_message_event_answer(self, event_id, user_id, peer_id, event_data):
        params = {
            "event_id": str(event_id),
            "user_id": int(user_id),
            "peer_id": int(peer_id),
            "event_data": json.dumps(event_data) if isinstance(event_data, dict) else str(event_data)
        }

        resp = await self.call("messages.sendMessageEventAnswer", **params)
        if "error" in resp:
            raise APIError(json.dumps(resp["error"]))
