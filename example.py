import json
from async_vk_bots import BaseBot, Scenario, create_command, create_handler
from async_vk_bots.api.KeyboardMaker import KeyBoardMaker, Color

default_kb = KeyBoardMaker(False).add_button("Buy", Color.Positive, payload=json.dumps({"button": "buy"})).generate()
select_kb = KeyBoardMaker()\
    .add_button("Pr 1", Color.Secondary, payload=json.dumps({"button": "select", "pr": 1}))\
    .add_button("Pr 2", Color.Primary, payload=json.dumps({"button": "select", "pr": 2}))\
    .generate()
group_id = 0
token = ""


class ShopScenario(Scenario):
    handlers = dict()
    handler = create_handler(handlers)

    @handler("buy")
    async def select(self, ctx):
        await ctx.reply("Выберите товар", keyboard=select_kb)

    @handler("select")
    async def success(self, ctx):
        await ctx.reply("Сделка совершенна", keyboard=default_kb)


class Bot(BaseBot):
    commands = dict()
    command = create_command(commands)

    def __init__(self):
        super().__init__(group_id)
        self.add_scenario(ShopScenario(self))

    async def on_ready(self):
        print("Ready")

    @command(r"(Start|Начать)")
    async def hype(self, msg, data, reply):
        await reply("Пример магазина", keyboard=default_kb)


Bot().run(token)
