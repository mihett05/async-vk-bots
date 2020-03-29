import json
import aiohttp
from .API import API
from .APIError import APIError


class LongPoll:
    def __init__(self, api: API, group_id: int):
        self.api = api
        self._group_id = group_id
        self._server = None
        self._key = None
        self._ts = None
        self.session = None

    async def fetch(self, url: str):
        if not self.session:
            self.session = aiohttp.ClientSession(loop=self.api.loop)
        async with self.session.get(url) as response:
            return await response.json()

    async def get_long_poll(self, update_ts=True):
        resp = await self.api.call("groups.getLongPollServer", group_id=self._group_id)
        if "response" in resp:
            self._server = resp["response"]["server"]
            self._key = resp["response"]["key"]
            if update_ts:
                self._ts = resp["response"]["ts"]
        elif "error" in resp:
            raise APIError(json.dumps(resp["error"]))
        else:
            raise APIError("Problem with api")

    async def __get_events(self):
        resp = await self.fetch(f"{self._server}?act=a_check&key={self._key}&ts={self._ts}&wait=25")
        if "failed" in resp:
            if resp["failed"] == 1:
                self._ts = resp["ts"]
                return await self.__get_events()
            elif resp["failed"] == 2:
                await self.get_long_poll(update_ts=False)
                return await self.__get_events()
            elif resp["failed"] == 3:
                await self.get_long_poll()
                return await self.__get_events()
        self._ts = resp["ts"]
        return resp["updates"]

    async def listen(self):
        await self.get_long_poll()
        while True:
            for event in (await self.__get_events()):
                yield event
