from async_vk_bots.Bot import Bot
from .Context import Context
from .Scenario import Scenario


def command(regexp):
    def decorator(func):
        if Bot.bot:
            Bot.bot.add_command(regexp, func)
    return decorator
