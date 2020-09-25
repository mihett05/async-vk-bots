import re
from asyncio import iscoroutinefunction

from async_vk_bots.ext.DataModels.Message.Message import Message


class MetaController(type):
    controllers = dict()

    def __new__(mcs, name, bases, attrs):
        cls = super(MetaController, mcs).__new__(mcs, name, bases, attrs)
        if name != "Controller":
            mcs.controllers[cls] = None
        return cls


class Controller(metaclass=MetaController):
    def __init__(self, api, event, data):
        self.api = api
        self.event = event
        self.model = Message(event["message"])
        self.data = data

    async def reply(self, message, **kwargs):
        await self.api.send(peer_id=self.model.peer_id, message=message, **kwargs)

    async def text(self):
        pass

    async def payload(self):
        pass

    async def message(self):
        if "payload" in self.event["message"]:
            if iscoroutinefunction(self.payload):
                await self.payload()
            else:
                self.payload()
        else:
            if iscoroutinefunction(self.text):
                await self.text()
            else:
                self.text()


class _ControllerCommand:
    def __init__(self, re_func, controller_cls):
        self.re_func = re_func
        self.controller = controller_cls

    async def handle(self, api, event):
        data = self.re_func(event["message"]["text"])
        if data:
            await self.controller(api, event, data).message()


def _get_re_func(exp, find_type="fullmatch"):
    if find_type in ["fullmatch", "search", "findall", "match"]:
        def _find_func(txt):
            find_func = getattr(re, find_type)
            res = find_func(exp, txt)
            if find_type != "findall" and res:
                return list(res.groups()) or [txt]
            return res or []
        return _find_func
    else:
        raise Exception(f"Unknown find_type: {find_type}")


def controller(re_command, find_type="fullmatch"):
    def decorator(controller_cls: type):
        if issubclass(controller_cls, Controller):
            MetaController.controllers[controller_cls] = _get_re_func(re_command, find_type)
        return controller_cls
    return decorator


def chat_controller(controller_cls):
    if issubclass(controller_cls, Controller):
        class __ChatController(controller_cls):
            async def message(self):
                if self.model.peer_id >= 2_000_000_000:
                    await super().message()
        if controller_cls in MetaController.controllers:
            MetaController.controllers[__ChatController] = MetaController.controllers.pop(controller_cls)
        return __ChatController
    else:
        raise Exception(
            f"{controller_cls.__name__} must be subclass of Controller"
        )


def command(re_command, find_type="fullmatch"):
    def decorator(func):
        @controller(re_command, find_type)
        class __Command(Controller):
            async def message(self):
                if iscoroutinefunction(func):
                    await func(self.model, self.data, self.reply)
                else:
                    func(self.model, self.data, self.reply)
        return func
    return decorator
