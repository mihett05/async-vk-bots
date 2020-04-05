from async_vk_bot import Bot
from .config import group_id, token

bot = Bot(group_id)

bot.run(token)