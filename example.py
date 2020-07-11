from async_vk_bots import Bot
from async_vk_bots.api.KeyboardMaker import KeyBoardMaker, Color
from async_vk_bots.ext import View, controller
from async_vk_bots.ext.DataModels.Message.MessageEvent import MessageEvent
from async_vk_bots.ext.DataModels.Message.Message import Message
token = ""
group_id = 0

bot = Bot(group_id)
menu = KeyBoardMaker(False, True, bot)


@menu.callback("Get my ID", Color.Primary, {"action": "get_id"})
async def get_id(event: MessageEvent):
    if event.conversation_message_id:
        await bot.api.edit(event.user_id, f"Your id is {event.user_id}!",
                           conversation_message_id=event.conversation_message_id, keyboard=menu)


@menu.callback("Clear", Color.Secondary, {"action": "clear"})
async def clear(event: MessageEvent):
    if event.conversation_message_id:
        # Can't use edit and snackbar at the same time
        await bot.api.edit(event.user_id, f"Menu",
                           conversation_message_id=event.conversation_message_id, keyboard=menu)


menu = menu.generate()

default_kb = KeyBoardMaker(False, bot=bot)\
    .add_button("GetMenu", Color.Positive, payload={"button": "menu"})


@default_kb.callback("NewMenu", Color.Primary, payload={"action": "get_menu"})
async def get_menu(event: MessageEvent):
    await bot.api.send(event.user_id, "Menu", keyboard=menu)
    return {
        "type": "show_snackbar",
        "text": "You've got new menu!"
    }


default_kb = default_kb.generate()


@bot.command(r"GetMenu")
async def get_menu(msg: Message, data, reply):
    await reply("Menu", keyboard=menu)


@controller("NewHype", bot=bot)
class NewHype(View):
    async def text(self):
        await self.reply("Hype ()_()", keyboard=default_kb)

    async def payload(self):
        await self.reply(self.message.payload, keyboard=default_kb)


@bot.command(r"Hi")
async def hype(msg, data, reply):
    await reply("Hello world", keyboard=default_kb)


bot.run(token)
