import re


class Controller:
    command = r""
    view_cls = None

    def get_data(self, text):
        res = re.fullmatch(self.command, text)
        return bool(res), res

    @property
    def view(self):
        if hasattr(self.view_cls, "as_view") and hasattr(self.view_cls.as_view, "__call__"):
            return self.view_cls.as_view()
        raise Exception("view_cls must implement as_view function")
