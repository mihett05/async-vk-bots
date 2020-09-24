import json
from async_vk_bots import Bot
from async_vk_bots.api.KeyboardMaker import KeyBoardMaker, Color
from async_vk_bots.ext import Controller, controller

group_id = 0
bot = Bot(group_id)

menu = KeyBoardMaker(False)\
    .add_button("Hello world!", Color.Positive, {"action": "hello_world"})\
    .add_button("Hi", Color.Primary, {"action": "hi"})
default_kb = menu.generate()


@controller(r"Hello world!", bot=bot)
class HelloController(Controller):
    # You can bind controller to bot
    async def text(self):
        # self.reply is binding for self.api.send, where id already set as self.model.from_id
        await self.reply("Hi from simple message!")

    async def payload(self):
        # self.model is instance of async_vk_bots.ext.DataModels.Message.Message.Message
        await self.reply(f"Hello from button message! Payload: {json.dumps(self.model.payload)}")


@bot.command(r"Hi")
async def hype(msg, data, reply):
    # msg is like self.model in controllers
    # data is result of regexp
    await reply("Hello world", keyboard=default_kb)


@bot.on_ready
async def on_ready():
    print("Ready")


bot.run("token", debug=True)
