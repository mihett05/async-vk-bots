from .View import View


class PMView(View):
    async def view(self):
        if self.message.peer_id < 2_000_000_000:
            await super(PMView, self).view()
