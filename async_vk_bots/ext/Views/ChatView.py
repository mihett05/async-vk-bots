from .View import View


class ChatView(View):
    async def view(self):
        if self.message.peer_id > 2_000_000_000:
            await super(ChatView, self).view()
