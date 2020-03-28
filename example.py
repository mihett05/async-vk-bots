import json
from Bot import Bot
from ext.commands import command, Scenario
from api.KeyboardMaker import KeyBoardMaker, Color

group_id = 0
token = "token"

bot = Bot(group_id)
sc1 = Scenario({
    "buy": 1,
    "select": 2
})

default_kb = KeyBoardMaker(False).add_button("Buy", Color.Positive, payload=json.dumps({"button": "buy"})).generate()
select_kb = KeyBoardMaker()\
    .add_button("Pr 1", Color.Secondary, payload=json.dumps({"button": "select", "pr": 1}))\
    .add_button("Pr 2", Color.Primary, payload=json.dumps({"button": "select", "pr": 2}))\
    .generate()


@sc1.handler(1)
async def sc1_select(ctx):
    await ctx.reply("Выберите товар", keyboard=select_kb)


@sc1.handler(2)
async def sc1_success(ctx):
    await ctx.reply("Сделка совершенна", keyboard=default_kb)


@command(r"(Start|Начать)")
async def hype(msg, data, reply):
    await reply("Пример магазина", keyboard=default_kb)


bot.add_scenario(sc1)
bot.run(token)
