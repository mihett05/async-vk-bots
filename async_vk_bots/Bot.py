import asyncio
import json
from aiohttp import web
from .api.API import API
from .api.LongPoll import LongPoll
from async_vk_bots.ext import Controller, Event, command
from async_vk_bots.ext import View
from .ext.DataModels.Message.MessageEvent import MessageEvent


class Bot:
    def __init__(self, group_id, version="5.120", loop=None):
        self._token = ""
        self._v = version
        self._group_id = group_id
        self._confirm = ""

        self._listeners = dict()
        self._commands = []
        self._events = []

        self._loop = loop
        if not isinstance(self._loop, asyncio.BaseEventLoop):
            self._loop = asyncio.get_event_loop()

        self._command_not_found = None
        self.api = None
        self._ready_cb = None

    def on_ready(self, func):
        self._ready_cb = func

    def command(self, re_command, find_type="fullmatch"):
        return command(re_command, find_type, self)

    def event(self, regexp_or_func):
        def decorator(func):
            class _CustomEvent(Event):
                async def answer(self, event):
                    return await func(event)

            if hasattr(regexp_or_func, "__call__"):
                def __get_data(self, text):
                    res = regexp_or_func(text)
                    return bool(res), res
                _CustomEvent.get_data = __get_data
            elif isinstance(regexp_or_func, str):
                _CustomEvent.payload = regexp_or_func

            self.add_event(_CustomEvent)
            return func
        return decorator

    def on(self, event: str):
        def decorator(func):
            async def wrapper(data):
                await func(data)
            if event not in self._listeners:
                self._listeners[event] = list()
            self._listeners[event].append(wrapper)
            return wrapper
        return decorator

    def add_command(self, controller):
        self._commands.append(controller())

    def add_event(self, event):
        self._events.append(event)

    async def __handler(self, request):
        try:
            if request["type"] in self._listeners:
                for func in self._listeners[request["type"]]:
                    await func(request["object"])
            elif request["type"] in self._listeners:
                for func in self._listeners[request["type"]]:
                    await func(request["object"])
            
            if request["type"] == "confirmation":
                return self._confirm
            elif request["type"] == "message_new":
                event = request["object"]
                for controller in self._commands:
                    await controller.handle(self.api, event)
            elif request["type"] == "message_event":
                obj = request["object"]
                events = list(filter(lambda x: x.get_data(json.dumps(obj["payload"]))[0], self._events))
                for event in events:
                    await event(self.api).handle(obj)

            return "ok"
        except KeyError:
            return "not vk"

    def get_web_hook(self, token, confirm_str):
        self._confirm = confirm_str
        self._token = token
        self.api = API(self._token, self._v, self._group_id, self._loop)
        return self.__web_hook

    async def __web_hook(self, request):
        try:
            try:
                json_data = await request.json()
                return web.Response(text=await self.__handler(json_data))
            except json.JSONDecodeError:
                return web.Response(text="Not json")
        except BaseException as e:
            print(e)
            return web.Response(text="error", content_type="text/plain", status=500)

    async def __run(self, token, debug):
        self._token = token
        self.api = API(self._token, self._v, self._group_id, self._loop)
        longpoll = LongPoll(self.api, self._group_id)
        if hasattr(self._ready_cb, "__call__"):
            if asyncio.iscoroutinefunction(self._ready_cb):
                await self._ready_cb()
            else:
                self._ready_cb()
        async for event in longpoll.listen():
            if debug:
                await self.__handler(event)
            else:
                try:
                    await self.__handler(event)
                except BaseException as e:
                    print(e)

    def run(self, token, debug=False):
        self._loop.run_until_complete(self.__run(token, debug))


