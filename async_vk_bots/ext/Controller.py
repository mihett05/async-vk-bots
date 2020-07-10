import re


class Controller:
    command = r""
    view_cls = None

    def __init__(self, bot=None):
        if bot:
            self.connect(bot)

    def get_data(self, text):
        res = re.fullmatch(self.command.lower(), text.lower())
        return bool(res), res

    @property
    def view(self):
        if hasattr(self.view_cls, "as_view") and hasattr(self.view_cls.as_view, "__call__"):
            return self.view_cls.as_view()
        raise Exception("view_cls must implement as_view function")

    @classmethod
    def connect(cls, bot):
        bot.add_controller(cls)


def controller(command_, search=False, bot=None):
    def decorator(view_cls_):
        class ControllerView(Controller):
            command = command_
            view_cls = view_cls_

            def get_data(self, text):
                if search:
                    res = re.search(self.command, text)
                    return bool(res), res
                return super().get_data(text)
        if bot:
            bot.add_controller(ControllerView)
        return ControllerView
    return decorator
