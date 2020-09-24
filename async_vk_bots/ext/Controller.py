import re
from asyncio import iscoroutinefunction

from async_vk_bots.ext.DataModels.Message.Message import Message


class Controller:
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


def controller(re_command, find_type="fullmatch", bot=None):
    def decorator(controller_cls: type):
        command_cls = type(f"_{controller_cls.__name__}Command", (_ControllerCommand,), {
            "__init__": lambda self: _ControllerCommand.__init__(
                self, _get_re_func(re_command, find_type), controller_cls
            )
        })
        if bot:
            bot.add_command(command_cls)
        return command_cls
    return decorator


def command(re_command, find_type="fullmatch", bot=None):
    def decorator(func):
        @controller(re_command, find_type, bot)
        class __Command(Controller):
            async def message(self):
                if iscoroutinefunction(func):
                    await func(self.model, self.data, self.reply)
                else:
                    func(self.model, self.data, self.reply)
        return func
    return decorator
