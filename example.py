import json
from async_vk_bots import Bot
from async_vk_bots.api.KeyboardMaker import KeyBoardMaker, Color
from async_vk_bots.ext import View, Controller, controller
token = ""
group_id = 0

default_kb = KeyBoardMaker(False).add_button("Hype", Color.Positive, payload=json.dumps({"button": "hype"})).generate()


class HypeView(View):
    async def get(self):
        await self.reply("Hype ()_()", keyboard=default_kb)

    async def post(self):
        await self.reply(self.message.payload, keyboard=default_kb)


class HypeController(Controller):
    command = r"Hype"
    view_cls = HypeView


bot = Bot(group_id)


@bot.command(r"Hi")
async def hype(msg, data, reply):
    await reply("Hello world", keyboard=default_kb)


bot.add_controller(HypeController)
bot.run(token)
