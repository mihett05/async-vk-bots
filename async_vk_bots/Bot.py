import asyncio
import json
from aiohttp import web
from .api.API import API
from .api.LongPoll import LongPoll
from async_vk_bots.ext import Controller, Event
from async_vk_bots.ext import View
from .ext.DataModels.Message.MessageEvent import MessageEvent


class Bot:
    def __init__(self, group_id, version="5.120", event_loop=None):
        self._token = ""
        self._v = version
        self._group_id = group_id
        self._scenarios = []
        self._listeners = dict()
        self._controllers = []
        self._events = []
        self._confirm = ""
        if event_loop is None:
            event_loop = asyncio.get_event_loop()
        self._loop = event_loop
        self._command_not_found = None
        self.api = None

    async def on_ready(self):
        pass

    def command(self, regexp_or_func):
        def decorator(func):
            class _CustomView(View):
                async def all(self):
                    await func(self.message, self.data, self.reply)
            if hasattr(regexp_or_func, "__call__"):
                class _CustomController(Controller):
                    view_cls = _CustomView

                    def get_data(self, text):
                        res = regexp_or_func(text)
                        return bool(res), res
            elif isinstance(regexp_or_func, str):
                class _CustomController(Controller):
                    command = regexp_or_func
                    view_cls = _CustomView
            else:
                raise Exception("regexp_or_func must be str or function")
            self.add_controller(_CustomController)
            return func
        return decorator

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

    def add_scenario(self, scenario):
        if scenario not in self._scenarios:
            self._scenarios.append(scenario)

    def on(self, event: str):
        def decorator(func):
            async def wrapper(data):
                await func(data)
            if event not in self._listeners:
                self._listeners[event] = list()
            self._listeners[event].append(wrapper)
            return wrapper
        return decorator

    def add_controller(self, controller):
        self._controllers.append(controller())

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
                msg = request["object"]
                for scenario in self._scenarios:
                    if await scenario.check_handlers(request):
                        return "ok"
                controllers = list(filter(lambda x: x.get_data(msg["message"]["text"])[0], self._controllers))
                for controller in controllers:
                    data = controller.get_data(msg["message"]["text"])[1]
                    await controller.view(self.api, msg, data)
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
        self.api = API(self._token, self._v, self._loop)
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
        self.api = API(self._token, self._v, self._loop)
        longpoll = LongPoll(self.api, self._group_id)
        await self.on_ready()
        async for event in longpoll.listen():
            if debug:
                await self.__handler(event)
            else:
                try:
                    await self.__handler(event)
                except BaseException as e:
                    print(e)

    def run(self, token, debug=False):
        print("Started")
        self._loop.run_until_complete(self.__run(token, debug))


